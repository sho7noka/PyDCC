# coding: utf-8
import os
import platform
import json
import textwrap
import collections

try:
    import clr
    import UnityEngine as UnityEngine
    import UnityEditor as UnityEditor

    # Do not Delete
    getattr(UnityEngine, "Debug")
    # ['AddToOutput', 'BeginWindows', 'Close', 'CreateInstance', 'CreateWindow', 'Destroy', 'DestroyImmediate', 'DestroyObject', 'DontDestroyOnLoad', 'EndWindows', 'Equals', 'Finalize', 'FindObjectOfType', 'FindObjectsOfType', 'FindObjectsOfTypeAll', 'FindObjectsOfTypeIncludingAssets', 'FindSceneObjectsOfType', 'Focus', 'FocusWindowIfItsOpen', 'GetExtraPaneTypes', 'GetHashCode', 'GetInstanceID', 'GetType', 'GetWindow', 'GetWindowWithRect', 'HasOpenInstances', 'Instantiate', 'MemberwiseClone', 'OnEnable', 'Overloads', 'ReferenceEquals', 'RemoveNotification', 'Repaint', 'SendEvent', 'SetDirty', 'Show', 'ShowAsDropDown', 'ShowAuxWindow', 'ShowModalUtility', 'ShowNotification', 'ShowPopup', 'ShowTab', 'ShowUtility', 'ShowWindow', 'ToString', '__call__', '__class__', '__delattr__', '__delitem__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__overloads__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'antiAlias', 'autoRepaintOnSceneChange', 'depthBufferBits', 'focusedWindow', 'get_antiAlias', 'get_autoRepaintOnSceneChange', 'get_depthBufferBits', 'get_focusedWindow', 'get_hideFlags', 'get_maxSize', 'get_maximized', 'get_minSize', 'get_mouseOverWindow', 'get_name', 'get_position', 'get_rootVisualElement', 'get_title', 'get_titleContent', 'get_wantsMouseEnterLeaveWindow', 'get_wantsMouseMove', 'hideFlags', 'maxSize', 'maximized', 'minSize', 'mouseOverWindow', 'name', 'op_Equality', 'op_Implicit', 'op_Inequality', 'position', 'rootVisualElement', 'set_antiAlias', 'set_autoRepaintOnSceneChange', 'set_depthBufferBits', 'set_hideFlags', 'set_maxSize', 'set_maximized', 'set_minSize', 'set_name', 'set_position', 'set_title', 'set_titleContent', 'set_wantsMouseEnterLeaveWindow', 'set_wantsMouseMove', 'title', 'titleContent', 'wantsMouseEnterLeaveWindow', 'wantsMouseMove
    Console = clr.UnityEditor.Scripting.Python.PythonConsoleWindow


    def EvalScript(script):
        """
        NOTE: Require Roslyn

        Args:
            script:

        Returns:

        """
        import System.IO
        try:
            clr.AddReference("Microsoft.CodeAnalysis.CSharp.Scripting")
            import Microsoft.CodeAnalysis.CSharp.Scripting as scripting
            scripting.CSharpScript.EvaluateAsync(script)
        except System.IO.FileNotFoundException:
            pass

except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, _, end, _ = __App("unity")._actions


    def Projects():
        """

        Returns: RecentProjectPath generator

        """
        recent_key = 'RecentlyUsedProjectPaths-'

        # https://area.autodesk.jp/column/tutorial/maya_atoz/send-to-unity/
        if platform.platform() == "Windows":
            import _winreg
            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Unity Technologies\Unity Editor 5.x')
            info = _winreg.QueryInfoKey(key)
            for i in range(info[1]):
                v = _winreg.EnumValue(key, i)
                if recent_key in v[0]:
                    yield v[1]

        if platform.platform() == "Darwin":
            import plistlib
            plist = os.getenv("HOME") + "/Library/Preferences/com.unity3d.UnityEditor5.x.plist"

            with open(plist, "rb") as fp:
                info = plistlib.load(fp)
                for k, v in info.items():
                    if recent_key in k:
                        yield v

        # TODO
        if platform.platform() == "Linux":
            yield None


    def to_manifest(path="Packages/manifest.json", version="2.0.1-preview.2"):
        """
        https://docs.unity3d.com/Packages/com.unity.package-manager-ui@2.0/manual/index.html
        Args:
            path:
            version:

        Returns:

        """
        with open(path) as f:
            df = json.load(f, object_pairs_hook=collections.OrderedDict)
            df["dependencies"]["com.unity.scripting.python"] = version
            with open(path, 'w') as w:
                json.dump(df, w, indent=4)


    def initialize_package(path):
        """
        Args:
            path:

        Returns:

        """
        cs_text = textwrap.dedent("""
        using UnityEngine;
        using System.IO;
        using System.Reflection;
        using System.Collections;
    
        #if UNITY_EDITOR
        using UnityEditor;
        using UnityEditor.SceneManagement;
    
        [InitializeOnLoad]
        public class Startup {
    
            static void Startup()
            {
                UnityEditor.PackageManager.Client.Add("com.unity.scripting.python");
            }
    
            [MenuItem("Examples/Execute menu items")]
            static void EditorPlaying()
            {
                var newScene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
                EditorApplication.ExecuteMenuItem("GameObject/3D Object/Cube");
                EditorSceneManager.SaveScene(newScene, "Assets/MyNewScene.unity");
                EditorApplication.Exit(0);
            }
        }
        #endif
        """)

        with file(path) as f:
            f.write(cs_text)
