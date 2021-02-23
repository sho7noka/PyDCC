# -*- coding: utf-8 -*-
import yurlungur
from yurlungur.core.app import application
from yurlungur.core import env


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
        from yurlungur.adapters import substance_designer as sd
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
        mel, hscript, tcl, lua, ue command, unity C#, mxs, and jsx.

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


class MetaObject(type):
    """"""

    def __new__(cls, name, bases, attrs):
        return super(MetaObject, cls).__new__(cls, name, bases, attrs)

    @staticmethod
    def add(self):
        pass

    @staticmethod
    def rmv(self):
        pass


# Dynamic Class
YObject = MetaObject("YObject", (object,),
                     {"__doc__": MetaObject.__doc__,
                      "add": MetaObject.add, "rmv": MetaObject.rmv})
