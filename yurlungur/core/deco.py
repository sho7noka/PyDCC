# -*- coding: utf-8 -*-
import sys
import time
import traceback
import functools
import threading
import platform
import multiprocessing
import contextlib

if sys.version_info > (3, 2):
    from contextlib import ContextDecorator
else:
    try:
        from contextlib2 import ContextDecorator
    except ImportError:
        class ContextDecorator(object):
            def __call__(self, fn):
                @functools.wraps(fn)
                def decorator(*args, **kw):
                    with self:
                        return fn(*args, **kw)

            def __enter__(self):
                return self

            def __exit__(self, type, value, tb):
                # Do whatever cleanup.
                if any((type, value, tb)):
                    raise (type, value, tb)

from yurlungur.tool.meta import meta
from yurlungur.core import env, logger

# assign UndoGroup
if env.UE4():
    UndoGroup = meta.ScopedEditorTransaction

elif env.Houdini():
    UndoGroup = meta.undos.group

elif env.Substance():
    UndoGroup = meta.sd.UndoGroup

elif env.Max():
    UndoGroup = functools.partial(meta.undo, True)

elif env.Nuke():
    UndoGroup = meta.Undo

else:
    class UndoGroup(ContextDecorator):
        """
        undoGroup for with statements.
    .
        >>> import yurlungur
        >>> with yurlungur.UndoGroup("undo group"):
        >>>     for node in "hoge", "fuga", "piyo":
        >>>         yurlungur.YNode(node).delete()
        """

        def __init__(self, label):
            self.label = label

        def __enter__(self):
            if env.Maya():
                meta.undoInfo(ock=1)

            elif env.Photoshop():
                self.label = (
                    meta.doc.activeHistoryState if Windows()
                    else meta.doc.currentHistoryState().get()
                )

            elif env.C4D():
                meta.doc.StartUndo()

            elif env.Davinci():
                meta.fusion.StartUndo()

            elif env.Blender():
                self.label = 0

            elif env.Rumba():
                meta.modify_begin()

            # https://answers.unity.com/questions/1587818/how-to-undo-a-lot-of-created-objects-at-once-2.html
            elif env.Unity():
                meta.editor.Undo.IncrementCurrentGroup()
                meta.editor.Undo.SetCurrentGroupName(self.label)
                self.index = meta.editor.Undo.GetCurrentGroup()

            return self

        def __exit__(self, exc_type, exc_value, traceback):
            if env.Maya():
                meta.undoInfo(cck=1)

            elif env.Photoshop():
                from yurlungur.adapters import photoshop

                if Windows():
                    meta.doc.activeHistoryState = self.label
                else:
                    meta.doc.currentHistoryState().setTo_(self.label)

                photoshop.do("undo")

            elif env.C4D():
                meta.doc.EndUndo()

            elif env.Davinci():
                meta.fusion.EndUndo()

            elif env.Blender():
                meta.ops.ed.undo_history(item=self.label)
                meta.ops.ed.redo()

            elif env.Rumba():
                meta.modify_end()
                # meta.undo_blend(self.label)

            elif env.Unity():
                meta.editor.Undo.CollapseUndoOperations(self.index)


def cache(func, *args, **kwargs):
    """
    Substance, Blender and Davinch use lcu_cache at Python3.

    Args:
        func:
        *args:
        **kwargs:

    Returns:

    """
    saved = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args in saved:
            return saved[args]
        result = func(*args)
        saved[args] = result
        return result

    return wrapper if sys.version_info < (3, 2) else functools.lcu_cache(*args, **kwargs)


def trace(func):
    """
    message util

    Args:
        func:

    Returns:

    """
    try:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                if hasattr(logger.logger, "warning"):
                    logger.logger.warning(traceback.format_exc())
                else:
                    logger.logger.log(traceback.format_exc(), logger.Warning)
    except (NameError, ImportError):
        wrapper = func

    return wrapper


def timer(func):
    """
    timeit

    Args:
        func:

    Returns:

    """
    import yurlungur

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        yurlungur.logger.pprint(
            '{0} start'.format(func.__name__)
        )
        start_time = time.clock()
        ret = func(*args, **kwargs)
        end_time = time.clock()
        yurlungur.logger.pprint(
            '\n{0}: {1:,f}s'.format("total: ", (end_time - start_time))
        )
        return ret

    return wrapper


@contextlib.contextmanager
def threads(func):
    """
    with statements for threads.
    available for Maya, Houdini, Nuke, 3dsMax, Substance Blender and Cinema 4D
    >>>
    :param func:
    :return:
    """

    # https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/c4d.threading/index.html
    if env.C4D():
        from c4d.threading import C4DThread
        class _Thread(C4DThread):
            def Main(self):
                func()

        t = _Thread()
        t.Start()
        # Do some other operations here
        t.Wait(True)

    elif env.Substance():
        class _Thread(threading.Thread):
            def run(self):
                func()
                return

        t = _Thread()
        t.start()

    else:
        t = threading.Thread(target=__worker, args=(func,))
        t.daemon = True
        t.start()
        t.join()


def __worker(func):
    """
    thread runner

    Args:
        func:

    Returns:

    """
    if env.Maya():
        import maya.utils as utils
        utils.executeDeferred(func)

    # https://forums.odforce.net/topic/22570-execute-in-main-thread-with-results/
    elif env.Houdini():
        import hdefereval

        n = 0
        while n < multiprocessing.cpu_count() + 1:
            hdefereval.executeInMainThreadWithResult(func)
            n += 1

    elif env.Nuke():
        meta.executeInMainThreadWithResult(func)

    elif env.Max():
        try:
            func.acquire()
            with meta.mxstoken():
                func()
        except:
            raise
        finally:
            if func.locked():
                func.release()

    return func


def Windows(func=None):
    """
    is Windows expression and decorator

    Args:
        func:

    Returns:

    """
    if func is None:
        return platform.system() == "Windows"

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() == "Windows":
            return func(*args, **kwargs)

    return wrapper


def Linux(func=None):
    """
    is Linux expression and decorator

    Args:
        func:

    Returns:

    """
    if func is None:
        return platform.system() == "Linux"

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() == "Linux":
            return func(*args, **kwargs)

    return wrapper


def Mac(func=None):
    """
    is macOS expression and decorator

    Args:
        func:

    Returns:

    """
    if func is None:
        return platform.system() == "Darwin"

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() == "Darwin":
            return func(*args, **kwargs)

    return wrapper
