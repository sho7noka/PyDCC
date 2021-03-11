===================
tool
===================

Yurlungur は各アプリケーションに内蔵されたPythonインタプリタをラップします。
ターミナルからの起動とコードからの起動の２つをサポートします。

シェル
-------------------

> python
> import yurlungur
> yurlungur.maya.shell("yurlungur.file.open('sample.ma')")

例えば、SubstanceDesigner から Maya のモデルデータを出力したりするときに便利です。


コンソール
-------------------

python -m yurlungur


===================================
Debug
===================================

このライブラリは開発エディタにPycharm Professionalを使用しています。
各種アプリケーションのテスト・リモートデバッグ作業に便利なモジュールを
user フォルダに内包しているので、開発効率をあげる手助けになります。


Pycharm
---------------

.. code-block:: python

    import pyvsd


VSCode
---------------

.. code-block:: python

    import pydevd

