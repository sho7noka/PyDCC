# -*- coding: utf-8 -*-
import sys

assert sys.version_info > (2, 7), ('yurlungur currently requires Python 2.7 later')
sys.dont_write_bytecode = True

from yurlungur.core import *  # noQA
from yurlungur.tool.meta import meta  # noQA
from yurlungur.tool.standalone import *  # noQA

# info
__all__ = []
__version__ = "0.9.8"
name = __name__
version = __version__

# to dispatch
sys.exit = None
del sys
