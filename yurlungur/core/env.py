# -*- coding: utf-8 -*-
import sys

try:
    import inspect
    import multiprocessing
    import subprocess
    import tempfile
    import os
    import functools
    import platform
    import code
    import urllib2
except ImportError:
    import urllib


def __import__(name, globals=None, locals=None, fromlist=None):
    """
    Fast path:
    see if the module has already been imported.

    Args:
        name:
        globals:
        locals:
        fromlist:

    Returns:
    """
    try:
        return sys.modules[name]
    except KeyError:
        pass

    try:
        if "DaVinci" not in name:
            raise NameError
        else:
            name = "DaVinciResolveScript"

        if platform.system() == "Windows":
            resolve = "%PROGRAMDATA%\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules"
        if platform.system() == "Darwin":
            resolve = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"
        if platform.system() == "Linux":
            resolve = "/opt/resolve/Developer/Scripting/Modules"
        sys.path.append(resolve)

    except NameError:
        pass

    if "clr" in sys.modules:
        import clr
        clr.AddReference("System.IO")
        import System.IO

        # https://pythonnet.github.io/ or https://ironpython.net/
        try:
            clr.AddReference(name)
        except System.IO.FileNotFoundException:
            pass

    try:
        import imp
        fp, pathname, description = imp.find_module(name)
        return imp.load_module(name, fp, pathname, description)

    except ImportError:
        try:
            from importlib import import_module
            return import_module(name)
        except ImportError:
            return False


def get_pip():
    """
    Returns: pip module

    """
    try:
        import pip
    except ImportError:
        with urllib2.urlopen("https://raw.github.com/pypa/pip/master/contrib/get-pip.py") as f:
            print(f.read().decode("utf-8"))
        execfile("get-pip.py")

    if not getattr(pip, "main", False):
        from pip import _internal as pip

    return pip


# patch
pip = get_pip()


class App(object):
    """"""

    def __init__(self, name, version=None):
        d = {
            "maya": _Maya(version), "photoshop": _Photoshop(version),
            "houdini": _Houdini(version), "substance": _Substance(version), "3dsmax": _Max(version),
            "nuke": _Nuke(version), "c4d": _Cinema4D(version), "davinci": None,
            "blender": _Blender(version), "ue4": _Unreal(version), "unity": None,
        }
        self.app_name = d[name]

    @property
    def _actions(self):
        """
        action list
        :return: run, shell, end
        """
        return self.run, self.shell, self.end

    def run(self):
        try:
            self.pop = subprocess.Popen(self.app_name, shell=False)
            self.pop.communicate()
        except (KeyboardInterrupt, SystemExit):
            self.end()

    def end(self):
        self.pop.terminate()

    def shell(self, cmd):
        """
        https://qiita.com/it_ks/items/ae1d0ae01d831c2fc9ae
        :param cmd:
        :return:
        """
        if "maya" in self.app_name:
            # https://knowledge.autodesk.com/ja/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2018/JPN/Maya-Scripting/files/GUID-83799297-C629-48A8-BCE4-061D3F275215-htm.html
            exe = sys.executable
            multiprocessing.set_executable(
                os.path.join(os.path.dirname(exe), "mayapy")
            )
            multiprocessing.process.ORIGINAL_DIR = os.path.join(
                os.path.dirname(exe),
                "../Python/Lib/site-packages"
            )
            po = multiprocessing.Pool(4)

            _cmd = "mayapy -i -c \"import maya.standalone;maya.standalone.initialize(name='python');%s\"" % cmd

        elif "UE4" in self.app_name:
            # https://docs.unrealengine.com/ja/Engine/Editor/ScriptingAndAutomation/Python/index.html
            with tempfile.NamedTemporaryFile(delete=False) as tf:
                with open(os.path.join(tf, 'testfile.py'), 'w+b') as fp:
                    fp.write(cmd)
                    _app = os.path.join(os.path.dirname(self.app_name), "UE4Editor-Cmd")
                    _cmd = " ".join([_app, "-run=pythonscript -script={0}".format(fp)])

        elif "houdini" in self.app_name:
            # https://www.sidefx.com/ja/docs/houdini/hom/commandline.html
            _cmd = "hython -i -c \"import hou;%s\"" % cmd

        elif "3dsmax" in self.app_name:
            # http://help.autodesk.com/view/3DSMAX/2018/ENU/?guid=__developer_about_the_3ds_max_python_api_html
            pass

        elif "substance" in self.app_name:
            # https://docs.substance3d.com/sat
            pass

        elif "nuke" in self.app_name:
            # https://learn.foundry.com/nuke/8.0/content/user_guide/configuring_nuke/command_line_operations.html
            _cmd = self.app_name + " -t"

        elif "c4d" in self.app_name:
            # https://developers.maxon.net/docs/Cinema4DPythonSDK/html/manuals/introduction/python_c4dpy.html
            self.app_name.replace("Cinema 4D", "c4dpy")

        elif "davinci" in self.app_name:
            # https://www.steakunderwater.com/wesuckless/viewtopic.php?t=2012
            pass

        elif "Blender" in self.app_name:
            # https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html#python-options
            _cmd = "{0} --python-expr '{1}' -b".format(self.app_name, cmd)

        elif "unity" in self.app_name:
            # https://docs.unity3d.com/jp/460/Manual/CommandLineArguments.html
            _cmd = "-batchmode -executeMethod"

        try:
            _cmd = " ".join([self.app_name, "-c", cmd])
            os.system(_cmd)
        except (KeyboardInterrupt, SystemExit):
            return
        # maya.standalone.uninitialize()
        # hou.releaseLicense()

        __import__("yurlungur")
        variables = globals().copy()
        variables.update(locals())
        shell = code.InteractiveConsole(variables)
        shell.interact()


