# -*- coding: utf-8 -*-
import sys
import unittest

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core.env import _Blender


@unittest.skipUnless(sys.version_info > (3, 2), "Blender is Python3 over")
class TestBlender(unittest.TestCase):
    def test_env(self):
        assert _Blender()

    @unittest.skip("")
    def test_cli(self):
        yr.blender.shell("import bpy; print(bpy)")

    @unittest.skip("only runtime")
    def test_cmds(self):
        # yr.meta.file(new=1, f=1)
        node = yr.YObject("shape")
        node.attr("castsShadows").set(1)
        yr.Node("").create()


if __name__ == '__main__':
    unittest.main()
