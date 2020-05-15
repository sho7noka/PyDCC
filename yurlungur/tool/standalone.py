# coding: utf-8
import sys
from yurlungur.adapters import *  # noQA


def _cli(args):
    """
    yurlungur command line parser

    Args:
        args:

    Returns:

    """
    import argparse
    import yurlungur as yr

    parser = argparse.ArgumentParser(
        prog='yurlungur.tool.standalone._cli',
        description="{0} v.{1} {2}".format(yr.name, yr.version, sys.executable),
        epilog='yurlungur console',
        add_help=True,
    )
    parser.add_argument("--command", "-c",
                        help="program passed in as string (terminates option list)",
                        nargs=2, type=str, metavar=("cmd", "app"), )

    parser.add_argument("--dialog", "-d",
                        help="Launch widget if Qt for Python is installed",
                        action="store_true", )

    parser.add_argument("--environ", "-e",
                        help="set ENV settings for module",
                        nargs=1, type=str, metavar="mod", )

    parser.add_argument("--qt", "-q",
                        help="install Qt for Python.",
                        action="store_true", )

    parser.add_argument("--ptvsd", "-p",
                        help="install ptvsd modules.",
                        action="store_true", )

    arguments = parser.parse_args(args)

    if arguments.command:
        cmd, app = arguments.command
        try:
            getattr(sys.modules[__name__], app).shell(cmd)
        except AttributeError:
            print(
                "%s is not found." % app,
                [m for m in dir(sys.modules[__name__]) if not m.startswith("_") and m != "sys"]
            )

    if arguments.dialog:
        from yurlungur.Qt import QtWidgets
        from yurlungur.tool import editor

        app = QtWidgets.QApplication(sys.argv)
        widget = editor.View()
        widget.show()
        sys.exit(app.exec_())

    if arguments.environ:
        from yurlungur.core.app import use
        use(arguments.environ[0])

    if arguments.qt:
        yr.env.pip.main(["install", "PySide2"])

    if arguments.ptvsd:
        yr.env.pip.main(["install", "ptvsd"])


if __name__ == '__main__':
    _cli(sys.argv[1:])