def Qt(func=None):
    """
    Blender, UE4, Unity, C4D, Davinch, Photoshop

    Args:
        func:

    Returns:

    """
    try:
        import yurlungur.Qt as Qt
        is_Qt = any([Qt])
    except ImportError:
        return False

    if func is None:
        return is_Qt

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if is_Qt:
            return func(*args, **kwargs)

    return wrapper


def Numpy(func=None):
    try:
        import numpy as nm
        is_numpy = True
    except ImportError:
        return False

    if func is None:
        return nm

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if is_numpy:
            return func(*args, **kwargs)

    return wrapper


def Maya(func=None):
    if func is None:
        return "maya" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "maya" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def Houdini(func=None):
    if func is None:
        return __import__("hou")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("hou"):
            return func(*args, **kwargs)

    return wrapper


def Substance(func=None):
    if func is None:
        return "Substance" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "Substance" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def SPainter(func=None):
    if func is None:
        return __import__("substance_painter")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("substance_painter"):
            return func(*args, **kwargs)

    return wrapper


def Blender(func=None):
    if func is None:
        return "blender" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "blender" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def UE4(func=None):
    if func is None:
        return "UE4" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "UE4" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def Unity(func=None):
    if func is None:
        return __import__("UnityEngine")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("UnityEngine"):
            return func(*args, **kwargs)

    return wrapper


def Nuke(func=None):
    if func is None:
        return "Nuke" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "Nuke" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def C4D(func=None):
    if func is None:
        return "Cinema 4D" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "Cinema 4D" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def Davinci(func=None):
    if func is None:
        return __import__("DaVinciResolveScript")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("DaVinciResolveScript"):
            return func(*args, **kwargs)

    return wrapper


def Photoshop(func=None):
    if func is None:
        try:
            from yurlungur.adapters import photoshop
            return photoshop.app.isRunning()
        except Exception:
            return False

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            from yurlungur.adapters import photoshop
            if photoshop.app.isRunning():
                return func(*args, **kwargs)
            else:
                raise WindowsError
        except Exception:
            return False

    return wrapper


