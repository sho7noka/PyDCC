# coding: utf-8
import sys
import unittest

sys.path.append('../yurlungur')
import yurlungur as yr
from yurlungur.core.env import _Nuke


@unittest.skipUnless(_Nuke(), "Maya is not found")
class TestResolve(unittest.TestSuite):

    @unittest.skip("")
    def test_node(self):
        yr.Node("").create("TimeWarp")

        if hasattr(yr.meta, "knob"):
            import nuke
            b = nuke.toNode("aaa")
            k = nuke.Array_Knob("name", "label")
            b.addKnob(k)


if __name__ == '__main__':
    unittest.main()
