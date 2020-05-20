# -*- coding: utf-8 -*-
from yurlungur.core.wrapper import YMObject

meta = YMObject()


def __make_completer(mod):
    """
    make each meta modules

    Args:
        mod:

    Returns:

    """
    import os
    import inspect

    local = os.path.dirname(os.path.dirname(inspect.currentframe().f_code.co_filename))
    completer = os.path.join(local, "user", "completer.pyi").replace(os.sep, "/")

    header = "\"\"\"this document generated by internal module.\"\"\"\n\n\n"
    module = __import__(mod)
    with open(completer, "w") as f:
        f.write(header)

        for fn, _ in inspect.getmembers(module):
            if fn.startswith("_"):
                continue

            f.write("def {0}(*args, **kwargsargs):\n".format(fn))
            f.write("   \"\"\"{0}\"\"\"\n".format(inspect.getdoc(fn)))
            f.write("   pass\n\n")
