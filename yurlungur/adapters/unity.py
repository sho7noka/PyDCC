# coding: utf-8
try:
    import clr
    import UnityEngine as UnityEngine
    import UnityEditor as UnityEditor

    Console = clr.UnityEditor.Scripting.Python.PythonConsoleWindow
    Outputs = Console.AddToOutput
    getattr(UnityEngine, "Debug")  # NOTE: DO NOT DELETE


    class Timeline(object):
        def __init__(self, timeline):
            self.timeline = timeline

            T = clr.GetClrType(Timeline.TimelineAsset)
            timelineAsset = UnityEngine.ScriptableObject.CreateInstance(T)
            path = "Assets/Sample.playable"
            UnityEditor.AssetDatabase.CreateAsset(timelineAsset, path)

        @property
        def tracks(self):
            return Track(self.timeline)


    class Track(object):
        def __init__(self, track):
            self.track = track

        @property
        def clips(self):
            return Item(self.track)


    class Item(object):
        pass


    def EvalScript(script):
        """
        NOTE: Require Roslyn or Mono.CSharp

        Args:
            script:

        Returns:

        """
        import System.IO
        try:
            clr.AddReference("Microsoft.CodeAnalysis.CSharp.Scripting")
            import Microsoft.CodeAnalysis.CSharp.Scripting as scripting
            scripting.CSharpScript.EvaluateAsync(script)

            clr.AddReference("Mono.CSharp")
            import Mono.Csharp
            Mono.CSharp.Evaluator.Run(script)

        except System.IO.FileNotFoundException:
            """
            https://stackoverflow.com/questions/19600315/how-to-use-a-net-method-which-modifies-in-place-in-python/19600349#19600349
            var value = 0;
            UnityEditor.ExpressionEvaluator.Evaluate(script, value: out value);    
            """
            v = 0
            _, out = UnityEditor.ExpressionEvaluator.Evaluate(script, v)
            print(out)

except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, _, end, _ = __App("unity")._actions

    __all__ = ["run", "end"]


def Projects():
    """
    Returns: RecentProjectPath list
    """
    import os
    import platform

    recent_key = 'RecentlyUsedProjectPaths-'
    projects = []

    # https://area.autodesk.jp/column/tutorial/maya_atoz/send-to-unity/
    if platform.platform() == "Windows":
        import _winreg
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Unity Technologies\Unity Editor 5.x')
        info = _winreg.QueryInfoKey(key)
        for i in range(info[1]):
            v = _winreg.EnumValue(key, i)
            if recent_key in v[0]:
                projects.append(v[1])

    if platform.platform() == "Darwin":
        import plistlib
        plist = os.getenv("HOME") + "/Library/Preferences/com.unity3d.UnityEditor5.x.plist"

        with open(plist, "rb") as fp:
            info = plistlib.load(fp)
            for k, v in info.items():
                if recent_key in k:
                    projects.append(v)

    # TODO
    if platform.platform() == "Linux":
        projects.append("")

    return projects


def to_manifest(path="Packages/manifest.json", version="2.0.1-preview.2"):
    """
    https://docs.unity3d.com/Packages/com.unity.scripting.python@2.1/manual/
    https://docs.unity3d.com/Packages/com.unity.package-manager-ui@2.0/manual/index.html
    Args:
        path:
        version:

    Returns:

    """
    import os
    import json
    import collections

    if path is None:
        latest = Projects()[0]
        path = os.path.join(latest, path)

    with open(path) as f:
        df = json.load(f, object_pairs_hook=collections.OrderedDict)
        df["dependencies"]["com.unity.scripting.python"] = version
        with open(path, 'w') as w:
            json.dump(df, w, indent=4)


def initialize_package(path="Assets/Editor/PythonEditor.cs"):
    """
    Args:
        path:

    Returns:

    """
    import os
    import textwrap

    if path is None:
        latest = Projects()[0]
        path = os.path.join(latest, path)

    with open(path, "w") as f:
        f.write(textwrap.dedent("""
        using System;
        using System.IO;
        using System.Linq;
        using System.Collections.Generic;
        using Object = UnityEngine.Object;
        #if UNITY_EDITOR
        using UnityEditor;
        using UnityEditor.Scripting.Python;
        
        namespace PythonExtensions
        {
            [InitializeOnLoad]
            public class Startup
            {
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
            }
        
            public class PythonExtension
            {
                [MenuItem("Assets/Python/Open In ScriptEditor")]
                private static void OpenScriptEditor()
                {
                    // get text
                    var selectedAssets = Selection.GetFiltered(typeof(Object), SelectionMode.Assets);
                    var path = AssetDatabase.GetAssetPath(selectedAssets.First());
                    var m_codeContents = System.IO.File.ReadAllText(path);
        
                    // serialize field
                    EditorApplication.ExecuteMenuItem("Window/General/Python Console");
        
                    var window = EditorWindow.GetWindow<PythonConsoleWindow>();
                    var content = new SerializedObject(window);
                    content.Update();
                    var property = content.FindProperty("m_codeContents");
                    property.stringValue = m_codeContents;
                    content.ApplyModifiedProperties();
                }
        
                [MenuItem("Assets/Python/Python Script")]
                private static void CreateScript()
                {
                    var path = "Assets/Python";
                    if (!AssetDatabase.IsValidFolder(path))
                    {
                        path = Path.GetDirectoryName(path);
                    }
        
                    path += Path.DirectorySeparatorChar + "new_script.py";
                    path = AssetDatabase.GenerateUniqueAssetPath(path);
                    path = Path.GetFullPath(path);
        
                    File.CreateText(path);
                    AssetDatabase.Refresh();
                }
            }
        
            public class SaveHook : UnityEditor.AssetModificationProcessor
            {
                private static bool is_python = false;
        
                private void OnWillSaveAssets(IEnumerable<string> paths)
                {
                    foreach (var path in paths)
                    {
                        if (!path.EndsWith(".py")) continue;
                        is_python = true;
                        break;
                    }
        
                    if (is_python)
                        AssetDatabase.Refresh();
                }
            }
        }
        #endif
        """))
