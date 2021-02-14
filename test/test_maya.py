# -*- coding: utf-8 -*-
import sys
import unittest

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core.env import _Maya

from time import time
from random import uniform as ru


@unittest.skipUnless(_Maya(), "Maya is not found")
class TestMaya(unittest.TestCase):
    def test_env(self):
        assert _Maya()

    @unittest.skip("only runtime")
    def test_maya(self):
        yr.maya.shell("import yurlungur as yr; print yr.name")

    @unittest.skip("only runtime")
    def test_objs(self):
        yr.maya.file(new=1, f=1)
        cone, shape = yr.maya.polyCone()
        node = yr.Object(shape)
        node.attr("castsShadows").set(1)

    @unittest.skip("only runtime")
    def test_cmds(self):
        from maya import cmds

        i = 0
        start = time()
        while i < 1000:
            cube = cmds.polyCube()[0]
            cmds.setAttr(cube + ".tx", ru(-5, 5))
            cmds.setAttr(cube + ".ty", ru(-5, 5))
            cmds.setAttr(cube + ".tz", ru(-5, 5))
            tx = cmds.getAttr(cube + ".tx")
            ty = cmds.getAttr(cube + ".ty")
            tz = cmds.getAttr(cube + ".tz")
            print((tx, ty, tz))
            i += 1
        end = time() - start
        print(end)

    @unittest.skip("only runtime")
    def test_pymel(self):
        from pymel import core as pm

        i = 0
        start = time()
        while i < 1000:
            cube = pm.polyCube()[0]
            cube.t.set((ru(-5, 5), ru(-5, 5), ru(-5, 5)))
            print(cube.t.get())
            i += 1
        end = time() - start
        print(end)

    @unittest.skip("only runtime")
    def test_cymel(self):
        from maya import cmds
        from cymel.all import *
        i = 0
        start = time()
        while i < 1000:
            cube = cm.O(cmds.polyCube()[0])
            cube.t.set((ru(-5, 5), ru(-5, 5), ru(-5, 5)))
            print(cube.t.get())
            i += 1
        end = time() - start
        print(end)

    @unittest.skip("only runtime")
    def test_cmdx(self):
        import cmdx
        i = 0
        start = time()
        while i < 1000:
            obj = cmdx.createNode("transform", "pCube")
            shape = cmdx.createNode("mesh", parent=obj)
            cube = cmdx.createNode("polyCube")
            cmdx.connectAttr(cube + ".output", shape=".inMesh")
            obj["t"] = (ru(-5, 5), ru(-5, 5), ru(-5, 5))
            print(obj["t"])
            i += 1
        end = time() - start
        print(end)

    @unittest.skip("only runtime")
    def test_yurlungur(self):
        i = 0
        start = time()
        while i < 1000:
            cube = yr.Node(yr.maya.polyCube()[0])
            cube.tx.set(ru(-5, 5))
            cube.ty.set(ru(-5, 5))
            cube.tz.set(ru(-5, 5))
            print(cube.tx, cube.ty, cube.tz)
            i += 1
        end = time() - start
        print(end)


if __name__ == '__main__':
    unittest.main()
