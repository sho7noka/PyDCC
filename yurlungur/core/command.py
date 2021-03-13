# -*- coding: utf-8 -*-
import fnmatch
import types
import importlib
from functools import partial, wraps

from yurlungur.core.proxy import Node, Attribute, File
from yurlungur.tool.meta import meta

__all__ = [
    "cmd", "node", "attr", "file"
]

u"""
node ベースのアプリだとコマンド化されずに
まとまったAPIで読み込みを行う必要があるので
ここでコマンドにしておく

runtimecommand 化
"""

_CMDS_ = {}


class Command(object):
    """
    >>> def pydef1():
    >>>     return True
    >>> Command.register(pydef1)
    >>> # or
    >>> @Command.register
    >>> def pydef2():
    >>>     return False
    >>> # result
    >>> yurlungur.cmd.pydef1()
    """

    def __getattr__(self, item):
        return _CMDS_[item]

    # @wraps(func)
    @staticmethod
    def register(func):
        p = partial(meta.eval, func)
        m = types.ModuleType(func)
        if _CMDS_.has_key(func):
            _CMDS_.update(func, p)  # cmd.func()
        else:
            _CMDS_.update(func, m)  # cmd.func

    @classmethod
    def list(cls):
        return [obj for obj in dir(cls) if not obj.startswith("_")]

    @staticmethod
    def unregister():
        _CMDS_.clear()


# Monkey-Patch for attribute
attr = Attribute()
Attribute.create = None
Attribute.delete = None


def _rm(cls, *args):
    for obj in args:
        try:
            node = cls(obj.name)
            node.delete()
        except:
            pass


def _ls(cls, *args, **kwargs):
    gen = []
    if getattr(meta, "SDNode", False):
        return
    if getattr(meta, "ls", False):
        gen = meta.ls(*args, **kwargs)
    if getattr(meta, "hda", False):
        gen = meta.pwd().allItems()
    if getattr(meta, "data", False):
        return
    if getattr(meta, "uclass", False):
        return
    if getattr(meta, "Debug", False):
        return
    if getattr(meta, "knob", False):
        return
    if getattr(meta, "C4DAtom", False):
        return
    if getattr(meta, "fusion", False):
        return
    if getattr(meta, "runtime", False):
        gen = meta.runtime.objects
    if getattr(meta, "BVH3", False):
        return
    if getattr(meta, "doc", False):
        return
    if getattr(meta, "SceneObject", False):
        gen = meta.getAllObjects()
    if getattr(meta, "textureset", False):
        return
    return (cls(obj) for obj in gen)


def _glob(cls, *args, **kwargs):
    if getattr(meta, "SDNode", False):
        return
    if getattr(meta, "ls", False):
        gen = meta.ls(*args, **kwargs)
    if getattr(meta, "hda", False):
        gen = meta.pwd().glob(*args, **kwargs)
    if getattr(meta, "data", False):
        return
    if getattr(meta, "uclass", False):
        return
    if getattr(meta, "Debug", False):
        return
    if getattr(meta, "knob", False):
        return
    if getattr(meta, "C4DAtom", False):
        return
    if getattr(meta, "fusion", False):
        gen = meta.fusion.GetCurrentComp().GetToolList(*args)
    if getattr(meta, "runtime", False):
        gen = meta.runtime.objects
    if getattr(meta, "BVH3", False):
        return
    if getattr(meta, "doc", False):
        return
    if getattr(meta, "SceneObject", False):
        return
    if getattr(meta, "textureset", False):
        return
    return tuple(cls(obj) for obj in gen)


