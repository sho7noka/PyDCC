# coding: utf-8
import sys
import unittest

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core.env import _Substance


@unittest.skipUnless(_Substance(), "Substance is not found")
class TestSubstance(unittest.TestCase):

    @unittest.skip("only runtime")
    def test_cmds(self):
        with yr.UndoGroup("undo"):
            print(dir(yr))
            node = yr.Node().create("uniform")

            print(node, node.attr("$pixelsize"), node.attrs)
            normal = yr.Node().create("normal")
            print(normal)

            node.connect("unique_filter_output", normal, "inputNodeOutput.connector")
            print(node.parent())
            node.disconnect("unique_filter_output")
            print(node.parent())

    @unittest.skip("only runtime")
    def test_file(self):
        yr.File.open("")


if __name__ == '__main__':
    unittest.main()
