===================================
Getting Started
===================================

このモジュールは cymel の考えに近いノード操作に絞った機能を提供します。

cymelは、pymelのように全てのMayaコマンドのラッパーを提供しません。 また、全てのノードタイプのクラスを提供するものの、APIやコマンドを完全に置き換えるほどの機能は提供しません。 頂点やポリゴンなどのコンポーネントもラップしません。

しかし、ノードやプラグを扱う上での主要な機能は整っているので、それで足りない部分はコマンドやAPIを併用してください。


オブジェクト構成
-----------------------------------

#. Node ベース  Maya Houdini Substance Nuke Fusion
#. Stack ベース 3dsMax Blender Unreal Unity Davinci

Node
    Attribute
        Transform
    Component 
        Mesh Material Texture


ツールセット
-----------------------------------

API UI ジェネリック FabricEngine
test document publish or chat

(polygonflow) か trimesh か https://github.com/maajor/pyhapi
#. https://github.com/Peter92/vfxwindow
#. https://github.com/martin-chatterjee/vfxtest
#. https://github.com/PaulSchweizer/vfx-testrunner

(vfxdoc)
ドキュメント制作で必要になる項目
markdown(rstじゃないです)
メンテナンスがめんどくさい
共有ライブラリの中身まで出力
ツールとの統合具合
画像がないのが悲しい

モンキーパッチは必要かもしれない
共通APIでツール開発、ドキュメント+テスト
環境の実現


Developer
------------------------------------