def _select(cls, *args, **kwargs):
    if getattr(meta, "select", False):
        return (cls(obj) for obj in meta.ls(sl=True))

    if getattr(meta, "hda", False):
        return (cls(obj.path()) for obj in meta.selectedNodes(args))

    if getattr(meta, "SDNode", False):
        context = meta.sd_app.getUIMgr()
        return (
            cls(node.getDefinition().getLabel())
            for node in context.getCurrentGraphSelection()
        )

    if getattr(meta, "runtime", False):
        if meta.runtime.execute("$") == meta.runtime.execute("$selection", False):
            return (cls(obj.name) for obj in meta.runtime.execute("$ as array"))
        else:
            return cls(meta.runtime.execute("$"))

    if getattr(meta, "data", False):
        return (cls(obj.name) for obj in meta.context.selected_objects)

    if getattr(meta, "C4DAtom", False):
        if len(args) == 0 and len(kwargs) == 0:
            meta.doc.SetActiveObject(meta.doc.SearchObject(args[0]), meta.SELECTION_NEW)
        return meta.doc.GetActiveObject().GetName()

    if getattr(meta, "knob", False):
        return (cls(node.name) for node in meta.selectedNodes())

    if getattr(meta, "doc", False):
        try:
            return cls(meta.doc.ActiveLayer.name)
        except AttributeError:
            return cls(meta.doc.currentLayer().name())

    if getattr(meta, "uclass", False):
        return (
            cls(asset.get_name())
            for asset in meta.editor.get_selected_assets()
        )

    if getattr(meta, "Debug", False):
        return (cls(go.name) for go in meta.editor.Selection.gameObjects)

    if getattr(meta, "BVH3", False):
        return (cls(node.name()) for node in meta.selection())

    if getattr(meta, "SceneObject", False):
        return (cls(obj.name) for obj in meta.getSelectedObjects())


def _abcImporter(cls, *args, **kwargs):
    if getattr(meta, "AbcImport", False):
        return cls(meta.AbcImport(*args, **kwargs))

    if getattr(meta, "runtime", False):
        importer = partial(
            meta.runtime.importFile, args[0], meta.runtime.Name("noPrompt"),
            using='AlembicImport'
        )
        if importer(**kwargs):
            return args[0]

    if getattr(meta, 'uclass', False):
        data = meta.AutomatedAssetImportData()
        data.set_editor_property('filenames', *args)
        for k, v in kwargs:
            data.set_editor_property(k, v)
        return meta.tools.import_assets_automated(data)

    if getattr(meta, "SceneObject", False):
        return meta.importModel(args[0])

    if getattr(meta, "textureset", False):
        return meta.project.create(*args, **kwargs)


def _abcExporter(cls, *args, **kwargs):
    if getattr(meta, "AbcExport", False):
        return cls(meta.AbcExport(*args, **kwargs))

    if getattr(meta, "runtime", False):
        export = partial(
            meta.runtime.exportFile, args[0], meta.runtime.Name("noPrompt"),
            using='AlembicExport'
        )
        if export(**kwargs):
            return args[0]

    if getattr(meta, "data", False):
        return cls(meta.export(*args))

    if getattr(meta, "BVH3", False):
        import rumba_alembic, rumbapy

        with rumbapy.Progress("Exporting animation...") as progress:
            export = partial(rumba_alembic.export_nodes, progress=progress.update)
            export(*args, **kwargs)
        return


def _fbxImporter(cls, *args, **kwargs):
    """
    3dsMax    Python3 / FBX/Alembic
    Davinci   Python3 / FBX/Alembic
    Painter   Python3 / FBX
    Marmoset  Python3 / FBX
    Args:
        cls:
        *args:
        **kwargs:

    Returns:

    """
    if getattr(meta, 'eval', False):
        return cls(meta.eval("FBXImport -file {0};".format(*args)))

    if getattr(meta, "runtime", False):
        importer = partial(
            meta.runtime.importFile, args[0], meta.runtime.Name("noPrompt"),
            using='FBXIMPORTER'
        )
        if importer(**kwargs):
            return args[0]

    if getattr(meta, "data", False):
        return cls(partial(meta.export, file_type=args[0])(*args[1:]))

    if getattr(meta, 'uclass', False):
        data = meta.AutomatedAssetImportData()
        data.set_editor_property('filenames', *args)
        for k, v in kwargs:
            data.set_editor_property(k, v)
        factory = meta.FbxSceneImportFactory()
        return data.set_editor_property('factory', factory)

        meta.tools.import_assets_automated(data)

    if getattr(meta, 'Debug', False):
        return

    if getattr(meta, "knob", False):
        return cls(args[0]) or Node(im.Name)

    if getattr(meta, "C4DAtom", False):
        return

    if getattr(meta, "fusion", False):
        # fu:ToggleUtility('FBXImport')
        meta.fusion.GetCurrentComp().Lock()
        im = meta.fusion.GetCurrentComp().AddTool("SurfaceFBXMesh")
        im.ImportFile = args[0]
        meta.fusion.GetCurrentComp().Unlock()
        return cls(args[0]) or Node(im.Name)

    # ---

    if getattr(meta, "textureset", False):
        # from yurlungur.adapters import substance_painter
        # substance_painter.shell(["--mesh", args[0], "--export-path", exportPath].join(" "))
        return meta.project.create(*args, **kwargs)

    if getattr(meta, "SceneObject", False):
        return meta.importModel(args[0])


