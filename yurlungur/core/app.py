# -*- coding: utf-8 -*-
"""
detect embed python interpreter.
sys.executable or __import__
"""
import sys
from yurlungur.core.env import __import__

application = sys.executable

if "maya" in application:
    import maya.cmds as cmds

    application = cmds

elif __import__("hou"):
    import hou

    application = hou

elif "Substance Designer" in application:
    import sd.api as sdapi

    application = sdapi

elif "Blender" in application:
    import bpy

    application = bpy

elif "UE4Editor" in application:
    import unreal

    application = unreal

elif __import__("UnityEngine"):
    import UnityEngine

    application = UnityEngine

elif "Nuke" in application:
    import nuke

    application = nuke

elif "Cinema 4D" in application:
    import c4d

    application = c4d

elif "3dsmax" in application:
    import pymxs

    application = pymxs

elif "Substance Painter" in application:
    import substance_painter

    application = substance_painter

elif __import__("rumba"):
    import rumba

    application = rumba

else:
    from yurlungur.tool import standalone

    application = standalone


def use(module):
    """
    set external application

    Args:
        module: str module

    Returns: None

    >>> import yurlungur
    >>> yurlungur.use("hou")
    """
    global application
    from yurlungur.core import env

    if module == "photoshop":
        from yurlungur.adapters import photoshop

        application = photoshop.app
    else:
        application = env.__import__(module)

    assert application, "application is not found."
