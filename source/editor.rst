===================================
Editor tips
===================================
デコレータと  ｔ


print
-------------------------------
print statement is not available in Python3.
Also IronPython is not bind with __future__ modules.

print 文は Python3 ではエラーになり、それを回避するための
__future__ モジュールも IronPython ではサポートされないため、
`yurlungur.pprint(*args)` の使用をお勧めします。


.. code-block:: python

    yurlungur.pprint(*args)

内部処理に pformat を使っているため、ログが見切れるような
長いリストでも視認性は損なわれません。

LogHandler をそれぞれのアプリケーションから継承し、一貫したインターフェースで
出力レベルの制御をします。


UndoGroup
-------------------------------
contextManager で制御されたUndoGroup で
アプリケーション側のUndoで操作を巻き戻すことが出来ます。

.. code-block:: python

    with yr.UndoGroup("undo"):
        yr.YNode("hoge").delete()


もしUndoGroupでインデントを囲わないスクリプト処理をした場合、
ひとつひとつundoを使って元に戻さなければなりません。


GUI
--------------------------------
Qt.py をラッピングしているので、Maya/Houdini といった
大型スタジオで使われるアプリケーションのバージョンを気にすることなく
Python から Qt を使うことが出来ます。

それぞれのDCCアプリケーション特有のウィンドウを取得して
Qt parent に渡すことができます。

.. code-block:: python

    Parent = yr.ui.widgetPtr()
    widget = QWidget(parent)



スタンドアロン起動の際にも他に宣言すべき決まりごとはありません。

.. code-block:: python

    widget = QWidget()
    yr.Qt.show(widget)


ゲームエンジンはQtを内蔵しません。
別途 pip インストールするか、env モジュールでアプリケーションを切り分けて、
meta モジュールからそれぞれネイティブの ui モジュールを参照して下さい。