def Max(func=None):
    if func is None:
        return "3dsmax" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "3dsmax" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def _Maya(v=2018):
    d = {
        "Linux": "/usr/Autodesk/maya%d-x64/bin/maya" % v,
        "Windows": "C:/Program Files/Autodesk/Maya%d/bin/maya.exe" % v,
        "Darwin": "/Applications/Autodesk/maya%d/Maya.app/Contents" % v,
    }
    return os.environ.get("MAYA_LOCATION") or d[platform.system()]


def _Houdini(v="17.5.173"):
    d = {
        "Linux": "/opt/hfs%s/houdini" % v,
        "Windows": "C:/Program Files/Side Effects Software/Houdini Houdini%s/bin/houdini.exe" % v,
        "Darwin": "/Applications/Houdini/Houdini%s/Utilities/Houdini Terminal %s.app" % (v, v),
    }
    return os.environ.get("HIP") or d[platform.system()]


def _Substance():
    d = {
        "Linux": "/usr/autodesk/maya2017-x64",
        "Windows": "C:/Program Files/Allegorithmic/Substance Designer/Substance Designer.exe",
        "Darwin": "/Applications/Substance Designer.app/Contents/MacOS/Substance Designer",
    }
    return d[platform.system()]


def _Blender():
    d = {
        "Linux": "/usr/bin/blender",
        "Windows": "C:/Program Files/Blender Foundation/Blender",
        "Darwin": "/Applications/Blender.app/Contents/MacOS/Blender"
    }
    return d[platform.system()]


def _Unreal(v=4.22):
    d = {
        "Linux": "",
        "Windows": "C:/Program Files/Epic Games/UE_%s/Engine/Binaries/Win64/UE4Editor.exe" % v,
        "Darwin": "/Users/Shared/Epic Games/UE_%s/Engine/Binaries/Mac/UE4Editor.app/Contents/MacOS/UE4Editor" % v
    }
    return d[platform.system()]


def _Unity(v="2019.3.0f6"):
    # https://docs.unity3d.com/ja/2019.1/Manual/CommandLineArguments.html
    d = {
        "Linux": None,
        "Windows": "C:/Program Files/Unity/Editor/Unity.exe",
        "Darwin": "/Applications/Unity/Hub/Editor/%s/Unity.app/Contents/MacOS/Unity" % v
    }
    return d[platform.system()]


def _Photoshop(v=2018):
    d = {
        "Linux": None,
        "Windows": "C:/Program Files/Adobe/Adobe Photoshop CC %d/Photoshop.exe" % v,
        "Darwin": "/Applications/Adobe Photoshop CC {0}/Adobe Photoshop CC {0}.app/Contents/MacOS/Adobe Photoshop CC {0}".format(
            v),
    }
    return d[platform.system()]


def _Max(v=2018):
    return os.environ.get("ADSK_3DSMAX_X64_%d" % v) or "C:/Program Files/Autodesk/3ds Max %d/3dsmax.exe" % v


def _SubstancePainter():
    d = {
        "Linux": "/opt/Allegorithmic/Substance_Painter/Substance Painter",
        "Windows": "C:/Program Files/Allegorithmic/Substance Painter/Substance Painter.exe",
        "Darwin": "/Applications/Substance Painter.app/Contents/MacOS/Substance Painter"
    }
    return d[platform.system()]


def _Nuke():
    d = {
        "Linux": "",
        "Windows": "",
        "Darwin": ""
    }
    return d[platform.system()]


def _Cinema4D(v=21):
    d = {
        "Linux": None,
        "Windows": "C:/Cinema/R%d/Cinema 4D.exe" % v,
        "Darwin": "/Applications/Maxon Cinema 4D R%d/Cinema 4D.app/Contents/MacOS/Cinema 4D" % v
    }
    return d[platform.system()]


def _Davinci():
    d = {
        "Linux": "",
        "Windows": "",
        "Darwin": "/Applications/DaVinci Resolve Studio.app/Contents/MacOS/Resolve"
    }
    return d[platform.system()]