def _fbxExporter(cls, *args, **kwargs):
    """
    Maya      Python2 / FBX/Alembic
    Rumba     Python2 / FBX/Alembic
    Args:
        cls:
        *args:
        **kwargs:

    Returns:

    """
    if getattr(meta, 'eval', False):
        return cls(meta.eval("FBXExportInAscii -v true; FBXExport -f \"{}\" -s;".format(*args)))

    if getattr(meta, "runtime", False):
        export = partial(
            meta.runtime.exportFile, args[0], meta.runtime.Name("noPrompt"),
            using='FBXEXPORTER'
        )
        if export(**kwargs):
            return args[0]

    if getattr(meta, "data", False):
        return cls(meta.export(*args))

    if getattr(meta, 'uclass', False):
        return

    if getattr(meta, 'Debug', False):
        return

    if getattr(meta, "knob", False):
        ex = meta.createNode("WriteGeo")
        return cls(args[0]) or Node(ex.Name)

    if getattr(meta, "fusion", False):
        meta.fusion.GetCurrentComp().Lock()
        ex = meta.fusion.GetCurrentComp().AddTool("ExporterFBX")
        ex.Filename = args[0]
        meta.eval("comp:Render({Tool = comp.%s})" % ex.Name)
        meta.fusion.GetCurrentComp().Unlock()
        return cls(args[0]) or Node(ex.Name)

    if getattr(meta, "C4DAtom", False):
        ExportId = 1026370
        plug = meta.plugins.FindPlugin(ExportId, meta.PLUGINTYPE_SCENESAVER)
        data = dict()
        plug.Message(meta.MSG_RETRIEVEPRIVATEDATA, data)

        fbxExport = data.get("imexporter", None)
        fbxExport[meta.FBXEXPORT_CAMERAS] = True
        fbxExport[meta.FBXEXPORT_LIGHTS] = True
        fbxExport[meta.FBXEXPORT_SPLINES] = True
        fbxExport[meta.FBXEXPORT_INSTANCES] = True

        meta.documents.SaveDocument(meta.documents.GetActiveDocument(), args[0],
                                    meta.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, ExportId)

    if getattr(meta, "textureset", False):
        kwargs["exportPath"] = args[0]
        export_preset = meta.resource.ResourceID(
            context="allegorithmic",
            name="USD PBR Metal Roughness")
        kwargs["defaultExportPreset"] = export_preset.url()
        return meta.export.export_project_textures(**kwargs)

    if getattr(meta, "BVH3", False):
        import fbx, rumbapy
        with rumbapy.Progress("Exporting animation...") as progress:
            fbx.export_nodes(args[0], [], [], False, True, progress.update)
        return


