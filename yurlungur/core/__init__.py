from yurlungur.core.app import application, use
from yurlungur.core.command import cmd, file, node
from yurlungur.core.deco import UndoGroup, cache, threads, timer
from yurlungur.core import env
from yurlungur.core.logger import pprint
from yurlungur.core.proxy import YFile, YColor, YVector, YMatrix

if env.Maya() or env.Houdini() or env.Substance() or env.Nuke() or env.Davinci() or env.Rumba():
    from yurlungur.core.proxy import YNode
else:
    from yurlungur.core.proxy import YObject

del app, command, deco, logger, proxy
