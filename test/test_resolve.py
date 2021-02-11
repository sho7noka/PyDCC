# coding: utf-8
import sys
import unittest

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.adapters import davinci


class TestResolve(unittest.TestSuite):

    @unittest.skip("")
    def test_aaa(self):
        projects = davinci.Projects()
        print (projects.timelines.tracks.comps)
        print (projects["Hellow"].timelines["g"].tracks)

    @unittest.skip("")
    def test_fscript(self):
        # comp起点とfusion起点の２つ
        # https://www.steakunderwater.com/VFXPedia/96.0.243.189/index1bea.html?title=Eyeon:Script/Reference/Applications/Fusion/Classes/Composition
        # print comp.GetToolList().values()[0].GetAttrs()
        # fpath = fusion.MapPath("/Users/shosumioka/Documents/DaVinci Resolve/aaa.comp")
        # mcomp = fusion.LoadComp(fpath)
        # pprint.pprint(mcomp.GetAttrs()['COMPS_FileName'])
        # mcomp.Save(), mcomp.Print(), mcomp.Close(), mcomp.Lock(), mcomp.Unlock(), mcomp.Paste()
        comp = davinci.Fusion().GetCurrentComp()
        bg1 = comp.Background()
        pl1 = comp.Plasma()
        mg1 = comp.Merge({"Background": bg1, "Foreground": pl1})
        comp.FindTool("MediaOut1").Input.ConnectTo(mg1.Output)
        for n in comp.ActiveTool.GetChildrenList().values():
            print (n.Name)
        # print comp.FindTool("MediaOut1").GetInputList()
        # comp.FindTool("MediaOut1").Input.ConnectTo()
        # print yr.YNode(mg1.Name).parent(), yr.YNode(mg1.Name).children()
        # yr.YNode("Loader1").connect()

    @unittest.skip("")
    def test_fusion(self):
        mg1 = yr.Node().create("Merge")
        print(yr.Node(mg1).children())
        paint = yr.Node().create("Paint", 2, 1)
        print(paint.id, paint.name, paint.attrs)
        paint.hide()
        paint.instance()
        paint.select()
        paint.connect(yr.Node("MediaOut1"))
        yr.Node().create("Grain").delete()
        myblur = yr.Node().create("Blur")
        mybg = yr.Node().create("Background")
        mybg.connect(yr.Node(myblur.name))
        mybg.Type.set("Vertical")
        myblur.XBlurSize.set(5.0)


if __name__ == "__main__":
    unittest.main()
