# -*- coding: utf-8 -*-
import sys
from yurlungur.core.env import __import__


class YException(NotImplementedError):
    """
    >>> raise NotImplementedError(application)
    """
    pass


application = sys.executable

if "maya" in application:
    import maya.cmds as cmds

    application = cmds

elif __import__("hou"):
    import hou

    application = hou

elif "Substance" in application:
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

elif __import__("substance_painter"):
    import substance_painter

    application = substance_painter

else:
    from yurlungur.tool import standalone

    application = standalone


def use(module):
    """
    set external application
    Args:
        module:

    Returns:

    >>> import yurlungur
    >>> yurlungur.use("hou")
    """
    from yurlungur.core import env

    if module == "photoshop":
        from yurlungur.adapters import photoshop

        application = photoshop.app
    else:
        application = env.__import__(module)

    assert application, "application is not found."
