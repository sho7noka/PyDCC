# -*- coding: utf-8 -*-
import fnmatch
from functools import partial

from yurlungur.core.proxy import Node, File
from yurlungur.tool.meta import meta
from yurlungur.core.exception import YException

__all__ = [
    "file", "cmd", "node"
]


class Command(object):
    """

    """
    @staticmethod
    def register(func):
        pass

    @classmethod
    def list(cls):
        return [obj for obj in dir(cls) if not obj.startswith("_")]


def _ls(cls, *args, **kwargs):
    if hasattr(meta, "hda"):
        gen = meta.pwd().allItems()
    if hasattr(meta, "SceneObject"):
        gen = meta.getAllObjects()
    if hasattr(meta, "runtime"):
        gen = meta.runtime.objects
    if hasattr(meta, "ls"):
        gen = meta.ls(*args, **kwargs)
    return tuple(Node(obj) for obj in gen)


def _rm(cls, *args):
    for obj in args:
        Node(obj.name).delete()


def _glob(cls, *args, **kwargs):
    if hasattr(meta, "ls"):
        gen = meta.ls(*args, **kwargs)
    if hasattr(meta, "hda"):
        gen = meta.pwd().glob(*args, **kwargs)
    if hasattr(meta, "runtime"):
        gen = meta.runtime.objects
    return tuple(Node(obj) for obj in gen)


def _select(cls, *args, **kwargs):
    if getattr(meta, "select"):
        return (cls(obj) for obj in meta.ls(sl=True))

    if hasattr(meta, "hda"):
        return (cls(obj.path()) for obj in meta.selectedNodes(args))

    if getattr(meta, "SDNode", False):
        context = meta.sd_app.getUIMgr()
        return (
            cls(node.getDefinition().getLabel())
            for node in context.getCurrentGraphSelection()
        )

    if getattr(meta, "runtime", False):
        if meta.runtime.execute("$") == meta.runtime.execute("$selection"):
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
            return Node(meta.doc.ActiveLayer.name)
        except AttributeError:
            return Node(meta.doc.currentLayer().name())

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


def _alembicImporter(cls, *args, **kwargs):
    if getattr(meta, "AbcImport", False):
        return cls(meta.AbcImport(*args, **kwargs))

    if getattr(meta, "textureset", False):
        return meta.project.create(*args, **kwargs)

    if getattr(meta, "hda", False):
        geo = Node("obj").create("geo")
        abc = geo.create("alembic")
        abc.fileName.set(*args)
        return cls(*args)

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
        meta.tools.import_assets_automated(data)

    if getattr(meta, "SceneObject", False):
        return meta.importModel(args[0])


def _alembicExporter(cls, *args, **kwargs):
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
    if getattr(meta, "importFBX", False):
        return meta.importFBX(*args, **kwargs)

    if getattr(meta, "runtime", False):
        importer = partial(
            meta.runtime.importFile, args[0], meta.runtime.Name("noPrompt"),
            using='FBXIMPORTER'
        )
        if importer(**kwargs):
            return args[0]

    if getattr(meta, "data", False):
        return cls(meta.export(*args))

    # fbx, obj, dae, ply, glb, abc
    if getattr(meta, "textureset", False):
        return meta.project.create(*args, **kwargs)

    if getattr(meta, 'uclass', False):
        data = meta.AutomatedAssetImportData()
        data.set_editor_property('filenames', *args)
        for k, v in kwargs:
            data.set_editor_property(k, v)
        factory = meta.FbxSceneImportFactory()
        return data.set_editor_property('factory', factory)

        meta.tools.import_assets_automated(data)

    if getattr(meta, 'eval', False):
        return cls(meta.eval("FBXImport -file {0};".format(*args)))

    if getattr(meta, "SceneObject", False):
        return meta.importModel(args[0])


def _fbxExporter(cls, *args, **kwargs):
    if getattr(meta, "runtime", False):
        export = partial(
            meta.runtime.exportFile, args[0], meta.runtime.Name("noPrompt"),
            using='FBXEXPORTER'
        )
        if export(**kwargs):
            return args[0]

    if getattr(meta, 'eval', False):
        return cls(meta.eval("FBXExportInAscii -v true; FBXExport -f \"{}\" -s;".format(*args)))

    if getattr(meta, "data", False):
        return cls(meta.export(*args))

    if getattr(meta, "BVH3", False):
        import fbx, rumbapy
        nodes = []  # export all the assets
        frames = []  # export all the frames
        ascii = False  # we want a binary FBX file
        prefix = True  # we want the asset names prefixed by the root node name, like Maya would do

        with rumbapy.Progress("Exporting animation...") as progress:
            fbx.export_nodes(args[0], nodes, frames, ascii, prefix, progress.update)
        return


def _gltfExporter(cls, *args, **kwargs):
    if getattr(meta, "hda", False):
        return cls(meta.exportGLTF(*args))
    if getattr(meta, "data", False):
        return cls(meta.export(*args))
    if getattr(meta, "SceneObject", False):
        return cls(meta.exportGLTF(*args))


def _usdImporter(cls, *args, **kwargs):
    """"""


def _usdExporter(cls, *args, **kwargs):
    """"""


class _NodeType(object):
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
# selection create glob list segments
node = Node()
Node.selected = _select
Node.glob = _glob
Node.ls = _ls
Node.rm = _rm

# Monkey-Patch for command
cmd = Command()
Command.nt = _NodeType
Command.exec = meta.eval

# Monkey-Patch for file extension
file = File()
File.abc.Importer = _alembicImporter
File.abc.Exporter = _alembicExporter
File.fbx.Importer = _fbxImporter
File.fbx.Exporter = _fbxExporter
File.gltf.Exporter = _gltfExporter
File.usd.Importer = _usdImporter
File.usd.Exporter = _usdExporter
