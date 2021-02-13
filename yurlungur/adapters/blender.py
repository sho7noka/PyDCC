# coding: utf-8
import sys as __sys

try:
    __sys.modules[__name__] = __sys.modules["bpy"]
except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, end, connect = __App("blender")._actions

    __all__ = ["run", "shell", "end", "connect"]


class Project(object):
    def __init__(self, project):
        self.project = project

    @property
    def sequences(self):
        return Timeline(self.project)


class Timeline(object):
    def __init__(self, timeline):
        self.timeline = timeline

    @property
    def tracks(self):
        return Track(self.timeline)


class Track(object):
    def __init__(self, track):
        self.track = track

    @property
    def clips(self):
        return Item(self.track)


class Item(object):
    pass

"""
import bpy
import queue
import contextlib

- logging
- threads
- undogroup

execution_queue = queue.Queue()


# This function can savely be called in another thread.
# The function will be executed when the timer runs the next time.
def run_in_main_thread(function):
    execution_queue.put(function)


def execute_queued_functions():
    while not execution_queue.empty():
        function = execution_queue.get()
        function()
    return 1.0


@contextlib.ContextManager
def threads():
    bpy.app.timers.register(execute_queued_functions)


try:
    pass
finally:
    bpy.app.timers.unregister(execute_queued_functions)

# https://docs.blender.org/api/blender2.8/bpy.types.Theme.html#bpy.types.Theme.info

# remove other Recent Reports
reports = [bpy.data.texts.remove(t, do_unlink=True)
           for t in bpy.data.texts
           if t.name.startswith("Recent Reports")]
# make a report
bpy.ops.ui.reports_to_textblock()
# print the report
for line in bpy.data.texts["Recent Reports"].lines:
    # if line.body.startswith("Operator:"): #it's an operator
    print(line.body)


class UndoGroup:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, 'r')

        return self.file

    def __exit__(self, type, value, traceback):
        self.file.close()

        # Redo specific action in history
        # Parameters:
        # item (int in [0, inf], (optional)) – Item
        bpy.ops.ed.undo_history(item=0)

        # Add an undo state (internal use only)
        # Parameters:
        # message (string, (optional, never None)) – Undo Message
        bpy.ops.ed.undo_push(message="Add an undo step *function may be moved*")

        # Undo and redo previous action
        bpy.ops.ed.undo_redo()
"""
