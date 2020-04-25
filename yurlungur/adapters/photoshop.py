# coding: utf-8
import os
from yurlungur.core import deco, env

if deco.Windows():
    if not env.__import__("comtypes"):
        env.pip.main(["install", "comtypes"])

    from comtypes.client import GetActiveObject
    from comtypes.gen import Photoshop

    app = GetActiveObject("Photoshop.Application")
    if app:
        setattr(app, "isRunning", True)
    psd = Photoshop

elif deco.Mac():
    if not env.__import__("ScriptingBridge"):
        env.pip.main(["install", "pyobjc-framework-ScriptingBridge"])

    from ScriptingBridge import SBApplication

    app = SBApplication.applicationWithBundleIdentifier_("com.adobe.photoshop")
    psd = None


class Document(object):
    """
    >>> app.Document()
    """

    def __init__(self):
        self._doc = app.activeDocument if deco.Windows() else app.currentDocument()

    def __repr__(self):
        return self._doc.name if deco.Windows() else self._doc.name()

    def __getitem__(self, val):
        if isinstance(val, int):
            self._doc = app.documents[val] if deco.Windows() else app.documents()[val]

        if isinstance(val, str):
            if deco.Windows():
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
            self._doc.activeLayer if deco.Windows() else self._doc.currentLayer()
        )

    def __repr__(self):
        return str(self._layer.name if deco.Windows() else self._layer.name())

    def __getitem__(self, val):
        if isinstance(val, int):
            self._layer = (
                self._doc.artLayers[val]
                if deco.Windows() else self._doc.artLayers()[val]
            )

        if isinstance(val, str):
            if deco.Windows():
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

    if deco.Windows():
        app.DoJavaScript("""
            executeAction(charIDToTypeID("%s"), undefined, DialogModes.NO);
        """ % cmd)
    else:
        osa = "osascript -e "
        osa += "'tell application \"%s\" " % str(app).split("\"")[1]
        osa += "to do javascript "
        osa += "\"executeAction(charIDToTypeID(\\\"%s\\\"), undefined, DialogModes.NO);\"'" % cmd
        os.system(osa)
