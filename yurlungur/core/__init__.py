from yurlungur.core.app import application, use, initialize
from yurlungur.core import env
from yurlungur.core.command import file, node, attr
from yurlungur.core.deco import UndoGroup, cache, threads, timer
# from yurlungur.core.datatype import Vector, Matrix, Color

if env.Maya() or env.Houdini() or env.Substance() or env.Nuke() or env.Davinci() or env.Rumba() or env.C4D():
    from yurlungur.core.proxy import Node
else:
    from yurlungur.core.proxy import Object as Node
from yurlungur.core.proxy import File

del app, command, deco, proxy
