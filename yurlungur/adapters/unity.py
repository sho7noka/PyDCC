# coding: utf-8
try:
    import clr
    import UnityEngine
    import UnityEditor

    getattr(UnityEngine, "Debug")

except (ImportError, AttributeError):
    import textwrap
    from yurlungur.core.env import App as _

    run, shell, end = _("unity")._actions


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
        print asm.ToString()
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
