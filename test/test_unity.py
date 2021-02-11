# coding: utf-8
import sys
import unittest

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core.env import _Unity


@unittest.skipUnless(_Unity(), "Unity is not found")
class MyTestCase(unittest.TestCase):

    @unittest.skip("only runtime")
    def test_something(self):
        cube = yr.Node("Cu")
        # import UnityEngine
        # pprint = UnityEngine.Debug.Log
        from System import Array, Console
        import System
        # a = yr.env.__import__("UnityEngine")
        # yr.YNode("Cu").attr("MeshRenderer").castShadows
        # print yr.YNode("GameObject").name
        # for trm in yr.YNode("Cu").children():
        #	pprint(trm.__name__)
        # pprint(yr.YObject("Cube").id)
        # cube.instance()
        # yr.YObject("Cube").hide()
        # yr.YNode("Cu").create("TextMesh")

        # pprint(dir(cube.Transform)[15])
        # pprint(cube.attr("Renderer").name)

        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
