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
    import contextlib
    import textwrap
    import urllib2 as urllib
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

    # https://pythonnet.github.io/ or https://ironpython.net/
    if "clr" in sys.modules:
        import clr
        clr.AddReference("System.IO")
        import System.IO

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
        with urllib.urlopen("https://raw.github.com/pypa/pip/master/contrib/get-pip.py") as f:
            print(f.read().decode("utf-8"))
        execfile("get-pip.py")
        os.remove("get-pip.py")

    if not getattr(pip, "main", False):
        from pip import _internal as pip

    return pip


# patch
pip = get_pip()


class App(object):
    """"""

    def __init__(self, name, version=None):
        d = {
            "maya": _Maya(), "houdini": _Houdini(), "substance": _Substance(),
            "blender": _Blender(), "ue4": _Unreal(), "unity": _Unity(),
            "nuke": _Nuke(), "c4d": _Cinema4D(), "davinci": _Davinci(),
            "3dsmax": _Max(), "photoshop": _Photoshop(),
            "substance_painter": _SubstancePainter()
        }
        self.app_name = d[name]
        self.process = None

    def run(self):
        try:
            self.process = subprocess.Popen(self.app_name, shell=False)
            self.process.communicate()
        except (KeyboardInterrupt, SystemExit):
            self.end()

    def shell(self, cmd):
        # https://knowledge.autodesk.com/ja/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2018/JPN/Maya-Scripting/files/GUID-83799297-C629-48A8-BCE4-061D3F275215-htm.html
        if "maya" in self.app_name:
            # exe = sys.executable
            # multiprocessing.set_executable(
            #     os.path.join(os.path.dirname(exe), "mayapy")
            # )
            # multiprocessing.process.ORIGINAL_DIR = os.path.join(
            #     os.path.dirname(exe),
            #     "../Python/Lib/site-packages"
            # )
            # po = multiprocessing.Pool(4)

            mayapy = self.app_name.replace("bin/maya", "bin/mayapy")
            _cmd = "%s -i -c \"import maya.standalone;maya.standalone.initialize(name='python');%s\"" % (mayapy, cmd)

        # https://www.sidefx.com/ja/docs/houdini/hom/commandline.html
        elif "houdini" in self.app_name:
            _cmd = "hython -i -c \"%s\"" % cmd

        elif "3dsmax" in self.app_name:
            if sys.version_info.major > 3:
                maxpy = os.path.join(os.path.dirname(self.app_name), "Python37/python.exe")
            else:
                maxpy = self.app_name.replace("3dsmax.exe", "3dsmaxpy.exe")
            _cmd = "%s -i -c \"%s\"" % (maxpy, cmd)

        # https://docs.unrealengine.com/ja/Engine/Editor/ScriptingAndAutomation/Python/index.html
        elif "UE4" in self.app_name:
            with tempfile.NamedTemporaryFile(delete=False) as tf:
                with open(os.path.join(tf, 'testfile.py'), 'w+b') as fp:
                    fp.write(cmd)
                    _app = os.path.join(os.path.dirname(self.app_name), "UE4Editor-Cmd")
                    _cmd = " ".join([_app, "-run=pythonscript -script={0}".format(fp)])

        elif "Blender" in self.app_name:
            # https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html#python-options
            _cmd = "{0} --python-expr '{1}' -b".format(self.app_name, cmd)

        # https://docs.unity3d.com/jp/460/Manual/CommandLineArguments.html
        elif "unity" in self.app_name:
            with open("Assets/Editor/PythonEditor.cs", "w") as f:
                f.write(textwrap.dedent("""
                using System;

                #if UNITY_EDITOR
                using UnityEditor.Scripting.Python;
                
                public static void Exec()
                {
                    var args = Environment.GetCommandLineArgs();
                    
                    if (args.First().EndsWith(".py"))
                    {
                        PythonRunner.RunFile(args.First());
                    }
                    else
                    {
                        PythonRunner.RunString(args.First());
                    }
                }
                #endif
                """))
            _cmd = "%s -batchmode -executeMethod PythonScript.Exec %s" % (self.app_name, cmd)

        # https://learn.foundry.com/nuke/8.0/content/user_guide/configuring_nuke/command_line_operations.html
        elif "nuke" in self.app_name:
            _cmd = self.app_name + " -t"

        # https://developers.maxon.net/docs/Cinema4DPythonSDK/html/manuals/introduction/python_c4dpy.html
        elif "c4d" in self.app_name:
            self.app_name = self.app_name.replace("Cinema 4D", "c4dpy")

        # https://www.steakunderwater.com/wesuckless/viewtopic.php?t=2012
        elif "davinci" in self.app_name:
            pass

        try:
            os.system(_cmd)
        except (KeyboardInterrupt, SystemExit):
            return
            # maya.standalone.uninitialize()
            # hou.releaseLicense()

        # __import__("yurlungur")
        # variables = globals().copy()
        # variables.update(locals())
        # shell = code.InteractiveConsole(variables)
        # shell.interact()

    @contextlib.contextmanager
    def connect(self, port):
        """
        https://qiita.com/QUANON/items/c5868b6c65f8062f5876
        """
        import yurlungur
        self.shell(
            "import sys;sys.path.append(\"%s\");from yurlungur.tool import rpc;rpc.listen(%d)"
            % (os.path.dirname(os.path.dirname(os.path.abspath(yurlungur.__file__))), port)
        )

        from yurlungur.tool import rpc
        try:
            yield rpc.session(port)
        finally:
            print("revert")

    def end(self):
        self.process.terminate()

    @property
    def _actions(self):
        """
        Returns:
           run, shell, end, connect
        """
        return self.run, self.shell, self.end, self.connect


def Qt(func=None):
    """
    Blender, UE4, Unity, C4D

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
    """
    Blender, Houdini
    Args:
        func:

    Returns:

    """
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


def _Maya(v=2020):
    d = {
        "Linux": "/usr/Autodesk/maya%d-x64/bin/maya" % v,
        "Windows": "C:/Program Files/Autodesk/Maya%d/bin/maya.exe" % v,
        "Darwin": "/Applications/Autodesk/maya%d/Maya.app/Contents/bin/maya" % v,
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
        "Linux": "/opt/Allegorithmic/Substance_Designer/Substance Designer",
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
