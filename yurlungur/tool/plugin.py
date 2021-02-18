# -*- coding: utf-8 -*-
import ast
from string import Template
from textwrap import dedent

from yurlungur.core.wrapper import MetaObject
from yurlungur.core.logger import GuiLogHandler

"""
proxy
decorator
env
logging
ui
"""

"""
maya max painter designer
"""


class Plugin(Template):
    def __init__(self, template):
        self.delimiter = "$"
        self.idpattern = self.idpattern
        self.template = dedent(template)

    def compile(self, path):
        with open(path, "w") as f:
            f.write(self.template)
        self.pattern


template = Plugin("""
VERSIONING_PLUGIN = None


def maya_useNewAPI():
    pass


def initializePlugin( mobject ):
    mplugin = om.MFnPlugin( mobject )
    try:
        # 引数を持たせる場合と持たせない場合でココもちょっと変わる
        mplugin.registerCommand( kPluginCmdName, cmdCreator, syntaxCreator )
    except:
        sys.stderr.write( 'Failed to register command: ' + kPluginCmdName )
 
def uninitializePlugin( mobject ):
    mplugin = om.MFnPlugin( mobject )
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( 'Failed to unregister command: ' + kPluginCmdName ) 
            

# Plugin entry point. Called by Designer when loading a plugin.
def initializeSDPlugin():
	print("Hello!")

# If this function is present in your plugin,
# it will be called by Designer when unloading the plugin.
def uninitializeSDPlugin():
	print("Bye!")


def start_plugin():
    global VERSIONING_PLUGIN
    VERSIONING_PLUGIN = VersioningPlugin()


def close_plugin():
    global VERSIONING_PLUGIN
    del VERSIONING_PLUGIN


if __name__ == "__main__":
    start_plugin()
""")

d = dict(who="")
template.substitute(d)


def register():
    pass


class Plugbase(MetaObject):
    """"""

    def proxy(self):
        pass

    def env(self):
        pass

    def logging(self):
        """
        logging level
        :return:
        """
        GuiLogHandler.emit = ""

    def decorator(self):
        pass

    def ui(self):
        pass


import os

# Substance Painter modules
import substance_painter.ui
import substance_painter.export
import substance_painter.project
import substance_painter.textureset

# PySide module to build custom UI
from PySide2 import QtWidgets

plugin_widgets = []


def export_textures():
    # Verify if a project is open before trying to export something
    if not substance_painter.project.is_open():
        return

    # Get the currently active layer stack (paintable)
    stack = substance_painter.textureset.get_active_stack()

    # Get the parent Texture Set of this layer stack
    material = stack.material()

    # Build Export Preset resource URL
    export_preset = substance_painter.resource.ResourceID(
        context="allegorithmic",
        name="PBR Metallic Roughness")

    print("Preset:")
    print(export_preset.url())

    # Setup the export settings
    resolution = material.get_resolution()

    # Setup the export path, in this case the textures
    # will be put next to the spp project file on the disk
    Path = substance_painter.project.file_path()
    Path = os.path.dirname(Path) + "/"

    # Build the configuration
    config = {
        "exportShaderParams": False,
        "exportPath": Path,
        "exportList": [{"rootPath": str(stack)}],
        "exportPresets": [{"name": "default", "maps": []}],
        "defaultExportPreset": export_preset.url(),
        "exportParameters": [
            {
                "parameters": {"paddingAlgorithm": "infinite"}
            }
        ]
    }

    substance_painter.export.export_project_textures(config)


def start_plugin():
    # Create a text widget for a menu
    Action = QtWidgets.QAction("Custom Python Export",
                               triggered=export_textures)

    # Add this widget to the existing File menu of the application
    substance_painter.ui.add_action(
        substance_painter.ui.ApplicationMenu.File,
        Action)

    # Store the widget for proper cleanup later when stopping the plugin
    plugin_widgets.append(Action)


def close_plugin():
    # Remove all widgets that have been added from the UI
    for widget in plugin_widgets:
        substance_painter.ui.delete_ui_element(widget)

    plugin_widgets.clear()


# https://help.autodesk.com/view/MAXDEV/2021/ENU/?guid=Max_Python_API_using_pymxs_pymxs_macroscripts_menus_html
from pymxs import runtime as rt


# Our Py function:
def myfunc():
    print('hello world')


# Connect to a gobal in the runtime:
rt.mxs_hello = myfunc
macroscript_name = 'My_Macroscript'
macroscript_category = 'Test'
macroscript_tooltip = 'This is a tooltip'
macroscript_text = 'My Macroscript'
macroscript_content = 'mxs_hello()'

macro_id = rt.macros.new(macroscript_category, macroscript_name, macroscript_tooltip, macroscript_button,
                         macroscript_content)
help_menu = rt.menuMan.findMenu('&Help')
menu_item = rt.menuMan.createActionItem(macroscript_name, macroscript_category)
help_menu.addItem(menu_item, -1)
rt.menuMan.updateMenuBar()
# help_menu.removeItem(menu_item)


import bpy  # アドオン開発者に対して用意しているAPIを利用する

# アドオンに関する情報を保持する、bl_info変数
bl_info = {
    "name": "サンプル 2-1: オブジェクトを生成するアドオン",
    "author": "ぬっち（Nutti）",
    "version": (3, 0),
    "blender": (2, 80, 0),
    "location": "3Dビューポート > 追加 > メッシュ",
    "description": "オブジェクトを生成するサンプルアドオン",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


# オブジェクト（ICO球）を生成するオペレータ
class SAMPLE21_OT_CreateObject(bpy.types.Operator):
    bl_idname = "object.sample21_create_object"
    bl_label = "球"
    bl_description = "ICO球を追加します"
    bl_options = {'REGISTER', 'UNDO'}

    # メニューを実行したときに呼ばれる関数
    def execute(self, context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("サンプル 2-1: ICO球を生成しました。")

        return {'FINISHED'}


# メニューを構築する関数
def menu_fn(self, context):
    self.layout.separator()
    self.layout.operator(SAMPLE21_OT_CreateObject.bl_idname)


# Blenderに登録するクラス
classes = [
    SAMPLE21_OT_CreateObject,
]


# アドオン有効化時の処理
def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_fn)
    print("サンプル 2-1: アドオン『サンプル 2-1』が有効化されました。")


# アドオン無効化時の処理
def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_fn)
    for c in classes:
        bpy.utils.unregister_class(c)
    print("サンプル 2-1: アドオン『サンプル 2-1』が無効化されました。")


# メイン処理
if __name__ == "__main__":
    register()

if __name__ == "__main__":
    start_plugin()
