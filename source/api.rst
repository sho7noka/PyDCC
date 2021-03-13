===================================
API Foundation
===================================

Object(Node)クラス、Attributeクラス、Fileクラスの基本を知れば、汎用的な操作ができます。


Object&Nodeオブジェクト
--------------------------------
数多くの3Dアプリケーションも、APIのレベルではノードベースとスタックベースに分けることができます。

UnityはComponent、BlenderはModifierでオブジェクトの振る舞いを制御しますが、

Maya や Houdini といったノードベースのアプリケーションでは、接続する同士の相互作用によってシーン全体を制御します。

前者のスタックベースのアプリケーションを使う際には Object、

後者のノードベースのアプリケーションを使う際には Node　がインターフェースの

デザインとして違和感なく使うことが出来ます。

アプリケーションが持つ性質を意識して、NodeとObjectをそれぞれ使いわけてプログラミングすると良いでしょう。


.. code-block:: python

    # 標準ではPython
    import yurlungur as yr

    obj = yr.Object("defaultResolution")

    # or

    node = yr.Node("defaultResolution")


Node is eble to initialize that is subclass for Object.
You have to str object.
Node オブジェクトのみ connection 関係のメソッドを持つ


.. code-block:: python

    node = yr.Node(obj.name)
    print(node.inputs())



Attributeオブジェクト
--------------------------------

これはPyMELをベースにした柔軟なAttributeクラスです。

すべてオブジェクトで扱えるようにアプリケーション間の戻値をラップしています。
これは、getter / setter のインターフェースがアプリケーション間で異なるためです

attr("str") は文字列ベースのアクセスになるので、予め文字列要素で構成したリストを準備すれば短く書くことができます。

Attribute クラスが別設計されたように、戻り値はすべてオブジェクトです。

引数に渡したり set するためには、value プロパティを使って、基本データ型に変更する必要があります。

.. code-block:: python

    width = obj.attr("width") # object YAttr
    yurlungur.log(width.value)



__getitem__ によるアクセスもサポートしているため、

ユーザー側が今操作しているオブジェクトの状態を気にすることなく

はじめからそのプロパティを持っていたかのように振る舞います。

.. code-block:: python

    width = obj.width
    yr.log(width.value)

    width.set(700)



Fileオブジェクト
--------------------------------
アプリケーション間のLiveLinkが主流になりつつありますが、I.Oを一つのインターフェースでまとめておくことは、

今後アプリケーションを使う上で役に立ちます。


.. code-block:: python

    import yurlungur

    yurlungur.file.open("sample.blend")
    yurlungur.file.save("sample.blend")


AlembicやFBX, PixarUSDなど汎用ファイルフォーマットのサポートは、アプリケーションとそのプラグインの実装に依存します。

(例えばゲームエンジンでは、一般的なファイルエクスポート機能はサポートされていません)

アプリケーションがサポートしているファイルフォーマットが利用できる場合、それぞれの拡張子のオブジェクトを

経由することで読み書きを行うことができます。


.. code-block:: python

    yurlungur.file.fbx.Import("sample.fbx")

    yurlungur.file.usd.Export("sample.usd")
    

Nuke や Houdini といったノードベースのアプリケーションは、FileオブジェクトではなくNodeオブジェクトが

戻り値として帰ってきます。