# coding: utf-8
try:
    import clr
    import UnityEngine
    import UnityEditor

    getattr(UnityEngine, "Debug")

except ImportError:
    import json
    import textwrap
    import collections
    from yurlungur.core.env import App as __App

    run, _, end, _ = __App("unity")._actions


    def manifest(path="Packages/manifest.json", version="2.0.1-preview.2"):
        with open(path) as f:
            df = json.load(f, object_pairs_hook=collections.OrderedDict)
            df["dependencies"]["com.unity.scripting.python"] = version
            with open(path, 'w') as w:
                json.dump(df, w, indent=4)


    def initialize_package(path):
        """
        https://docs.unity3d.com/Packages/com.unity.package-manager-ui@2.0/manual/index.html

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


def Console():
    """

    Returns:

    """
    import System
    for asm in System.AppDomain.CurrentDomain.GetAssemblies():
        print (asm.ToString())
    return clr.UnityEditor.Scripting.Python.PythonConsoleWindow


def EvalScript(script):
    """

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
