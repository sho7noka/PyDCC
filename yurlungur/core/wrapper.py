# -*- coding: utf-8 -*-
"""

"""

import yurlungur
from yurlungur.core.app import application
from yurlungur.core import env


class MetaObject(type):
    def __new__(cls, name, bases, attrs):
        return super(MetaObject, cls).__new__(cls, name, bases, attrs)


class MetaAttr(type):
    def __new__(cls, name, bases, attrs):
        return super(MetaAttr, cls).__new__(cls, name, bases, attrs)

    @staticmethod
    def add(self):
        pass

    @staticmethod
    def rmv(self):
        pass


# Dynamic Class
_YObject = MetaObject("YObject", (object,), {"__doc__": MetaObject.__doc__})
_YAttr = MetaAttr("YAttr", (object,), {"__doc__": MetaAttr.__doc__, "add": MetaAttr.add, "rmv": MetaAttr.rmv})
_YVector, _YMatrix, _YColors = (object, object, object)


class MultiObject(object):
    """
    command wrapper for any application
    """
    if env.Photoshop():
        from yurlungur.adapters import photoshop as ps
        doc = ps.Document()._doc

    if env.UE4():
        from yurlungur.adapters import ue4
        editor = ue4.EditorUtil()
        assets = ue4.GetEditorAssetLibrary()
        levels = ue4.GetEditorLevelLibrary()
        tools = ue4.tools

    if env.Unity():
        from yurlungur.adapters import unity
        editor = unity.UnityEditor
        engine = unity.UnityEngine

    if env.Substance():
        from yurlungur.adapters import substance as sd
        graph = sd.graph
        manager = sd.manager

    if env.C4D():
        doc = application.documents.GetActiveDocument()

    if env.Davinci():
        resolve = env.__import__("DaVinciResolveScript").scriptapp("Resolve")
        if resolve:
            fusion = resolve.Fusion()
            manager = resolve.GetProjectManager()

    def __getattr__(self, item):
        try:
            from inspect import getmembers

        except ImportError:
            setattr(yurlungur, item, getattr(application, item))
            return getattr(application, item)

        for cmd, _ in getmembers(application):
            if cmd == item:
                setattr(
                    yurlungur, cmd,
                    (lambda str: dict(getmembers(application))[str])(cmd)
                )
                return getattr(yurlungur, item)

        return getattr(yurlungur, item, False)

    def eval(self, script):
        """
        eval script for
        mel, hscript, tcl, lua, ue4, C#, mxs, and jsx.

        Args:
            script:

        Returns:

        """
        if env.Maya():
            import maya.mel as mel
            return mel.eval(script)

        if env.Houdini():
            return application.hscript(script)

        if env.Nuke():
            return application.tcl(script)

        if env.Davinci() and self.resolve:
            return self.fusion.GetCurrentComp().Execute(script)

        if env.UE4():
            from yurlungur.adapters import ue4
            return ue4.execute_console_command(script)

        if env.Unity():
            from yurlungur.adapters import unity
            return unity.EvalScript(script)

        if env.Max():
            return application.runtime.execute(script)

        if env.Photoshop():
            return application.DoJavascript(script)

    @property
    def module(self):
        return application


# math for native
if env.Maya() or env.Rumba():  # and Katana
    try:
        import imath
    except ImportError:
        import Imath as imath

    _YVector = type('_YVector', (imath.V3f,), dict())
    _YMatrix = type('_YMatrix', (imath.M33f,), dict())
    _YColors = type('_YColors', (imath.Color4f,), dict())

    if env.Maya():
        for plugin in "fbxmaya.mll", "AbcImport.mll", "AbcExport.mll":
            application.loadPlugin(plugin, qt=1)

elif env.Houdini() or env.UE4() or env.Unity():
    _YVector = type('_YVector', (
        application.Vector if hasattr(application, "Vector") else application.Vector3,
    ), dict())

    if env.Unity():
        pass
        # _YMatrix = type('_YMatrix', (application.Matrix4x4), dict())
    else:
        _YMatrix = type('_YMatrix', (
            application.Matrix if hasattr(application, "Matrix") else application.Matrix4,
        ), dict())

    _YColors = type('_YColors', (application.Color,), dict())

elif env.Substance():
    _YVector = type('_YVector', (application.SDValueVector,), dict())
    _YMatrix = type('_YMatrix', (application.SDValueMatrix,), dict())
    _YColors = type('_YColors', (application.SDValueColorRGBA,), dict())

elif env.Blender():
    import mathutils

    _YVector = type('_YVector', (mathutils.Vector,), dict())
    _YMatrix = type('_YMatrix', (mathutils.Matrix,), dict())
    _YColors = type('_YColors', (mathutils.Color,), dict())

elif env.Nuke():
    import _nukemath

    _YVector = type('_YVector', (_nukemath.Vector3,), dict())
    _YMatrix = type('_YMatrix', (_nukemath.Matrix4,), dict())

elif env.Max():
    _YVector = type('_YVector', (application.Point3,), dict())
    _YMatrix = type('_YMatrix', (application.Matrix3,), dict())
    _YColors = type('_YColors', (application.Color,), dict())
