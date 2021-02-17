# -*- coding: utf-8 -*-
import os
import inspect

try:
    from functools import partial, total_ordering
except ImportError:
    total_ordering = dir

from yurlungur.core.deco import trace
from yurlungur.core.exception import YException
from yurlungur.core.wrapper import _YObject, _YAttr
# from yurlungur.core.datatype import Vector, Matrix, Color
from yurlungur.tool.meta import meta


class Object(_YObject):
    """document base object
    >>> cone = Object("pCone")
    >>> cone.set("my_cone")
    >>> cone.castShadows.set(True)
    """

    def __init__(self, item):
        self.item = item

    def __repr__(self):
        if getattr(meta, "SDNode", False):
            return "id:" + self.name
        else:
            return self.name

    def __dir__(self):
        return self.attrs

    def __getattr__(self, val):
        return self.attr(val)

    @property
    def name(self):
        if getattr(meta, "SDNode", False):
            return self.id
        elif getattr(meta, "hda", False):
            return self.item.name
        else:
            return self.item

    @property
    def id(self):
        if getattr(meta, "SDNode", False):
            node_id = ""
            for node in meta.graph.getNodes():
                d = node.getDefinition()
                if (d.getId() == self.item or d.getLabel() == self.item or node.getIdentifier() == self.item):
                    node_id = node.getIdentifier()
                    break
            return node_id if node_id else meta.graph.getIdentifier()

        if getattr(meta, "ls", False):
            return meta.ls(self.name, uuid=1)[0] or 0

        if getattr(meta, "hda", False):
            return meta.node(self.name).sessionId() or 0

        if getattr(meta, "runtime", False):
            return meta.runtime.getnodebyname(self.name).gbufferChannel or 0

        if getattr(meta, "data", False):
            return meta.data.objects[self.name].id_data or 0

        if getattr(meta, "C4DAtom", False):
            return meta.doc.SearchObject(self.item).GetGUID()

        if getattr(meta, "knob", False):
            return meta.toNode(self.name)["name"].value() or 0

        if getattr(meta, "fusion", False):
            return meta.fusion.GetCurrentComp().FindTool(self.name).ID or 0

        if getattr(meta, "uclass", False):
            return meta.ue4.uname(self.name).get_name() or 0

        if getattr(meta, "Debug", False):
            return meta.engine.GameObject.Find(self.name).GetInstanceID() or 0

        if getattr(meta, "BVH3", False):
            return meta.active_document()

        if getattr(meta, "SceneObject", False):
            raise YException("api is not found")

        if getattr(meta, "textureset", False):
            raise YException("api is not found")

    @trace
    def set(self, *args, **kwargs):
        """
        rename object
        Args:
            *args:
            **kwargs:

        Returns:

        """
        if getattr(meta, "SDNode", False):
            meta.graph.setIdentifier(args[0])

        if getattr(meta, "rename", False):
            return meta.rename(self.item, *args, **kwargs)

        if getattr(meta, "hda", False):
            return meta.node(self.item).setName(*args, **kwargs)

        if getattr(meta, "runtime", False):
            meta.runtime.getnodebyname(self.name).name = args[0]
            return Node(args[0])

        if getattr(meta, "data", False):
            meta.data.objects[self.item].name = "".join(args)
            return "".join(args)

        if getattr(meta, "C4DAtom", False):
            return meta.doc.SearchObject(self.item).SetName(args[0])

        if getattr(meta, "knob", False):
            meta.toNode(self.item).setName(args[0], **kwargs)

        if getattr(meta, "fusion", False):
            return (
                meta.fusion.GetCurrentComp()
                    .FindTool(self.item)
                    .SetAttrs({"TOOLS_Name": args[0]})
            )

        if getattr(meta, "doc", False):
            try:
                return setattr(meta.doc.activeLayer, "name", args[0])
            except AttributeError:
                return meta.doc.currentLayer().setValue_forKey_(args[0], "name")

        if getattr(meta, "uclass", False):
            uname = meta.ue4.uname(self.name)
            if type(uname) == str:
                meta.assets.rename_asset(
                    uname, os.path.join(os.path.dirname(uname), args[0])
                )
                return Node(args[0])
            else:
                return uname.set_actor_label(args[0])

        if getattr(meta, "Debug", False):
            go = meta.engine.GameObject.Find(self.name)
            if go:
                meta.editor.Undo.RegisterFullObjectHierarchyUndo(go, "Rename %s" % args[0])
                go.name = args[0]
            else:
                meta.editor.AssetDatabase.RenameAsset(self.name, args[0])
                asset = meta.editor.AssetDatabase.LoadAssetAtPath(*args[1:])
                meta.editor.EditorUtility.SetDirty(asset)

            return Node(args[0])

        if getattr(meta, "BVH3", False):
            node = meta.active_document().first_name(args[0])
            return node.rename(args[1])

        if getattr(meta, "SceneObject", False):
            meta.findObject(args[0]).name = args[1]
            return meta.findObject(args[1])

        if getattr(meta, "textureset", False):
            return

    @trace
    def attr(self, val, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            prop = meta.graph.getNodeFromId(self.name).getPropertyFromId(
                val, meta.sd.SDPropertyCategory.Input
            )
            return Attribute(
                meta.graph.getNodeFromId(self.name).getPropertyValue(prop).get(),
                self.name,
                val,
            )

        if getattr(meta, "getAttr", False):
            return Attribute(
                meta.getAttr(self.name + "." + val, *args, **kwargs), self.name, val
            )

        if getattr(meta, "hda", False):
            parm = meta.node(self.name).parm(val) or meta.node(self.name).parmTuple(val)
            return Attribute(parm.eval(), self.name, val)

        if getattr(meta, "runtime", False):
            return Attribute(
                getattr(meta.runtime.getnodebyname(self.name), val), self.name, val
            )

        if getattr(meta, "data", False):
            return Attribute(meta.data.objects[self.name].name, self.name, val)

        if getattr(meta, "C4DAtom", False):
            return Attribute(
                meta.doc.SearchObject(self.name)[getattr(meta, val)], self.name, val
            )

        if getattr(meta, "knob", False):
            return Attribute(meta.toNode(self.name)[val], self.name, val)

        if getattr(meta, "fusion", False):
            return Attribute(
                getattr(meta.fusion.GetCurrentComp().FindTool(self.name), val), self.name, val
            )

        if getattr(meta, "doc", False):
            try:
                layer = meta.doc.layers[self.name]
            except TypeError:
                layer = meta.ps.Document().layers[self.name]

            return Attribute(getattr(layer, val), self.name, val)

        if getattr(meta, "uclass", False):
            try:
                return Attribute(
                    meta.ue4.uname(self.name).get_editor_property(val), self.name, val
                )
            except:
                return Attribute(
                    meta.ue4.uname(self.name).root_component.get_editor_property(val),
                    self.name, val
                )

        if getattr(meta, "Debug", False):
            obj = meta.engine.GameObject.Find(self.name)
            for com in obj.GetComponentsInChildren(meta.engine.Component):
                if val in dir(obj.GetComponent(com.GetType())):
                    return Attribute(obj.GetComponent(com.GetType()), self.name, val)
            return None

        if getattr(meta, "BVH3", False):
            node = meta.active_document().first_name(self.name)
            return Attribute(node.plug(val), self.name, val)

        if getattr(meta, "SceneObject", False):
            return Attribute(meta.findObject(val), self.name, val)

        if getattr(meta, "textureset", False):
            raise YException("api is not found")

    @property
    def attrs(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            return (
                prop.getId() for prop in
                meta.graph.getNodeFromId(self.name).getProperties(
                    meta.sd.SDPropertyCategory.Input
                )
            )

        if getattr(meta, "listAttr", False):
            return tuple(meta.listAttr(self.name, *args, **kwargs) or [])

        if getattr(meta, "hda", False):
            return (p.name() for p in meta.node(self.name).parms() or [])

        if getattr(meta, "runtime", False):
            return tuple(inspect.getmembers(meta.runtime.getnodebyname(self.name)))

        if getattr(meta, "data", False):
            return tuple(inspect.getmembers(meta.data.objects[self.name]))

        if getattr(meta, "C4DAtom", False):
            attrs = []
            ids = {}  # {v.lower(): v for v in dir(app.application) if v.isupper()}
            for k, v in ids.items():
                try:
                    meta.doc.SearchObject(self.name)[getattr(meta, v)]
                    attrs.append(k)
                except AttributeError:
                    pass
            return tuple(attrs)

        if getattr(meta, "knob", False):
            return ([knob.name() for knob in meta.toNode(self.name).allKnobs()])

        if getattr(meta, "fusion", False):
            return tuple(meta.fusion.GetCurrentComp().FindTool(self.name).GetAttrs())

        if getattr(meta, "doc", False):
            try:
                return (p for p, _ in inspect.getmembers(meta.photoshop.Photoshop.ArtLayer) if "_" not in p)
            except AttributeError:
                return (k for k in meta.ps.Document()._doc.layers()[0].properties())

        if getattr(meta, "uclass", False):
            return meta.ue4.uname(self.name).component_tags()

        if getattr(meta, "Debug", False):
            obj = meta.engine.GameObject.Find(self.name)
            attrs = dir(obj)
            for com in obj.GetComponentsInChildren(meta.engine.Component):
                attrs.extend(dir(obj.GetComponent(com.GetType())))
            return (set([attr for attr in attrs if not attr.startswith("__")]))

        if getattr(meta, "BVH3", False):
            node = meta.active_document().first_name(self.name)
            return (plug.name() for plug in node.plugs())

        if getattr(meta, "SceneObject", False):
            return (attr for attr in dir(meta.findObject(args[0])) if not attr.startswith("__"))

        if getattr(meta, "textureset", False):
            raise YException("api is not found")

    @trace
    def create(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            node_id = (
                args[0] if "::" in args[0] else "::".join(["sbs", "compositing", args[0]])
            )
            return Node(meta.graph.newNode(node_id).getIdentifier())

        if getattr(meta, "createNode", False):
            return Node(meta.createNode(*args, **kwargs))

        if getattr(meta, "hda", False):
            if len(args) == 0 and len(kwargs) == 0:
                return Node(
                    partial(meta.node(self.name).createNode, self.name)(
                        *args, **kwargs
                    ).path()
                )
            return Node(meta.node(self.name).createNode(*args, **kwargs).path())

        if getattr(meta, "runtime", False):
            obj = getattr(meta.runtime, args[0])
            msx_class = meta.runtime.classOf(obj)
            _obj = obj(**kwargs)

            if str(msx_class) == "modifier":
                meta.runtime.addModifier(meta.runtime.getnodebyname(self.name), _obj)
                return Node(
                    meta.runtime.getnodebyname(self.name).name + "." + _obj.name
                )

            elif str(msx_class) == "material":
                meta.runtime.material = _obj

            return Node(_obj.name)

        if getattr(meta, "data", False):
            if self.name:
                self.select(self.name)
                return meta.ops.object.modifier_add(type=str(args[0]).upper())
            else:
                try:
                    return getattr(meta.ops.mesh, args[0] + "_add")(*args[1:], **kwargs)
                except AttributeError:
                    return partial(meta.ops.object.add, type=str(args[0]).upper())(*args[1:], **kwargs)

        if getattr(meta, "C4DAtom", False):
            if args[0][0] == "O":  # object
                obj = meta.BaseObject(getattr(meta, args[0]))
                meta.doc.InsertObject(obj)

            if args[0][0] == "T":  # tag
                obj = meta.doc.SearchObject(self.name).MakeTag(getattr(meta, args[0]))

            if args[0][0] == "M":  # material
                obj = meta.BaseMaterial(getattr(meta, args[0]))
                meta.doc.InsertMaterial(obj)

            meta.EventAdd()
            return Node(obj.GetName())

        if getattr(meta, "fusion", False):
            return Node(meta.fusion.GetCurrentComp().AddTool(*args, **kwargs).Name)

        if getattr(meta, "doc", False):
            try:
                ps = getattr(meta.photoshop.Photoshop, "ps%s" % args[0], meta.doc.psNormalLayer)
                layer = meta.doc.artLayers.Add()
                layer.name = self.name
                return setattr(layer, "Kind", ps)
            except AttributeError:
                _ = kwargs.update({"name": self.name})
                layer = meta.classForScriptingClass_("art layer").alloc().initWithProperties_(kwargs)
                meta.ps.Document()._doc.artLayers().addObject_(layer)
                return Object(self.name)

        if getattr(meta, "uclass", False):
            factory = getattr(meta, self.name + "Factory")
            if not args:
                args = (self.name, "/Game", None)

            assert len(args) == 3 and factory

            new_asset = partial(meta.tools.create_asset, *args)(factory(), **kwargs)
            if new_asset:
                meta.assets.save_loaded_asset(new_asset)
                return Node(new_asset.get_name())
            else:
                return

        if getattr(meta, "Debug", False):
            go = meta.engine.GameObject.Find(self.name)
            cm = getattr(meta.engine, args[0])

            if go is None:
                if issubclass(cm, meta.engine.Behaviour):
                    import clr
                    T = clr.GetClrType(cm)
                    go = meta.editor.ObjectFactory.CreateGameObject(self.name, [T])
                    meta.editor.Undo.RegisterCreatedObjectUndo(go, "Create %s" % self.name)
                    return Object(go.name)
                else:
                    # prefab = PrefabUtility.CreatePrefab("Assets/camera_test.prefab", go)
                    # PrefabUtility.ReplacePrefab(go, prefab, ReplacePrefabOptions.ConnectToPrefab)
                    # issubclass(cm, meta.engine.Object)
                    instance = meta.editor.ObjectFactory.CreateInstance(cm)
                    return meta.editor.AssetDatabase.CreateAsset(instance, "Assets/%s" % self.name)

            elif go and isinstance(cm, meta.engine.Component):
                meta.editor.Undo.AddComponent(go, cm)
                return Object(cm.name)

        if getattr(meta, "BVH3", False):
            node = meta.Node(*args)
            return Node(node.name())

        if getattr(meta, "SceneObject", False):
            obj = {
                "mesh": meta.MeshObject, "material": meta.Material,
                "light": meta.LightObject, "camera": meta.CameraObject, "fog": meta.FogObject,
            }[args[0]](*args[1:])
            return Object(obj.name)

        if getattr(meta, "textureset", False):
            raise YException("api is not found")

    @trace
    def delete(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            return meta.graph.deleteNode(meta.graph.getNodeFromId(self.name))

        if getattr(meta, "delete", False):
            node = meta.toNode(self.name) if getattr(meta, "knob") else self.name
            return meta.delete(node, *args, **kwargs)

        if getattr(meta, "hda", False):
            return meta.node(self.name).destroy()

        if getattr(meta, "runtime", False):
            return meta.runtime.delete(meta.runtime.getnodebyname(self.name))

        if getattr(meta, "data", False):
            return meta.context.collection.objects.unlink(meta.data.objects[self.name])

        if getattr(meta, "C4DAtom", False):
            return meta.doc.SearchObject(self.item).Remove()

        if getattr(meta, "fusion", False):
            return meta.fusion.GetCurrentComp().FindTool(self.name).Delete()

        if getattr(meta, "doc", False):
            try:
                return meta.doc.layers[self.name].delete()
            except TypeError:
                return meta.ps.Document().layers[self.name].delete()

        if getattr(meta, "uclass", False):
            uname = meta.ue4.uname(self.name)
            if type(uname) == str:
                return meta.assets.delete_asset(uname)
            else:
                return uname.destroy_actor()

        if getattr(meta, "Debug", False):
            go = meta.engine.GameObject.Find(self.name)
            if go:
                return meta.editor.Undo.DestroyObjectImmediate(go)
            else:
                return meta.editor.AssetDatabase.DeleteAsset(self.name)

        if getattr(meta, "BVH3", False):
            node = meta.active_document().find_first(self.name)
            return node.delete_node(True)

        if getattr(meta, "SceneObject", False):
            return meta.findObject(self.name).destroy()

        if getattr(meta, "textureset", False):
            raise YException("api is not found")

    @trace
    def instance(self, *args, **kwarg):
        if getattr(meta, "SDNode", False):
            return meta.graph.newInstanceNode(self.name, *args, **kwarg)

        if getattr(meta, "instance", False):
            if len(args) > 0:
                return meta.instance(self.name, lf=1)
            else:
                return meta.listRelatives(self.name, ap=1, f=1)[1:] or None

        if getattr(meta, "runtime", False):
            return Node(
                meta.runtime.instance(meta.runtime.getnodebyname(self.name)).name
            )

        if getattr(meta, "data", False):
            return meta.ops.object.make_local(type='SELECT_OBJECT')

        if getattr(meta, "C4DAtom", False):
            obj = meta.InstanceObject()
            obj.SetReferenceObject(meta.doc.SearchObject(self.name))
            meta.doc.InsertObject(obj)
            return obj.GetName()

        if getattr(meta, "hda", False):
            return meta.node(self.name).copyTo(*args, **kwarg)

        if getattr(meta, "knob", False):
            if len(args) > 0:
                return meta.clone(meta.toNode(self.name), *args, **kwarg)
            else:
                return meta.toNode(self.name).clones()

        if getattr(meta, "fusion", False):
            meta.fusion.GetCurrentComp().Copy(self.name)
            return meta.fusion.GetCurrentComp().Paste(*args, **kwarg)

        if getattr(meta, "doc", False):
            try:
                return meta.doc.layers[self.name].duplicate()
            except TypeError:
                return meta.ps.Document().layers[self.name].duplicate()

        if getattr(meta, "uclass", False):
            uname = meta.ue4.uname(self.name)
            if type(uname) == str:
                return meta.assets.duplicate_asset(
                    uname, os.path.join(os.path.dirname(uname), *args)
                )
            else:
                return

        if getattr(meta, "Debug", False):
            go = meta.engine.GameObject.Find(self.name)
            if go:
                return go.Instantiate(go, *args)
            else:
                meta.editor.AssetDatabase.CopyAsset(self.name, args[0])
                asset = meta.editor.AssetDatabaseLoadAssetAtPath(*args[1:])
                meta.editor.EditorUtility.SetDirty(asset)
                return Object(asset.name)

        if getattr(meta, "SceneObject", False):
            return Object(meta.findObject(self.name).duplicate(args[0]).name)

    @trace
    def select(self, *args, **kwargs):
        from yurlungur.core.command import node

        if getattr(meta, "SDNode", False):
            return node.selected

        if getattr(meta, "select"):
            if "shape" not in kwargs and "s" not in kwargs:
                kwargs["s"] = True

            if len(args) == 0 and len(kwargs) == 0:
                return node.selected
            else:
                return meta.select(*args, **kwargs)

        if getattr(meta, "hda", False):
            if len(args) == 0 and len(kwargs) == 0:
                return node.selected
            else:
                return meta.node(self.name).setCurrent(*args, **kwargs)

        if getattr(meta, "runtime", False):
            if len(args) == 0 and len(kwargs) == 0:
                return node.selected
            else:
                return meta.runtime.select(meta.runtime.getnodebyname(self.name))

        if getattr(meta, "data", False):
            if len(args) == 0 and len(kwargs) == 0:
                return node.selected
            else:
                return meta.ops.object.select_pattern(pattern=self.name)

        if getattr(meta, "C4DAtom", False):
            if len(args) == 0 and len(kwargs) == 0:
                meta.doc.SetActiveObject(meta.doc.SearchObject(args[0]), meta.SELECTION_NEW)
            return meta.doc.GetActiveObject().GetName()

        if getattr(meta, "knob", False):
            if len(args) == 0 and len(kwargs) == 0:
                return node.selected
            else:
                return meta.toNode(self.name).setSelected()

        if getattr(meta, "fusion", False):
            return meta.fusion.GetCurrentComp().CurrentFrame.FlowView.Select(
                *args, **kwargs
            )

        if getattr(meta, "doc", False):
            if len(args) == 0 and len(kwargs) == 0:
                return node.selected
            else:
                try:
                    return setattr(
                        meta.doc, "ActiveLayer", meta.doc.artLayers[self.name],
                    )
                except TypeError:
                    return meta.doc.currentLayer().setTo_(meta.ps.Document().layers[self.name])

        if getattr(meta, "uclass", False):
            uname = meta.ue4.uname(self.name)
            if len(args) == 0 and len(kwargs) == 0:
                if type(uname) == str:
                    return node.selected
                else:
                    return (
                        Node(asset.get_name())
                        for asset in meta.editor.get_selection_set()
                    )
            else:
                if type(uname) == str:
                    return
                else:
                    return meta.editor.set_actor_selection_state(uname, *args)

        if getattr(meta, "Debug", False):
            if len(args) == 0 and len(kwargs) == 0:
                return node.selected
            else:
                return setattr(
                    meta.editor.Selection.activeGameObject,
                    meta.engine.GameObject.Find(*args)
                )

        if getattr(meta, "BVH3", False):
            if len(args) == 0 and len(kwargs) == 0:
                return node.selected
            else:
                return meta.select(*args, **kwargs)

        if getattr(meta, "SceneObject", False):
            return node.selected

    @trace
    def hide(self, on=True):
        if getattr(meta, "data", False):
            return setattr(meta.data.objects[self.name], "hide_viewport", on)

        if getattr(meta, "runtime", False):
            return getattr(meta.runtime, "hide" if on else "unhide")(
                meta.runtime.getnodebyname(self.name)
            )

        if getattr(meta, "C4DAtom", False):
            return setattr(
                meta.doc.SearchObject(self.item)[meta.ID_BASEOBJECT_VISIBILITY_EDITOR], on)

        if getattr(meta, "fusion", False):
            return (
                meta.fusion.GetCurrentComp()
                    .FindTool(self.name)
                    .SetAttrs({"TOOLB_Visible": on, "TOOLB_Locked": True})
            )

        if getattr(meta, "doc", False):
            try:
                return setattr(meta.doc.layers[self.name], "visible", not on)
            except TypeError:
                return meta.ps.Document().layers[self.name].setValue_forKey_(not on, "visible")

        if getattr(meta, "uclass", False):
            return meta.ue4.uname(self.name).root_component.set_editor_property(
                "visible", not on
            )

        if getattr(meta, "Debug", False):
            return meta.engine.GameObject.Find(self.name).SetActive(not on)

        if getattr(meta, "BVH3", False):
            import rumbapy
            node = meta.active_document().find_first(self.name)
            return rumbapy.hide([node]) if on else rumbapy.show_([node])

        if getattr(meta, "SceneObject", False):
            return setattr(meta.findObject(self.name), "visible", not on)

    @trace
    def parent(self, *args, **kwarg):
        if getattr(meta, "SDNode", False):
            nodes = []
            for prop in self._inputs:
                for connect in meta.graph.getNodeFromId(
                        self.name
                ).getPropertyConnections(prop):
                    nodes.append(Node(connect.getInputPropertyNode().getIdentifier()))
            return nodes

        if getattr(meta, "getAttr", False):
            if len(args) == 0 and len(kwarg) > 0:
                return meta.parent(self.item, *args, **kwarg)
            else:
                return Node(
                    partial(meta.listRelatives, self.item, p=1)(*args, **kwarg)
                )

        if getattr(meta, "hda", False):
            return Node(meta.node(self.item).parent().path())

        if getattr(meta, "runtime", False):
            if len(args) > 0:
                meta.runtime.getnodebyname(self.item).parent = args[0]
                return Node(args[0])
            else:
                _parent = meta.runtime.getnodebyname(self.item).parent
                return Node(_parent.name) if _parent else None

        if getattr(meta, "data", False):
            if len(args) > 0:
                return setattr(meta.data.objects[self.item], "parent", meta.data.objects[args[0]])
            else:
                return Object(meta.data.objects[self.item].parent.name)

        # https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/c4d.documents/BaseDocument/index.html?highlight=getactiveobject#BaseDocument.GetObjects
        if getattr(meta, "C4DAtom", False):
            return meta.doc.SearchObject(self.name)

        if getattr(meta, "knob", False):
            index = meta.toNode(self.name).inputs() - 1
            return Node(meta.toNode(self.name).input(index).name())

        if getattr(meta, "fusion", False):
            return meta.fusion.GetCurrentComp().FindTool(self.name).ParentTool

        if getattr(meta, "doc", False):
            return Node(meta.doc.artLayers[self.name].parent.name)

        if getattr(meta, "uclass", False):
            return Node(meta.ue4.uname(self.name).get_parent_actor().get_name())

        if getattr(meta, "Debug", False):
            transform = meta.engine.GameObject.Find(self.name).transform
            if len(args) > 0:
                parent = meta.engine.GameObject.Find(args[0]).transform
                meta.editor.Undo.SetTransformParent(transform, parent, "%s Parenting" % transform.name)
                return Object(parent.name)
            else:
                return Object(transform.parent.name) if transform.parent else None

        if getattr(meta, "BVH3", False):
            node = meta.active_document().find_first(self.name)
            return Node(node.parent().name())

        if getattr(meta, "SceneObject", False):
            return Object(meta.findObject(self.name).parent.name)

    @trace
    def children(self, *args, **kwarg):
        if getattr(meta, "SDNode", False):
            nodes = []
            for prop in self._outputs:
                for connect in meta.graph.getNodeFromId(
                        self.name
                ).getPropertyConnections(prop):
                    nodes.append(Node(connect.getOutputPropertyNode().getIdentifier()))
            return nodes

        if getattr(meta, "getAttr", False):
            return partial(meta.listRelatives, self.item, c=1)(*args, **kwarg) or None

        if getattr(meta, "hda", False):
            return [Node(node.name) for node in meta.node(self.item).children()]

        if getattr(meta, "runtime", False):
            if len(args) > 0:
                meta.eval("append $%s.children $%s" % (self.item, args[0]))
                return Object(args[0])
            else:
                nodes = []
                children = meta.runtime.getnodebyname(self.item).children
                for i in range(children.count):
                    nodes.append(children[i].name)
                return [Object(node.name) for node in nodes]

        if getattr(meta, "data", False):
            children = []
            for obj in meta.data.objects:
                if obj.parent == meta.data.objects[self.item]:
                    children.append(obj)
            return [Object(obj.name) for obj in children]

        if getattr(meta, "C4DAtom", False):
            return meta.doc.SearchObject(self.item)

        if getattr(meta, "doc", False):
            return [
                Object(layer.name)
                for layer in meta.doc.LayerSets[self.item].layers
            ]

        if getattr(meta, "uclass", False):
            return (
                Node(actor.get_name())
                for actor in meta.ue4.uname(self.item).get_all_child_actors()
            )

        if getattr(meta, "Debug", False):
            transform = meta.engine.GameObject.Find(self.item).transform
            return (Object(transform.GetChild(i).name) for i in range(transform.childCount))

        if getattr(meta, "BVH3", False):
            node = meta.active_document().find_first(self.name)
            return (Node(n.name()) for n in node.children())

        if getattr(meta, "SceneObject", False):
            return (Object(obj.name) for obj in meta.findObject(self.name).getChildren())


class Node(Object):
    """relationship object"""

    def __init__(self, item=None):
        super(Node, self).__init__(item)
        self.item = item
        if self.item and getattr(meta, "SDNode", False):
            self._inputs = meta.graph.getNodeFromId(self.name).getProperties(meta.sd.SDPropertyCategory.Input)
            self._outputs = meta.graph.getNodeFromId(self.name).getProperties(meta.sd.SDPropertyCategory.Output)

    @trace
    def connect(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            args = (args[0], meta.graph.getNodeFromId(args[1].id), args[2])
            return (
                meta.graph.getNodeFromId(self.name)
                    .newPropertyConnectionFromId(*args)
                    .getClassName()
            )

        if getattr(meta, "connectAttr"):
            return partial(meta.connectAttr, self.name + "." + args[0])(
                args[1:], **kwargs
            )

        if getattr(meta, "hda", False):
            return partial(meta.node(self.name).setInput, 0)(*args, **kwargs)

        if getattr(meta, "knob", False):
            return meta.toNode(self.name).setInput(*args, **kwargs)

        if getattr(meta, "fusion", False):
            return (
                meta.fusion.GetCurrentComp()
                    .FindTool(self.name)
                    .ConnectInput(*args, **kwargs)
            )

        if getattr(meta, "BVH3", False):
            node = meta.active_document().first_name(self.name)
            return node.plug(args[0]).connect(*args[1:], **kwargs)

    @trace
    def disconnect(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            for arg in args:
                for prop in self._inputs:
                    if arg == prop.getId():
                        return meta.graph.getNodeFromId(
                            self.name
                        ).deletePropertyConnections(prop)
                for prop in self._outputs:
                    if arg == prop.getId():
                        return meta.graph.getNodeFromId(
                            self.name
                        ).deletePropertyConnections(prop)
            return

        if hasattr(meta, "disconnectAttr"):
            return partial(meta.disconnectAttr, self.name + "." + args[0])(
                args[1:], **kwargs
            )

        if getattr(meta, "hda", False):
            return partial(meta.node(self.name).setInput, 0, None)(*args, **kwargs)

        if getattr(meta, "knob", False):
            return meta.toNode(self.name).setInput(0, None)

        if getattr(meta, "fusion", False):
            return setattr(
                meta.fusion.GetCurrentComp().FindTool(self.name), "Input", None
            )

        if getattr(meta, "BVH3", False):
            node = meta.active_document().first_name(self.name)
            return node.plug(args[0]).disconnect(True)

    @trace
    def inputs(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            return [
                connect.getId() for connect in self._inputs if connect.isConnectable()
            ]

        if hasattr(meta, "listConnections"):
            return partial(meta.listConnections, s=1)(*args, **kwargs)

        if getattr(meta, "hda", False):
            return [Node(node.name) for node in meta.node(self.name).inputs()]

        if getattr(meta, "knob", False):
            return [
                Node(meta.toNode(self.name).input(index).name())
                for index in range(meta.toNode(self.name).inputs())
            ]

        if getattr(meta, "fusion", False):
            return (
                meta.fusion.GetCurrentComp()
                    .FindTool(self.name)
                    .GetInputList()
                    .values()[0]
                    .GetAttrs()
            )

        if getattr(meta, "BVH3", False):
            node = meta.active_document().first_name(self.name)
            return Node(node.plug(args[0]).input().node().name())

    @trace
    def outputs(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            return [
                connect.getId() for connect in self._outputs if connect.isConnectable()
            ]

        if hasattr(meta, "listConnections"):
            return partial(meta.listConnections, d=1)(*args, **kwargs)

        if getattr(meta, "hda", False):
            return [Node(node.name) for node in meta.node(self.name).outputs()]

        if getattr(meta, "knob", False):
            return meta.toNode(self.name).dependencies(meta.EXPRESSIONS)

        if getattr(meta, "fusion", False):
            return (
                meta.fusion.GetCurrentComp()
                    .FindTool(self.name)
                    .GetOutputList()
                    .values()[0]
                    .GetAttrs()
            )

        if getattr(meta, "BVH3", False):
            node = meta.active_document().first_name(self.name)
            return [Node(out.name()) for out in node.plug(args[0]).outputs()]


@total_ordering
class Attribute(_YAttr):
    """parametric object"""

    def __init__(self, *args):
        assert len(args) > 2, "parameter is invalid."
        self._values = args
        self.obj, self.val = self._values[1:]

    def __getitem__(self, idx):
        return self._values[idx]

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value >= other.value

    @trace
    def __call__(self, *args, **kwargs):
        """
        helper method for set

        Args:
            *args:
            **kwargs:

        Returns:

        """
        self.set(*args, **kwargs)

    @property
    def value(self):
        if getattr(meta, "SDNode", False):
            return self._values[0]

        if getattr(meta, "Debug", False):
            return getattr(self._values[0], self.val)

        if getattr(meta, "BVH3", False):
            return self._values[0].value()

        if ":" in str(self._values[0]):
            try:
                return getattr(self._values[0], self.val)
            except AttributeError:
                return self._values[0]()
        else:
            return self._values[0]

    @trace
    def set(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            sd_value = meta.SDValueInt.sNew(args[0])

            if type(self.value) == bool:
                sd_value = meta.SDValueBool.sNew(args[0])
            if type(self.value) == float:
                sd_value = meta.SDValueFloat.sNew(args[0])
            if type(self.value) == str:
                sd_value = meta.SDValueString.sNew(args[0])

            prop = meta.graph.getNodeFromId(self.obj).getPropertyFromId(
                self.val, meta.sd.SDPropertyCategory.Input
            )
            return meta.graph.getNodeFromId(self.obj).setPropertyValue(prop, sd_value)

        if getattr(meta, "setAttr", False):
            return meta.setAttr(
                self.obj + "." + self.val, *args, **kwargs)

        if getattr(meta, "hda", False):
            parm = meta.node(self.obj).parm(self.val) or meta.node(self.obj).parmTuple(
                self.val
            )
            return parm.set(
                args[0].tolist() if hasattr(args[0], "T") else args[0], **kwargs
            )

        if getattr(meta, "runtime", False):
            if ":" in str(self._values[0]):
                return setattr(self._values[0], self.val, args[0])
            else:
                return setattr(meta.runtime.getnodebyname(self.obj), self.val, args[0])

        if getattr(meta, "data", False):
            return setattr(
                meta.data.objects[self.obj],
                self.val,
                args[0].tolist() if hasattr(args[0], "T") else args,
            )

        if getattr(meta, "C4DAtom", False):
            meta.doc.SearchObject(self.obj)[getattr(meta, self.val)] = args[0]
            return args[0]

        if getattr(meta, "knob", False):
            return meta.toNode(self.obj)[self.val].setValue(
                args[0], **kwargs
            )

        if getattr(meta, "fusion", False):
            return setattr(
                meta.fusion.GetCurrentComp().FindTool(self.obj), self.val, args[0])

        if getattr(meta, "doc", False):
            try:
                return getattr(meta.doc.layers[self.obj], self.val)(*args, **kwargs)
            except TypeError:
                try:
                    return setattr(
                        meta.doc.layers[self.obj], self.val, args[0]
                    )
                except TypeError:
                    return meta.ps.Document().layers[self.obj].setValue_forKey_(args[0], self.val)

        if getattr(meta, "uclass", False):
            try:
                return meta.ue4.uname(self.obj).set_editor_property(self.val, args[0])
            except TypeError:
                return getattr(meta.ue4.uname(self.obj), self.val)(*args, **kwargs)
            except:
                return meta.ue4.uname(self.obj).root_component.set_editor_property(
                    self.val, args[0]
                )

        if getattr(meta, "Debug", False):
            go = meta.engine.GameObject.Find(self.obj)
            meta.editor.Undo.RecordObject(go, "Inspector")

            for com in go.GetComponentsInChildren(meta.engine.Component):
                if self.val in dir(go.GetComponent(com.GetType())):
                    return setattr(go.GetComponent(com.GetType()), self.val, args[0])

        if getattr(meta, "BVH3", False):
            node = meta.active_document().first_name(self.obj)
            return node.plug(self.val).set_value(args[0], True)

        if getattr(meta, "SceneObject", False):
            return setattr(meta.findObject(self.val), "", args[0])

        if getattr(meta, "textureset", False):
            return

    @trace
    def create(self):
        """create attribute"""

    @trace
    def delete(self):
        """delete attribute"""

    @trace
    def lock(self, on):
        if getattr(meta, "setAttr", False):
            return meta.setAttr(self.obj + "." + self.val, lock=on)

        if getattr(meta, "hda", False):
            return meta.node(self.obj).parm(self.val).lock(on)

        if getattr(meta, "knob", False):
            return meta.toNode(self.obj)[self.val].setEnabled(on)

        if getattr(meta, "data", False):
            return setattr(meta.data.objects[self.obj], "lock_" + self.val, on)

        if getattr(meta, "BVH3", False):
            return self._values[0].lock.set_value(on)

        if getattr(meta, "SceneObject", False):
            return

    @trace
    def hide(self, on=True):
        if getattr(meta, "setAttr", False):
            return meta.setAttr(
                self.obj + "." + self.val, keyable=not on, channelBox=not on
            )

        if getattr(meta, "hda", False):
            return meta.node(self.obj).parm(self.val).hide(on)

        if getattr(meta, "knob", False):
            return meta.toNode(self.obj)[self.val].setVisible(not on)

        if getattr(meta, "BVH3", False):
            return self._values[0].visible.set_value(not on)

        if getattr(meta, "SceneObject", False):
            return

    @property
    def vector(self):
        try:
            return Vector(self._values[0])
        except TypeError:
            return Vector(*self._values[0])

    @property
    def color(self):
        try:
            return Color(self._values[0])
        except TypeError:
            return Color(*self._values[0])

    @property
    def matrix(self):
        try:
            return Matrix(self._values[0])
        except TypeError:
            return Matrix(*self._values[0])


class File(_YObject):
    """save, open and export"""
    abc, fbx, usd, gltf = None, None, None, None

    def __init__(self, path=""):
        self.file = path if path else self.current

    @property
    def name(self):
        if getattr(meta, "data", False):
            return meta.path.basename(self.file)
        else:
            return os.path.basename(self.file)

    @property
    def path(self):
        return os.path.dirname(self.file)

    @classmethod
    def open(cls, *args, **kwargs):
        from yurlungur.core.command import file

        if args[0].endswith("abc"):
            return cls(file.abc.Importer(*args, **kwargs))

        if args[0].endswith("fbx"):
            return cls(file.fbx.Importer(*args, **kwargs))

        if args[0].endswith("usd"):
            return cls(file.usd.Importer(*args, **kwargs))

        if getattr(meta, "sbs", False):
            return cls(meta.manager.loadUserPackage(*args, **kwargs))

        if getattr(meta, "doc", False):
            return meta.Open(*args, **kwargs)

        if getattr(meta, "setAttr", False):
            return cls(partial(meta.file, i=1)(*args, **kwargs))

        if getattr(meta, "hipFile", False):
            return cls(meta.hipFile.load(*args, **kwargs))

        if getattr(meta, "runtime", False):
            if meta.runtime.loadMaxFile(*args, **kwargs):
                return cls(args[0])

        if getattr(meta, "data", False):
            return partial(meta.ops.wm.open_mainfile, filepath=args[0])(**kwargs)

        if getattr(meta, "C4DAtom", False):
            meta.documents.LoadFile(*args)
            return cls(args[0])

        if getattr(meta, "knob", False):
            return meta.scriptOpen(*args, **kwargs)

        if getattr(meta, "fusion", False):
            storage = meta.resolve.GetMediaStorage()
            if "." in args:
                return storage.AddItemsToMediaPool(*args)
            else:
                return meta.manager.LoadProject(*args, **kwargs)

        if getattr(meta, "uclass", False):
            return cls(file.abcImporter(*args, **kwargs))

        if getattr(meta, "Debug", False):
            return cls(meta.editor.AssetDatabase.ImportAsset(*args, **kwargs))

        if getattr(meta, "BVH3", False):
            return meta.load_document(*args, **kwargs)

        if getattr(meta, "SceneObject", False):
            return meta.loadScene(*args)

        if getattr(meta, "textureset", False):
            if args[0].endswith(".spp"):
                return meta.project.open(*args)
            else:
                return meta.project.create(*args, **kwargs)

    @classmethod
    def save(cls, *args, **kwargs):
        from yurlungur.core.command import file

        if args[0].endswith("abc"):
            return cls(file.abc.Exporter(*args, **kwargs))

        if args[0].endswith("fbx"):
            return cls(file.fbx.Exporter(*args, **kwargs))

        if args[0].endswith("usd"):
            return cls(file.usd.Exporter(*args, **kwargs))

        if args[0].endswith("gltf"):
            return cls(file.gltf.Exporter(*args, **kwargs))

        if getattr(meta, "sbs", False):
            return cls(meta.manager.savePackageAs(*args, **kwargs))

        if getattr(meta, "doc", False):
            if args[0].endswith(".psd"):
                return meta.doc.Save()
            else:
                return meta.doc.SaveAs(*args, **kwargs)

        if getattr(meta, "setAttr", False):
            return cls(partial(meta.file, s=1)(*args, **kwargs))

        if getattr(meta, "hipFile", False):
            return cls(meta.hipFile.save(*args, **kwargs))

        if getattr(meta, "runtime", False):
            if meta.runtime.saveMaxFile(*args, **kwargs):
                return cls(args[0])

        if getattr(meta, "data", False):
            return partial(meta.ops.wm.save_mainfile, filepath=args[0])(**kwargs)

        if getattr(meta, "C4DAtom", False):
            meta.documents.SaveDocument(
                meta.doc, args[0], meta.SAVEDOCUMENTFLAGS_NONE, meta.FORMAT_C4DEXPORT
            )
            return cls(args[0])

        if getattr(meta, "knob", False):
            return meta.scriptSave(*args, **kwargs)

        if getattr(meta, "fusion", False):
            return meta.manager.SaveProject(*args, **kwargs)

        if getattr(meta, "uclass", False):
            return meta.tools.export_assets(*args, **kwargs)

        if getattr(meta, "Debug", False):
            return

        if getattr(meta, "BVH3", False):
            doc = meta.active_document()
            return doc.write(*args, **kwargs)

        if getattr(meta, "SceneObject", False):
            return meta.saveScene(*args)

        if getattr(meta, "textureset", False):
            if args[0].endswith(".spp"):
                return meta.project.save_as(*args, **kwargs)
            else:
                return meta.export.export_project_textures(**kwargs)

    @property
    def current(self):
        if getattr(meta, "sbs", False):
            return meta.manager.getUserPackageFromFilePath()

        if getattr(meta, "doc", False):
            try:
                return os.path.join(meta.doc.path, meta.doc.name)
            except AttributeError:
                path = meta.doc.filePath()
                if path:
                    return path.absoluteString()
                return

        if getattr(meta, "setAttr", False):
            return meta.file(exn=1, q=1)

        if getattr(meta, "hipFile", False):
            return meta.hipFile.path()

        if getattr(meta, "runtime", False):
            return meta.runtime.maxFilePath + meta.runtime.maxFileName

        if getattr(meta, "data", False):
            return meta.data.filepath

        if getattr(meta, "C4DAtom", False):
            return meta.doc.GetDocumentPath() + meta.doc.GetDocumentName()

        if getattr(meta, "knob", False):
            return meta.scriptName()

        if getattr(meta, "fusion", False):
            return meta.manager.GetCurrentProject()

        if getattr(meta, "uclass", False):
            if self.path:
                return meta.assets.find_asset_data(self.path).package_path
            else:
                return meta.assets.list_assets(
                    "/Game", recursive=True, include_folder=True)

        if getattr(meta, "Debug", False):
            return meta.editor.AssetDatabase.GetAssetOrScenePath()

        if getattr(meta, "BVH3", False):
            return meta.active_document().full_document_name() + meta.active_document_filename()

        if getattr(meta, "SceneObject", False):
            return meta.getScenePath()

        if getattr(meta, "textureset", False):
            return meta.project.file_path()
