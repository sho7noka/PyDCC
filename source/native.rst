:orphan:

============================================
native Foundation (under development)
============================================


言語に詳しい開発者がDCCツールに詳しいことはまれです。
Mayaのことを多少知っていても、HoudiniとPhotoshopに詳しいエンジニアはほとんどいません。
静的な言語を普段書いている開発者は動的スクリプト言語でカスタマイズする機会はまれです。

native
--------------------------------------------

TAはアーティストとエンジニアを繋ぐ稀有な存在ですが、
自社エンジンにネイティブコードをコントリビュートする機会は少ないです。
アーティスト志向ではない内製ツールをより便利にするためには部署間の交渉がつきものですが、
多くの場合、それらの改善は遅々として進みません。

artist
あの機能が使いにくい、もっと簡単にしてほしい
少しの修正や互換性のないアトリビュートの補完のためにもう一度DCCツールに戻るのはめんどくさい。

developper
優先度が低い割に機能を理解して実装するコストが高い
どうすればいいのか詳細な仕様を教えてもらえませんか

native は開発者に最小限の労力でアセット作成ツール間の連携機能を提供します。


.. code-block:: cpp

    #include native.h

    using namespace nt;

    nt::use("maya");
    auto node = nt::Node("");
    node->create();
    node.attr();
    nt::end();


APIを通して実際の処理を行うのはもちろん、詳細なパイプラインはTAに委任させるためには
pybind11 のエイリアスである eval メソッドをコールします。

main 関数内で呼ぶことで簡易的なcliの提供も可能です。


.. code-block:: cpp

    #include native.h

    using namespace nt;

    int main() {

    }
    

自社エンジンに関わらず、DCCアプリケーション間のやり取りも
ホストアプリに組み込むことでイテレーション速度の向上が期待できます。
特に標準でPythonInterpreterの提供を行っていないアプリにプラグイン形式で組み込むことで
相互運用が簡単に実現できます。


.. code-block:: cpp

    #include <openmaya.h>
    #include native.h
    #include yurlungur-native.h

    yr::use(maya);
    yr::YNode().create();
    yr::end();


精緻な絵を描いたりリアルなモデリングを開発者がすることは難しいですが、
グラフィクスAPIに沿ったデータをDCCツールからc++を通して取り出すのは簡単です。


# Native imprimentations


## なぜ
- インハウスツールの拡張性は低い傾向にある
- DCCツールの操作に詳しいグラフィクス・システムエンジニアは希少
- 小さな連携のためにSDKとドキュメントを読むのが面倒

データ構造の互換性やプロセス間通信などの緊密な統合に関して、

それぞれのツールSDKを読み込む必要があります。

ネイティブからapiコール
pluginパッケージから読み取り

embeded.h
---------------------------------------------

#. (埋込) エディタ(dll)内にCapiを組み込む
#. Python インタープリター不要
#. 競合他社間のソフトウェア統合


.. code-block:: make

    cmake_minimum_required(VERSION 3.0)
    project(yurlungur)
    
    find_package(pybind11 REQUIRED)  # or add_subdirectory(pybind11)
    
    add_executable(yurlungur main.cpp)
    target_link_libraries(yurlungur PRIVATE pybind11::embed)


.. code-block:: cpp

    #include <pybind11/embed.h>
    #include <yurlungur/embeded.h>
    
    namespace py = pybind11;
    
    PYBIND11_EMBEDDED_MODULE(cpp_module, m) {
        m.attr("a") = 1;
    }
    
    int main() {
        py::scoped_interpreter guard{};
    
        auto py_module = py::module::import("py_module");
    
        auto locals = py::dict("fmt"_a="{} + {} = {}", **py_module.attr("__dict__"));
        assert(locals["a"].cast<int>() == 1);
        assert(locals["b"].cast<int>() == 2);
    
        py::exec(R"(
            c = a + b
            message = fmt.format(a, b, c)
        )", py::globals(), locals);
    
        assert(locals["c"].cast<int>() == 3);
        assert(locals["message"].cast<std::string>() == "1 + 2 = 3");
    }


.. code-block:: python

    """py_module.py located in the working directory"""
    import cpp_module
    
    a = cpp_module.a
    b = a + 1


extension.h
------------------------------------------

#. (拡張) SDKをPython Capiから呼び出す
#. 内蔵インタプリタのイニシャライズが必要
#. pybind11 のラッパー


Build
--------------------------------------------------------------


.. code-block:: bash

    cmake_minimum_required(VERSION 3.0)
    project(example)
    
    add_subdirectory(pybind11)
    pybind11_add_module(example example.cpp)


Bindings
---------------------------------------------------------------


.. code-block:: cpp

    #include "string"
    
    class Node {
        Node(const std::string &name) : name(name) { }
        void setName(const std::string &name_) { name = name_; }
        const std::string &getName() const { return name; }
    
        std::string name;
    };
    
    struct File {
        void import(const std::string file_name);
        void export(const std::string file_name);
    
        std::string path;
    }
    
    struct Shell {
    
    }


Extension
----------------------------------------------------


.. code-block:: cpp

    #include <pybind11/pybind11.h>
    #include <yurlungur/extension.h>
    
    namespace py = pybind11;
    
    PYBIND11_MODULE(example, m) {
        py::class_<Node>(m, "Node")
            .def(py::init<const std::string &>())
            .def("setName", &Node::setName)
            .def("getName", &Node::getName);
    
        py::class_<File>(m, "File")
            .def("import", $File::import);
    }