def _usdImporter(cls, *args, **kwargs):
    """
    Maya      Python2 / USD InOut(plugin)
    Houdini   Python3 / USD InOut
    Blender   Python3 / USD Out
    Unreal    Python3 / USD InOut
    Unity     Python2 / USD InOut(plugin)
    Nuke      Python2 / USD In
    Cinema4D  Python3 / USD InOut
    Painter   Python3 / USD Out
    """
    if getattr(meta, "mayaUSDImport", False):
        meta.loadPlugin('mayaUsdPlugin')
        obj = meta.mayaUSDImport(file=args[0], chaser=['info'])
        return cls(obj[0])

    if getattr(meta, "hda", False):
        usd = meta.node('/obj/lopimport1').createNode("usdimport")
        usd.parm("filepath1").set(args[0])
        usd.parm("reload").pressButton()
        return cls(args[0]) or Node(usd.name)

    if getattr(meta, "uclass", False):
        data = meta.AutomatedAssetImportData()
        data.set_editor_property('filenames', *args)
        for k, v in kwargs:
            data.set_editor_property(k, v)
        factory = meta.UUSDSceneImportFactory()
        data.set_editor_property('factory', factory)
        return meta.tools.import_assets_automated(data)

    if getattr(meta, "Debug", False):
        return

    # https://community.foundry.com/discuss/topic/153415/extend-active-scenegraph?mode=Post&postID=1205506
    if getattr(meta, "knob", False):
        geo = meta.createNode("ReadGeo")
        # TODO: scenegraph tab?
        geo["file"].setValue(args[0])
        geo["reload"].execute()
        return cls(args[0]) or Node(geo.name)

    if getattr(meta, "C4DAtom", False):
        ImportId = 1055178
        plug = meta.plugins.FindPlugin(ImportId, meta.PLUGINTYPE_SCENELOADER)
        data = dict()
        plug.Message(meta.MSG_RETRIEVEPRIVATEDATA, data)

        usdImport = data.get("imexporter", None)
        usdImport[meta.USDIMPORTER_KEEPBRIDGEOPEN] = True
        usdImport[meta.USDIMPORTER_CAMERAS] = True
        usdImport[meta.USDIMPORTER_LIGHTS] = True
        usdImport[meta.USDIMPORTER_GEOMETRY] = True
        usdImport[
            meta.USDIMPORTER_NORMALS] = meta.USDIMPORTER_NORMALS_PHONG  # USDIMPORTER_NORMALS_NONE / USDIMPORTER_NORMALS_VERTEX
        usdImport[meta.USDIMPORTER_PHONG_ANGLE] = 40
        usdImport[meta.USDIMPORTER_UV] = True
        usdImport[meta.USDIMPORTER_DISPLAYCOLOR] = True

        meta.documents.MergeDocument(meta.documents.GetActiveDocument(), args[0],
                                     meta.SCENEFILTER_OBJECTS | meta.SCENEFILTER_MATERIALS, None)
        meta.EventAdd()
        return cls(args[0])


def _usdExporter(cls, *args, **kwargs):
    if getattr(meta, "mayaUSDExport", False):
        meta.loadPlugin('mayaUsdPlugin')
        meta.mayaUSDExport(
            file=args[0],
            chaser=['alembic'],
            chaserArgs=[
                ('alembic', 'primvarprefix', 'ABC_,ABC2_=customPrefix_,ABC3_=,ABC4_=customNamespace:'),
            ])
        return cls(args[0])

    if getattr(meta, "hda", False):
        usd = meta.node("/obj/lopimport1").createNode("usdexport")
        usd.parm('lopoutput').set(args[0])
        usd.parm('execute').pressButton()
        return cls(args[0]) or Node(usd.name)

    if getattr(meta, "data", False):
        return cls(partial(meta.ops.wm.save_mainfile, filepath=args[0])(**kwargs))

    if getattr(meta, "uclass", False):
        return

    if getattr(meta, "Debug", False):
        return

    if getattr(meta, "C4DAtom", False):
        usdExportId = 1055179
        plug = meta.plugins.FindPlugin(usdExportId, meta.PLUGINTYPE_SCENESAVER)
        data = dict()
        plug.Message(meta.MSG_RETRIEVEPRIVATEDATA, data)

        usdExport = data.get("imexporter", None)
        usdExport[meta.USDEXPORTER_FILEFORMAT] = meta.USDEXPORTER_FILEFORMAT_USDC if args[0].endswith(".usdc",
                                                                                                      False) else meta.USDEXPORTER_FILEFORMAT_USDA
        usdExport[meta.USDEXPORTER_ZIP] = args[0].endswith(".usdz")
        usdExport[meta.USDEXPORTER_CAMERAS] = True
        usdExport[meta.USDEXPORTER_LIGHTS] = True
        usdExport[meta.USDEXPORTER_GEOMETRY] = True
        usdExport[meta.USDEXPORTER_NORMALS] = True
        usdExport[meta.USDEXPORTER_UV] = True
        usdExport[meta.USDEXPORTER_DISPLAYCOLOR] = True
        usdExport[meta.USDEXPORTER_VERTEXCOLORS] = True

        meta.documents.SaveDocument(meta.documents.GetActiveDocument(), args[0],
                                    meta.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, usdExportId)
        return cls(args[0])

    if getattr(meta, "textureset", False):
        kwargs["exportPath"] = args[0]
        export_preset = meta.resource.ResourceID(
            context="allegorithmic",
            name="USD PBR Metal Roughness")
        kwargs["defaultExportPreset"] = export_preset.url()
        return meta.export.export_project_textures(**kwargs)


