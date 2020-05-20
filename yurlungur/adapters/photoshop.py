# coding: utf-8
import os
from yurlungur.core import env
from yurlungur.core.deco import Windows, Mac

if Windows():
    if not env.__import__("comtypes"):
        env.pip.main(["install", "comtypes"])

    from comtypes.client import GetActiveObject
    from comtypes.gen import Photoshop

    app = GetActiveObject("Photoshop.Application")
    if app:
        setattr(app, "isRunning", True)
    psd = Photoshop

elif Mac():
    if not env.__import__("ScriptingBridge"):
        if env.Maya():
            cmd = env._Maya().replace("bin/maya", "bin/mayapy") + " -m pip install pyobjc-framework-ScriptingBridge"
            os.system(cmd)
        else:
            env.pip.main(["install", "pyobjc-framework-ScriptingBridge"])

    from ScriptingBridge import SBApplication

    app = SBApplication.applicationWithBundleIdentifier_("com.adobe.photoshop")
    psd = None

run = None
end = None


class Document(object):
    """
    >>> app.Document()
    """

    def __init__(self):
        self._doc = app.activeDocument if Windows() else app.currentDocument()

    def __repr__(self):
        return self._doc.name if Windows() else self._doc.name()

    def __getitem__(self, val):
        if isinstance(val, int):
            self._doc = app.documents[val] if Windows() else app.documents()[val]

        if isinstance(val, str):
            if Windows():
                for i, doc in enumerate(app.documents):
                    if doc.name == val:
                        self._doc = app.documents[i]
            else:
                for i, doc in enumerate(app.documents()):
                    if doc.name() == val:
                        self._doc = app.documents()[i]
        return self._doc

    @property
    def layers(self):
        return Layer(self._doc)


class Layer(object):
    """
    >>> app.Document().layers.add()
    """

    def __init__(self, document):
        self._doc = document
        self._layer = (
            self._doc.activeLayer if Windows() else self._doc.currentLayer()
        )

    def __repr__(self):
        return str(self._layer.name if Windows() else self._layer.name())

    def __getitem__(self, val):
        if isinstance(val, int):
            self._layer = (
                self._doc.artLayers[val]
                if Windows() else self._doc.artLayers()[val]
            )

        if isinstance(val, str):
            if Windows():
                for layer in self._doc.artLayers:
                    if layer.name == val:
                        self._layer = layer
            else:
                for layer in self._doc.artLayers():
                    if layer.name() == val:
                        self._layer = layer
        return self._layer

    def rmv(self):
        self._layer.delete()


def do(cmd):
    """
    photoshop script runner
    """
    assert len(cmd) == 4 and ("'" not in cmd)

    if Windows():
        app.DoJavaScript("""
            executeAction(charIDToTypeID("%s"), undefined, DialogModes.NO);
        """ % cmd)
    else:
        osa = "osascript -e "
        osa += "'tell application \"%s\" " % str(app).split("\"")[1]
        osa += "to do javascript "
        osa += "\"executeAction(charIDToTypeID(\\\"%s\\\"), undefined, DialogModes.NO);\"'" % cmd
        os.system(osa)
