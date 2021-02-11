# -*- coding: utf-8 -*-

def main():
    """
    yurlungur cli entry point
    """
    import sys, os, inspect
    sys.dont_write_bytecode = True

    local = os.path.dirname(os.path.dirname(inspect.currentframe().f_code.co_filename))
    if not local in sys.path:
        sys.path.append(local)

    from yurlungur.tool.standalone import _cli
    _cli(sys.argv[1:])


if __name__ == "__main__":
    main()