class _NodeType(object):
    """
    >>> blur = yurlungur.node.Blur()
    >>> blur = yurlungur.Node().create("Blur")
    """

    def __getattr__(self, item):
        if getattr(meta, "types", False):
            nodes = fnmatch.filter(dir(meta.types), str(item))
        else:
            nodes = self.findNodes(item)

        for node in nodes:
            setattr(self, str(item), Node(node))

        return Node(item)

    def findNodes(self, pattern):
        if getattr(meta, "listNodeTypes", False):
            # http://help.autodesk.com/cloudhelp/2016/JPN/Maya-Tech-Docs/CommandsPython/shadingNode.html
            categories = ["geometry", "camera", "light",
                          "utility", "color", "shader",
                          "texture", "rendering", "postprocess"]

            # meta.allNodeTypes(ia=1)
            for category in categories:
                yield fnmatch.filter(meta.listNodeTypes(category), pattern)

        if getattr(meta, "hda", False):
            for category in meta.nodeTypeCategories().keys():
                yield fnmatch.filter(
                    meta.nodeTypeCategories()[category].nodeTypes().keys(),
                    pattern
                )

        if getattr(meta, "knob", False):
            yield

        if getattr(meta, "BVH3", False):
            for node in ["SceneGraphNode",
                         "AnimLayer", "AnimLayerBlend",
                         "ConstraintLayer", "EvalSurface",
                         "GetArray", "GetDict",
                         "IsoCurve", "Lerp",
                         "MakeArray", "MakeDict",
                         "MakeSparseBuffer", "Reference",
                         "RemoveAttribute", "SelectionSet", "SetAttribute",
                         "ShapeAttribute",
                         "SurfaceInfo", "TransformGeometry"]:
                yield fnmatch.filter(
                    meta.nodeTypeCategories()[category].nodeTypes().keys(),
                    pattern
                )


# Monkey-Patch for node
node = Node()
Node.ls = _ls
Node.sel = _select
Node.rm = _rm
Node.glob = _glob


def _Bake(cls, *args, **kwargs):
    """"""


# Monkey-Patch for command
cmd = Command()
Command.bake = _Bake

# Monkey-Patch for file
file = File()

fbxs = ["eval", "runtime", "data", "uclass", "Debug", "knob", "C4DAtom", "fusion", "textureset", "SceneObject"]
if any([getattr(meta, p, False) for p in fbxs]):
    File.fbx = types.ModuleType("fbx")
    File.fbx.Import = _fbxImporter
    File.fbx.Export = _fbxExporter

abcs = ["AbcImport", "runtime", "uclass", "SceneObject", "textureset", "data", "BVH3"]
if any([getattr(meta, p, False) for p in abcs]):
    File.abc = types.ModuleType("abc")
    File.abc.Import = _abcImporter
    File.abc.Export = _abcExporter

for p in "hda", "uclass", "Debug", "C4DAtom":
    if getattr(meta, p, False):
        File.usd = types.ModuleType("usd")
        File.usd.Import = _usdImporter
        File.usd.Export = _usdExporter

if getattr(meta, "knob", False):
    File.usd = types.ModuleType("usd")
    File.usd.Import = _usdImporter
if getattr(meta, "data", False):
    File.usd = types.ModuleType("usd")
    File.usd.Export = _usdExporter
