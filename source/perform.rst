===================================
Performance
===================================
このモジュールはパフォーマンスに焦点を当てたモジュールではありませんが、

maya.cmds, pymel, cmdx, cymel

を対象にしたMaya上でのテスト計測結果を記載します。

.. code-block:: python

    import maya.cmds as cmds
    import cymel.main as cm
    import pymel.core as pm
    import timeit
    from random import uniform as ru
    import math
    ms = math.log(5)
    exp = math.exp

    cmds.file(f=True, new=True)
    cm.nt.Transform()

    scales = [.5 if x % 2 else 2. for x in range(1000)]

    def dotest(f):
        with cm.UndoChunk():
            print('%s=%f' % (f.__name__, timeit.timeit(f, number=1)))
        if f.__name__ != 'by_cmdx':
            cmds.undo()

    def by_pymel():
        plug = pm.selected(type='transform')[0].s
        for s in scales:
            plug.set(plug.get() * s)
    dotest(by_pymel)

    def by_cymel():
        plug = cm.sel.s
        for s in scales:
            plug.set([x * s for x in plug.get()])
    dotest(by_cymel)

    def by_cmds():
        plug = cmds.ls(sl=True, type='transform')[0] + '.s'
        for s in scales:
            cmds.setAttr(plug, *[x * s for x in cmds.getAttr(plug)[0]])
    dotest(by_cmds)

    try:
        import cmdx
    except:
        pass
    else:
        def by_cmdx():
            plug = cmdx.ls(sl=True, type='transform')[0] + '.s'
            for s in scales:
                cmdx.setAttr(plug, [x * s for x in cmdx.getAttr(plug)])
        dotest(by_cmdx)

    try:
        import yurlungur
    except:
        pass
    else:
        def by_yurlungur():
            plug = yurlungur.maya.ls(sl=True, type='transform')[0] + '.s'
            for s in scales:
                cmdx.setAttr(plug, [x * s for x in cmdx.getAttr(plug)])
        dotest(by_yurlungur)


Results

.. code-block:: python

    by_pymel=0.263930
    # Undo:  #
    by_cymel=0.048010
    # Undo:  #
    by_cmds=0.043140
    # Undo:  #
    by_cmdx=0.054413
    # Undo:  #
    by_yurlungur=0.054413