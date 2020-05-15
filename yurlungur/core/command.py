# -*- coding: utf-8 -*-
import fnmatch
from functools import partial

from yurlungur.core.proxy import YNode, YFile
from yurlungur.tool.meta import meta
from yurlungur.core.app import YException

__all__ = ["file", "cmd", "node"]


class _NodeType(object):
    def __getattr__(self, item):
        if hasattr(meta, "types"):
            nodes = fnmatch.filter(dir(meta.types), str(item))
        else:
            nodes = self.findNodes(item)

        for node in nodes:
            setattr(self, str(item), YNode(node))

        return YNode(item)

    def findNodes(self, pattern):
        if hasattr(meta, "listNodeTypes"):
            # http://help.autodesk.com/cloudhelp/2016/JPN/Maya-Tech-Docs/CommandsPython/shadingNode.html
            categories = ["geometry", "camera", "light", "utility", "color", "shader", "texture", "rendering",
                          "postprocess"]
            # meta.allNodeTypes(ia=1)
            for category in categories:
                yield fnmatch.filter(meta.listNodeTypes(category), pattern)

        if hasattr(meta, "nodeTypes"):
            for category in meta.nodeTypeCategories().keys():
                yield fnmatch.filter(
                    meta.nodeTypeCategories()[category].nodeTypes().keys(),
                    pattern
                )


class Command(object):
    """plugin system"""

    @staticmethod
    def register(func):
        pass

    @classmethod
    def list(cls):
        return [obj for obj in dir(cls) if not obj.startswith("_")]


def _ls(cls, *args, **kwargs):
    gen = meta.ls(*args, **kwargs) if hasattr(meta, "ls") else meta.pwd().allItems()
    return tuple(YNode(obj) for obj in gen)


def _rm(cls, *args):
    for obj in args:
        YNode(obj).delete()


def _glob(cls, *args, **kwargs):
    gen = meta.ls(*args, **kwargs) if hasattr(meta, "ls") else meta.pwd().glob(*args, **kwargs)
    return tuple(YNode(obj) for obj in gen)


def _select(cls, *args, **kwargs):
    if hasattr(meta, "select"):
        meta.select(*args, **kwargs)

    if hasattr(meta, "hda"):
        for node in meta.nodes(args):
            node.setSelected(True, **kwargs)


# Monkey-Patch for node
# selection create glob list segments
node = YNode()
YNode.selection = _select
YNode.parent = None

cmd = Command()
Command.ls = _ls
Command.rm = _rm
Command.glob = _glob
Command.select = _select


def _alembicImporter(cls, *args, **kwargs):
    """
    >>> f = YFile()
    >>> YFile.new_method = new_method
    >>> print f.new_method("new")
    """
    if getattr(meta, "AbcImport", False):
        return cls(meta.AbcImport(*args, **kwargs))

    if getattr(meta, "textureset", False):
        return meta.project.create(*args, **kwargs)

    if getattr(meta, "hda", False):
        geo = yr.YNode("obj").create("geo")
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

    raise YException


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

    raise YException


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

    # fbx, obj, dae, ply, gltf, abc
    if getattr(meta, "textureset", False):
        return meta.project.create(*args, **kwargs)

    if getattr(meta, 'uclass', False):
        data = unreal.AutomatedAssetImportData()
        data.set_editor_property('filenames', *args)
        for k, v in kwargs:
            data.set_editor_property(k, v)
        factory = unreal.FbxSceneImportFactory()
        data.set_editor_property('factory', factory)

        meta.tools.import_assets_automated(data)

    if getattr(meta, 'eval', False):
        return cls(meta.eval("FBXImport -file {0};".format(*args)))

    raise YException


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

    raise YException


def _gltfImporter(cls, *args, **kwargs):
    pass


def _gltfExporter(cls, *args, **kwargs):
    pass


def _usdImporter(cls, *args, **kwargs):
    pass


def _usdExporter(cls, *args, **kwargs):
    pass


# Monkey-Patch for file
file = YFile()
YFile.abcImporter = _alembicImporter
YFile.abcExporter = _alembicExporter
YFile.fbxImporter = _fbxImporter
YFile.fbxExporter = _fbxExporter
YFile.gltfImporter = _gltfImporter
YFile.gltfExporter = _gltfExporter
YFile.usdImporter = _usdImporter
YFile.usdExporter = _usdExporter

YType = _NodeType()
