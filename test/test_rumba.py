# -*- coding: utf-8 -*-
import sys
import unittest

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core.env import _Rumba


@unittest.skipUnless(_Rumba(), "Rumba is not found")
class TestRumba(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_cli(self):
        yr.rumba.run()


if __name__ == '__main__':
    unittest.main()
