# coding: utf-8

# https://docs.unity3d.com/Packages/com.unity.scripting.python@2.0/manual/index.html
try:
    import UnityEngine
    import UnityEditor

    getattr(UnityEngine, "Debug")

except (ImportError, AttributeError):
    from yurlungur.core.env import App as _

    run, shell, end = _("unity")._actions


def Console():
    typeName = "UnityEngine.MonoBehaviour"
    # print System.Reflection.Assembly.Load("UnityEngine.dll").GetType(typeName);
    import clr
    import System
    for asm in System.AppDomain.CurrentDomain.GetAssemblies():
        print asm.ToString()
    return clr.UnityEditor.Scripting.Python.PythonConsoleWindow


def EvalScript(script):
    import clr
    import System.IO

    # eval C# from Roslyn
    try:
        clr.AddReference("Microsoft.CodeAnalysis.CSharp.Scripting")
        Microsoft.CodeAnalysis.CSharp.Scripting.CSharpScript.EvaluateAsync(script)
    except System.IO.FileNotFoundException:
        pass


"""
using UnityEngine;
using System.IO;
using System.Reflection;
using System.Collections;

#if UNITY_EDITOR
using System;
using UnityEditor;
using UnityEditor.SceneManagement;

[InitializeOnLoad]
public class Startup {
    static Startup()
    {
        UnityEditor.PackageManager.Client.Add("com.unity.scripting.python");
    }
}

[UnityEditor.InitializeOnLoad]
public class ExampleClass
{
    [MenuItem("Examples/Execute menu items")]
    static void EditorPlaying()
    {
        // https://docs.unity3d.com/Packages/com.unity.package-manager-ui@2.0/manual/index.html
        UnityEditor.PackageManager.Client.Add("com.unity.scripting.python");

        var newScene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
        EditorApplication.ExecuteMenuItem("GameObject/3D Object/Cube");
        EditorSceneManager.SaveScene(newScene, "Assets/MyNewScene.unity");
        EditorApplication.Exit(0);
    }
}
#endif
"""
