---------------
メモ
---------------

#. Node ベース  Maya Houdini Substance Nuke
#. Stack ベース 3dsMax Blender Unreal Davinci

- restructuredtext の記入
- docstring の記入
- test case の記入


cymelは、pymelのように全てのMayaコマンドのラッパーを提供しません。 また、全てのノードタイプのクラスを提供するものの、APIやコマンドを完全に置き換えるほどの機能は提供しません。 頂点やポリゴンなどのコンポーネントもラップしません。

しかし、ノードやプラグを扱う上での主要な機能は整っているので、それで足りない部分はコマンドやAPIを併用してください。


双方向
-----------------------------------

短くシンプルなスペルでオブジェクトベースのAPI
双方向通信: コマンドライン、RPC、GoZ/LiveLink

https://help.autodesk.com/view/MAYAUL/2016/JPN/?guid=__files_Shapes_Shapes_in_Maya_htm

Node Attribute

Component Transform Mesh Material Texture

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

python -m pip install -r requirements.txt -t .

yurlungur.ext.UIWindow
yurlungur.ext.Assets
yurlungur.ext.Publish
yurlungur.ext.vfxtest
yurlungur.ext.mkdocs