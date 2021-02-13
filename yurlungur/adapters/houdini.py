# coding: utf-8
import sys as __sys

try:
    __sys.modules[__name__] = __sys.modules["hou"]
except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, end, connect = __App("houdini")._actions

    __all__ = ["run", "shell", "end", "connect"]


def enableHouModule():
    '''"import hou"が動作するように、環境をセットアップします。'''
    import sys, os

    # houをインポートすることで、Houdiniのライブラリが読み込まれ、Houdiniが初期化されます。
    # そして、HoudiniはC++で記述されたHDK拡張を読み込みます。
    # それらの拡張は、Houdiniのライブラリに対してリンクさせる必要があるので、Houdiniのライブラリのシンボルが、
    # Houdiniが読み込む他のライブラリから見えている必要があります。
    # そのため、houをインポートする前に、Pythonのdlopenフラグを調整します。
    if hasattr(sys, "setdlopenflags"):
        old_dlopen_flags = sys.getdlopenflags()
    #     import DLFCN
    #     sys.setdlopenflags(old_dlopen_flags | DLFCN.RTLD_GLOBAL)

    try:
        import hou
    except ImportError:
        # Pythonがhouモジュールを検索できるように、
        # sys.pathに`$HFS/houdini/python2.7libs`を追加します。
        sys.path.append(os.environ['HFS'] + "/houdini/python%d.%dlibs" % sys.version_info[:2])
        import hou
    finally:
        if hasattr(sys, "setdlopenflags"):
            sys.setdlopenflags(old_dlopen_flags)


# enableHouModule()

# 123.cmd/pyや456.cmd/pyの初期化スクリプトを実行させたいのであれば、以下の行のコメントを外します。そうすればhouが読み込まれます。
# import hou

# hou.__runUserDefinedCode()
