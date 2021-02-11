# -*- coding: utf-8 -*-
import sys
import unittest

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core.env import _Houdini

@unittest.skipUnless(_Houdini(), "Houdini is not found")
class TestHoudini(unittest.TestCase):

    def test_hou(self):
        print (yr.name, yr.version)

    def test_node(self):
        print (yr.YObject('obj'))

    @unittest.skip("only runtime")
    def test_attr(self):
        yr.YObject('obj').create('geo')

    @unittest.skip("")
    def test_file(self):
        yr.File.save('temp.hip')


if __name__ == '__main__':
    unittest.main()
