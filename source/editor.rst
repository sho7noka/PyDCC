===================================
Editor tips
===================================

ここでは、APIを使ったシーン操作でよく使う項目ではなく、

GUI開発やデバッグなどそのプロセスで便利になる機能をまとめています。


Print
-------------------------------
print statement is not available in Python3.

Also IronPython is not bind with __future__ modules.

`yurlungur.pprint(*args)` の使用をお勧めします。

LogHandler をそれぞれのアプリケーションから継承し、一貫したインターフェースで出力レベルの制御をします。


.. code-block:: python

    yurlungur.pprint(*args)
    

内部処理に pformat を使っているため、ログが見切れるような長いリストでもスクリプトエディタ上の視認性は損なわれません。



UndoGroup
-------------------------------
もしUndoGroupでインデントを囲わないスクリプト処理をした場合、ひとつひとつundoを使って元に戻さなければなりません。

contextManagerで制御されたUndoGroupでアプリケーション側のUndoで操作を一度に巻き戻すことが出来ます。


.. code-block:: python

    with yr.UndoGroup("undo"):
        yr.YNode("hoge").delete()



GUI
--------------------------------
Maya/Houdiniといった大型スタジオで使われるアプリケーションのバージョンを気にすることなく

Qt.py をラッピングしているので、Python から Qt を使うことが出来ます。

それぞれのDCCアプリケーションウィンドウを取得してparentを指定することができます。

標準でQt for Pythonがインストールされていないアプリケーションでモジュールを使用するためには、

別途 pip でインストールするか、envモジュールでアプリケーションを切り分けて、

metaモジュールからそれぞれネイティブのuiモジュールを参照して下さい。


.. code-block:: python

    import yurlungur
    ptr = yr.Qt.main_window()
    widget = QWidget(ptr)


スタンドアロン起動の際にもshowメソッドでそのまま実行することができます。


.. code-block:: python

    import yurlungur
    widget = QWidget()
    yr.Qt.show(widget)


VFXWindowをサポートした環境では、いくつかのアプリケーションでコールバックを追加するパッチを適用した

UIWindow クラスにも対応しています。


.. code-block:: python

    import yurlungur

    class MyWindow(yurlungur.UIWindow):
        WindowID = 'unique_window_id'
        WindowName = 'My Window'
    
        def __init__(self, parent=None, **kwargs):
            super(MyWindow, self).__init__(parent, **kwargs)
            
    def main():
        MyWindow.show()
    
    if __name__ == '__main__':
        main()



Shell
-------------------

Yurlungur は各アプリケーションに内蔵されたPythonインタプリタをラップします。

ターミナルからの起動とコードからの起動の２つをサポートします。

例えば、SubstancePainter上で Maya のモデルデータを出力したりするときに便利です。


.. code-block:: python

    import yurlungur
    yurlungur.maya.shell("yurlungur.file.open('sample.ma')")


コマンドラインからの起動にも対応しています。


.. code-block:: bash

    python -m yurlungur -h
    
    usage: yurlungur.tool.standalone._cli [-h] [--command cmd app] [--environ mod]
                                          [--qt] [--ptvsd] [--shotgun]
    
    optional arguments:
      -h, --help            show this help message and exit
      --command cmd app, -c cmd app
                            program passed in as string (terminates option list)
      --environ mod, -e mod
                            set ENV settings for module
      --qt, -q              install Qt for Python.
      --ptvsd, -p           install ptvsd modules.
      --shotgun, -s         install shotgun modules.



Debug
-------------------

このライブラリは開発にPycharm Professionalを使用しています。Vscodeで開発を行う方も多いようです。

このモジュールはそれぞれのデバッガーをラップしたモジュールを提供しています。

デバッグしたいアプリケーションに yurlungur と使用するエディターのデバッガーモジュールのパスを通します。

スクリプトエディタ等で共通の下記Pythonスクリプトを実行します。


.. code-block:: python

    import yurlungur
    yurlungur.remote_debug_listen()
    
    
Pycharm (Use Pro.)
------------------------------

リモートデバッグの設定を行います。


VSCode
------------------------------

リモートデバッグの設定を行います。

