# coding: utf-8
import sys

try:
    import unreal

    sys.modules[__name__] = sys.modules["unreal"]

    @unreal.uclass()
    class EditorUtil(unreal.GlobalEditorUtilityBase):
        pass


    @unreal.uclass()
    class GetEditorAssetLibrary(unreal.EditorAssetLibrary):
        pass


    @unreal.uclass()
    class GetEditorLevelLibrary(unreal.EditorLevelLibrary):
        pass


    @unreal.uclass()
    class MaterialEditingLib(unreal.MaterialEditingLibrary):
        pass


    @unreal.uclass()
    class GetAnimationLibrary(unreal.AnimationLibrary):
        pass


    def execute_console_command(script):
        # UE4Editor.exe Project.uproject -ExecCmds=”Automation RunTests テスト名;Quit” -game
        # unreal.PythonScriptLibrary.execute_python_command("任意のスクリプトかパス")
        Editor = unreal.EditorLevelLibrary.get_editor_world()
        unreal.SystemLibrary.execute_console_command(Editor, script)


    def uname(item):
        """compatible for asset and"""

        for asset in GetEditorAssetLibrary().list_assets("/Game/"):
            if asset.endswith(item):
                return asset

        for actor in GetEditorLevelLibrary().get_all_level_actors():
            if item in actor.get_name():
                return EditorUtil().get_actor_reference(actor.get_full_name().split(":")[1])

        raise Exception


    tools = unreal.AssetToolsHelpers.get_asset_tools()


except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, end, _ = __App("ue4")._actions


class Project(object):
    def __init__(self, project):
        self.project = project

    @property
    def sequences(self):
        return Timeline(self.project)


class Timeline(object):
    def __init__(self, timeline):
        self.timeline = timeline

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
