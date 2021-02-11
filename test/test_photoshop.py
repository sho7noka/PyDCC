# coding: utf-8
import sys
import unittest

sys.path.append("../yurlungur")

import yurlungur as yr
from yurlungur.core.env import _Photoshop
from yurlungur.core.deco import Windows


@unittest.skipUnless(_Photoshop(), "Photoshop is not found")
class TestPhotoshop(unittest.TestCase):

    @unittest.skip("only runtime")
    def test_cmds(self):
        # print yr.YObject("aaa").create(kind="layer/black")
        with yr.UndoGroup("undo"):
            node = yr.YObject("nnn")
            print (node.opacity)
            print (node.name)
            node.hide()
            node.select("aaa")
            print(yr.File().current)

    # @unittest.skipIf(not Windows(), "only windows")
    @unittest.skip("")
    def test_layer(self):
        yr.YObject("test").create("Normal")
        yr.YObject("test").AutoContrast()
        print(yr.YObject("test").parent())
        print(yr.YObject("test").blendMode)
        print(yr.YObject("test").attr("blendMode"))
        yr.YObject("test").opacity.set(3)
        yr.YObject("test")("test1")
        yr.YObject("test1").hide(False)
        print(yr.YObject("test1").instance())
        yr.YObject("test1").delete()
        print(yr.YObject("BBB").children())

    # @unittest.skipIf(not Windows(), "only windows")
    @unittest.skip("")
    def test_file(self):
        yr.file.save("%USER%\\Documents\\Adobe\\ccd.psd")
        yr.file.open("%USER%\\Documents\\Adobe\\ccc.psd")
        print(yr.file.current)


if __name__ == "__main__":
    unittest.main()
