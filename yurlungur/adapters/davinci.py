# coding: utf-8
import os
from yurlungur.core.env import App as __App


class Render(object):
    def __init__(self, project):
        self.project = project
        self.jobs = project.GetRenderJobs()
        self.presets = project.GetRenderPresets()
        self.formats = project.GetRenderFormats()
        # GetCurrentRenderFormatAndCodec

    def add(self):
        self.project.AddRenderJob()

    def start(self, *args):
        """args 無しも可能"""
        self.project.StartRendering(*args)

    def stop(self):
        if self.project.IsRenderingInProgress():
            self.project.StopRendering()

    def delete(self, *args):
        if len(args) == 0:
            self.project.DeleteAllRenderJobs()
        else:
            self.project.DeleteRenderJobIndex(args[0])


class Projects(object):

    def __init__(self):
        from yurlungur.tool.meta import meta
        self.manager = meta.resolve.GetProjectManager()
        self.project = self.manager.GetCurrentProject()
        self.projects = self.manager.GetProjectListInCurrentFolder()

    def __repr__(self):
        return self.project.GetName()

    def __getitem__(self, val):
        if val in self.projects:
            self.project = self.manager.LoadProject(val)
        else:
            self.project = self.manager.CreateProject(val)

        return self

    @property
    def sequences(self):
        return Timeline(self.project)

    @property
    def render(self):
        return Render(self.project)


class Timeline(object):
    def __init__(self, project):
        self.project = project
        self.timeline = project.GetCurrentTimeline()
        self.media = project.GetMediaPool()
        self.clips = self.media.GetRootFolder().GetClips().values()

    def __repr__(self):
        return self.timeline.GetName() + self.timeline.GetCurrentTimecode()

    def __getitem__(self, val):
        assert isinstance(val, (str, int))

        if type(val) == int:
            if 0 < val < self.project.GetTimelineCount():
                self.timeline = self.project.GetTimelineByIndex(val)

        elif type(val) == str:
            if os.path.exists(val):
                self.timeline = self.media.ImportTimelineFromFile(val)
            elif val in [v.GetName() for v in self.clips]:
                self.project.SetCurrentTimeline(val)
                self.timeline = self.project.GetCurrentTimeline()
            else:
                self.timeline = self.media.CreateEmptyTimeline(val)

        return self

    def imports(self, *args):
        self.media.AppendToTimeline(*args)
        self.timeline = self.project.GetCurrentTimeline()
        return self

    @property
    def tracks(self):
        return Track(self.timeline)


class Track(object):
    def __init__(self, timeline):
        self.timeline = timeline
        self.track = timeline.GetCurrentVideoItem()

    def __repr__(self):
        return self.track.GetName()

    def __getitem__(self, val):
        assert isinstance(val, int)

        if 0 < val < self.timeline.GetTrackCount("video"):
            self.track = self.timeline.GetItemsInTrack("video", val)
        return self

    @property
    def clips(self):
        return Item(self.track)


class Item(object):
    def __init__(self, track):
        self.track = track

    def __repr__(self):
        return self.track.GetName() + self.track.GetDuration()

    def __getitem__(self, val):
        assert isinstance(val, (str, int))

        if type(val) == int:
            if 0 < val < self.track.GetFusionCompCount():
                self.track = self.track.GetFusionCompByIndex(val)

        elif type(val) == str:
            for v in self.track.GetFusionCompNames().values():
                if val in v.GetName():
                    self.track = self.track.GetFusionCompByName(val)
            if os.path.exists(val):
                self.track = self.track.ImportFusionComp(val)
                self.track = self.track.LoadFusionCompByName(val)
            else:
                self.track = self.track.AddFusionComp()
                self.track.RenameFusionCompByName(self.track.GetName(), val)

        return self

    def exports(self, path):
        return self.track.ExportFusionComp(path, 1)

    def delete(self, name):
        return self.track.DeleteFusionCompByName(name)


# clips
# clips = resolve.GetMediaStorage().AddItemsToMediaPool(paths)
# clips.GetClipProperty()
# clips.SetClipProperty(n, v)

run, _, end, _ = __App("davinci")._actions
