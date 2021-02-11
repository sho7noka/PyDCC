from yurlungur.core.app import application, use, initialize
from yurlungur.core.command import cmd, file, node
from yurlungur.core.deco import UndoGroup, cache, threads, timer
from yurlungur.core import env
from yurlungur.core.proxy import File

# from yurlungur.core.datatype import Vector, Matrix, Color

if env.Maya() or env.Houdini() or env.Substance() or env.Nuke() or env.Davinci() or env.Rumba() or env.UE4():
    from yurlungur.core.proxy import Node
else:
    from yurlungur.core.proxy import Object as Node

del app, command, deco, proxy
