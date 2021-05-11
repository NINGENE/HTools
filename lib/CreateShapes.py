# __*__ coding: utf-8 __*__
from maya import cmds, mel
from HTools.lib import HToolsLib
reload(HToolsLib)
'''
作成日 2018/2/15
更新日 2018/2/16
更新再開日　2019/12/16

概要
Nurbusシェイプを生成するライブラリにすることを目的とする
'''
shapeDict = {'linierCircle':1, 'ototsuCircle':2, 'cross':3,
             'arrowCross':4, 'box':5, 'pyramid':6, 
             'gear':7, 'sphere':8, 'candyLike':9}

def callShape(shapeNumber, shapeName=''):
    if not shapeNumber:
        print('There is no number for choosing the shape.')
    
    elif shapeNumber == 1:
        tempName = linerCircle()
    
    elif shapeNumber == 2:
        tempName = ototsuCircle()

    elif shapeNumber == 3:
        tempName = cross()

    elif shapeNumber == 4:
        tempName = arrowCross()

    elif shapeNumber == 5:
        tempName = box()

    elif shapeNumber == 6:
        tempName = pyramid()

    elif shapeNumber == 7:
        tempName = gear()

    elif shapeNumber == 8:
        tempName = sphere(shapeName, color=22)

    elif shapeNumber == 9:
        tempName = candyLike()

    return tempName
    
def linerCircle():
	#ルートコントローラー作成（円）
    tempName = cmds.curve(d=1, p=[(0, 0, -1), (-0.195, 0, -0.981), (-0.383, 0, -0.924),
                                    (-0.556, 0, -0.831), (-0.707, 0, -0.707), (-0.831, 0, -0.556),
                                    (-0.924, 0, -0.383), (-0.981, 0, -0.195), (-1, 0, 0),
                                    (-0.981, 0, 0.195), (-0.924, 0, 0.383), (-0.831, 0, 0.556),
                                    (-0.707, 0, 0.707), (-0.556, 0, 0.831), (-0.383, 0, 0.924),
                                    (-0.195, 0, 0.981), (0, 0, 1), (0.195, 0, 0.981),
                                    (0.383, 0, 0.924), (0.556, 0, 0.831), (0.707, 0, 0.707),
                                    (0.831, 0, 0.556), (0.924, 0, 0.383), (0.981, 0, 0.195), 
                                    (1, 0, 0), (0.981, 0, -0.195), (0.924, 0, -0.383),
                                    (0.831, 0, -0.556), (0.707, 0, -0.707), (0.556, 0, -0.831),
                                    (0.383, 0, -0.924), (0.195, 0, -0.981), (0, 0, -1)],
                                k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                                    17, 18, 19, 20, 21, 22, 23, 24,25, 26, 27, 28, 29, 30, 31, 32])
    return tempName

def ototsuCircle():
	#ルートコントローラー作成（円）
    tempName = cmds.curve(d=1, p=[(0, 0, -0.7), (-0.195, 0, -0.981), (-0.383, 0, -0.924),
                                    (-0.556, 0, -0.831), (-0.707, 0, -0.707), (-0.831, 0, -0.556),
                                    (-0.924, 0, -0.383), (-0.981, 0, -0.195), (-1, 0, 0),
                                    (-0.981, 0, 0.195), (-0.924, 0, 0.383), (-0.831, 0, 0.556),
                                    (-0.707, 0, 0.707), (-0.556, 0, 0.831), (-0.383, 0, 0.924),
                                    (-0.195, 0, 0.981), (0, 0, 1.3), (0.195, 0, 0.981),
                                    (0.383, 0, 0.924), (0.556, 0, 0.831), (0.707, 0, 0.707),
                                    (0.831, 0, 0.556), (0.924, 0, 0.383), (0.981, 0, 0.195), 
                                    (1, 0, 0), (0.981, 0, -0.195), (0.924, 0, -0.383),
                                    (0.831, 0, -0.556), (0.707, 0, -0.707), (0.556, 0, -0.831),
                                    (0.383, 0, -0.924), (0.195, 0, -0.981), (0, 0, -0.7)],
                                k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                                    17, 18, 19, 20, 21, 22, 23, 24,25, 26, 27, 28, 29, 30, 31, 32])
    return tempName

def cross():
    tempName = cmds.curve(d=1, p=[(0.4, 0, -0.4), (0.4, 0, -2), (-0.4, 0, -2),
                                    (-0.4, 0, -0.4), (-2, 0, -0.4), (-2, 0, 0.4),
                                    (-0.4, 0, 0.4), (-0.4, 0, 2), (0.4, 0, 2),
                                    (0.4, 0, 0.4), (2, 0, 0.4), (2, 0, -0.4), (0.4, 0, -0.4)],
                                k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])	
    return tempName

def arrowCross():
	#移動コントローラーの作成（十字矢印）
    tempName = cmds.curve(d=1, p=[(0, 0, -1), (-0.25, 0, -0.66), (-0.1, 0, -0.66),
                                (-0.1, 0, -0.1), (-0.66, 0, -0.1), (-0.66, 0, -0.25),
                                (-1, 0, 0), (-0.66, 0, 0.25), (-0.66, 0, 0.1),
                                (-0.1, 0, 0.1), (-0.1, 0, 0.66), (-0.25, 0, 0.66),
                                (0, 0, 1), (0.25, 0, 0.66), (0.1, 0, 0.66),
                                (0.1, 0, 0.1), (0.66, 0, 0.1), (0.66, 0, 0.25),
                                (1, 0, 0), (0.66, 0, -0.25), (0.66, 0, -0.1),
                                (0.1, 0, -0.1), (0.1, 0, -0.66), (0.25, 0, -0.66), (0, 0, -1)],
                                k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
    return tempName

def box():
    tempName = cmds.curve(d=1, p=[(0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
                                    (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5),
                                    (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5),
                                    (0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5),
                                    (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5),
                                    (-0.5, 0.5, 0.5)], 
                                k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    return tempName

def pyramid():
    tempName = cmds.curve(d=1, p=[(0.5, -1, 0.87), (-0.5, -1, 0.87), (0, 1, 0),
                            (0.5, -1, 0.87), (1, -1, 0), (0, 1, 0),
                            (0.5, -1, -0.87), (1, -1, 0), (0, 1, 0),
                            (-0.5, -1, -0.87), (0.5, -1, -0.87), (0, 1, 0),
                            (-1, -1, 0), (-0.5, -1, -0.87), (0, 1, 0),
                            (-0.5, -1, 0.87), (-1, -1, 0)],
                            k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
    
    return tempName

def gear():
    tempName = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=50, d=3, ut=False, s=16, ch=True)
    cmds.select(cl=True)
    i=0
    while i < 16:
        editPoint = tempName[0]+'.cv['+str(i)+']'
        if i %2 == 0:
            cmds.select(editPoint, add=True)
        i+=1
    cmds.scale(0.4, 0.4, 0.4)
    cmds.select(tempName)
    HToolsLib.freezeAndDeletehistory()

    return tempName[0]

def sphere(shapeName, color=22):
    CIRCLE_ODER = ('A', 'B', 'C')
    topNodeName = ''
    for i in range(1, 4):
        ctrlName = shapeName + CIRCLE_ODER[i-1]
        tempName = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=False, s=8, ch=True)
        HToolsLib.renameAndColor(tempName[0], ctrlName, color)
        cmds.select(ctrlName, r=True)
        if i == 1:
            topNodeName = ctrlName
            cmds.rotate(0, 0, 0)
        elif i == 2:
            cmds.rotate(0, 0, 90)
        elif i == 3:
            cmds.rotate(90, 0, 90)
        else:
            pass

        HToolsLib.freezeAndDeletehistory()

        if i > 1:
            cmds.select(ctrlName + 'Shape')
            cmds.select(topNodeName, add=True)
            cmds.parent(r=True, s=True)
            cmds.delete(ctrlName)

    return topNodeName

def candyLike():
    tempName = cmds.curve(d=1, p=[(0, 0, 0), (-2, 0, 0), (-2.292893, 0, 0.707107),
                                (-3, 0, 1), (-3.707107, 0, 0.707107), (-4, 0, 0),
								(-3.707107, 0, -0.707107), (-3, 0, -1),
								(-2.292893, 0, -0.707107), (-2, 0, 0),
								(-2.292893, 0, 0.707107), (-3.707107, 0, -0.707107),
								(-4, 0, 0), (-3.707107, 0, 0.707107), (-2.292893, 0, -0.707107)],
								k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

    return tempName

#FKIK切り替えコントローラーの作成
#スイッチの名前変えられるようにするべき
def createFKIKSwitch(ctlScale = 1):
    allController = []  #最後のペアレント用のリスト

    #'FK'文字の作成
    ctrlName = 'curve_FK'
    allController.append(ctrlName)

    tempName = cmds.curve(d=1, p=[(-7, 0, -25), (-25, 0, -25), (-28, 0, 25), 
                                  (-22, 0, 25), (-19, 0, 2), (-8, 0, 1), 
                                  (-9, 0, -8), (-19, 0, -6), (-17, 0, -14), 
                                  (-9, 0, -15), (-7, 0, -25)], 
                               k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    HToolsLib.renameAndColor(tempName, ctrlName, 16)
    

    ctrlName = 'curve_FK_K' #テンポラリのノードなのでappendしない

    tempName = cmds.curve(d=1, p=[(5, 0, -27), (-1, 0, 25), (6, 0, 27), 
                                  (9, 0, 8), (17, 0, 25), (24, 0, 25), 
                                  (15, 0, 2), (28, 0, -15), (20, 0, -21), 
                                  (11, 0, -6), (14, 0, -26), (5, 0, -27)], 
                               k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

    HToolsLib.renameAndColor(tempName, ctrlName, 16)

    cmds.parent('curve_FK_KShape', 'curve_FK', r=True, s=True)
    cmds.rename('curve_FKShape', 'curve_FK_FShape')
    cmds.delete('curve_FK_K')
    cmds.move(0, 0, -30, 'curve_FK', r=True)
    HToolsLib.freezeAndDeletehistory('curve_FK')
    
    
    #'IK'文字の作成
    ctrlName = 'curve_IK'
    allController.append(ctrlName)

    tempName = cmds.curve(d=1, p=[(-29, 0, -23), (-14, 0, -21), (-16, 0, -16), 
                                  (-20, 0, -16), (-21, 0, 15), (-15, 0, 19), 
                                  (-17, 0, 24), (-30, 0, 21), (-30, 0, 13), 
                                  (-27, 0, 14), (-26, 0, -16), (-30, 0, -16), (-29, 0, -23)], 
                               k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    HToolsLib.renameAndColor(tempName, ctrlName, 16)

    
    ctrlName = 'curve_IK_K' #テンポラリのノードなのでappendしない

    tempName = cmds.curve(d=1, p=[(2, 0, -21), (-1, 0, 25), (6, 0, 23), 
                                  (8, 0, 7), (18, 0, 25), (26, 0, 23), 
                                  (13, 0, -1), (30, 0, -20), (15, 0, -22), 
                                  (10, 0, -7), (10, 0, -22), (2, 0, -21)], 
                               k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

    HToolsLib.renameAndColor(tempName, ctrlName, 16)

    cmds.parent('curve_IK_KShape', 'curve_IK', r=True, s=True)

    cmds.rename('curve_IKShape', 'curve_IK_IShape')
    cmds.delete('curve_IK_K')
    cmds.move(0, 0, 30, 'curve_IK', r=True)
    HToolsLib.freezeAndDeletehistory('curve_IK')

    #HandSwitcherの作成
    baseHandCtrlName = 'handCtrl_SWTC'
    ctrlName = baseHandCtrlName + '_L'
    allController.append(ctrlName)

    tempName = cmds.curve(d=1, p=[(6, 0, -5), (3, 0, -7), (1, 0, -10), 
                                  (-2, 0, -9.5), (-2, 0, -8), (-1, 0, -5.5), 
                                  (1, 0, -3), (-9.5, 0, -3), (-10.5, 0, -2), 
                                  (-10.5, 0, -0.5), (-9.5, 0, 0.5), (2, 0, 0.5), 
                                  (-5, 0, 1), (-6, 0, 2.5), (-6, 0, 4), 
                                  (-5, 0, 5), (1.5, 0, 4), (-4.5, 0, 5), 
                                  (-5, 0, 6), (-4.5, 0, 7.5), (-4, 0, 8), 
                                  (1.5, 0, 6), (-3, 0, 8), (-3.5, 0, 9), 
                                  (-3, 0, 10.5), (-2, 0, 11), (3, 0, 9), (7, 0, 6.5), 
                                  (9, 0, 4), (10, 0, 3), (10, 0, -2), 
                                  (9, 0, -3), (6, 0, -5)], 
                               k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32])

    HToolsLib.renameAndColor(tempName, ctrlName, 16)

    ctrlName = baseHandCtrlName + '_R'
    allController.append(ctrlName)

    tempName = cmds.duplicate(baseHandCtrlName + '_L')
    cmds.rename(tempName, ctrlName)
    cmds.select(ctrlName, r=True)
    cmds.scale(-1, 1, 1)

    cmds.move(45, 0, -50, baseHandCtrlName +'_L')
    HToolsLib.freezeAndDeletehistory(baseHandCtrlName + '_L')

    cmds.move(-45, 0, -50, baseHandCtrlName + '_R')
    HToolsLib.freezeAndDeletehistory(baseHandCtrlName + '_R')

    cmds.select(baseHandCtrlName + '_L', r=True)
    cmds.transformLimits(etz=(True, True), tz=(0, 1))

    cmds.select(baseHandCtrlName + '_R', r=True)
    cmds.transformLimits(etz=(True, True), tz=(0, 1))


    #LegSwitcherの作成
    baseLegCtrlName = 'footCtrl_SWTC'
    ctrlName = baseLegCtrlName + '_L'
    allController.append(ctrlName)

    tempName = cmds.curve(d=1, p=[(-7, 0, -9), (-7, 0, -5.8), (-6, 0, -5.8), 
                                  (-6, 0, -0.3), (-6.5, 0, -0.4), (-6, 0, 1.4), 
                                  (-6.5, 0, 2), (-6, 0, 3), (-6, 0, 4.5), 
                                  (-7, 0, 7), (-6.8, 0, 9), (-3.6, 0, 9), 
                                  (-3.5, 0, 8), (-2, 0, 9), (5, 0, 9), 
                                  (6, 0, 8.5), (7, 0, 7), (6.5, 0, 4), 
                                  (4, 0, 2.5), (1.7, 0, 3.5), (1, 0, 3), 
                                  (0.1, 0, 2), (-0.7, 0, 1.5), (-0.1, 0, 0.6), 
                                  (-0.5, 0, -0.1), (-0.5, 0, -5), (0.5, 0, -5), 
                                  (0.8, 0, -8.5), (-7, 0, -9)], 
                               k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28])

    HToolsLib.renameAndColor(tempName, ctrlName, 16)


    ctrlName = baseLegCtrlName + '_R'
    allController.append(ctrlName)

    tempName = cmds.duplicate(baseLegCtrlName + '_L')
    cmds.rename(tempName, ctrlName)
    cmds.select(ctrlName, r=True)
    cmds.scale(-1, 1, 1)

    cmds.move(45, 0, -20, baseLegCtrlName + '_L')
    cmds.select(baseLegCtrlName + '_L')
    HToolsLib.freezeAndDeletehistory()

    cmds.move(-45, 0, -20, baseLegCtrlName + '_R')
    cmds.select(baseLegCtrlName + '_R')
    HToolsLib.freezeAndDeletehistory()

    #↓なんであるのか覚えてない、要らなくない？
    #cmds.select(ctrlName, r=True)
    #cmds.transformLimits(tz=(-50, 50))
    #cmds.transformLimits(etz=(True, True))

    cmds.select(baseLegCtrlName + '_L', r=True)
    cmds.transformLimits(etz=(True, True), tz=(0, 1))

    cmds.select(baseLegCtrlName + '_R', r=True)
    cmds.transformLimits(etz=(True, True), tz=(0, 1))

    #スイッチャーのグループ化
    cmds.group(w=True, em=True, n='FKIK_SWITCH_GRP')
    cmds.group(w=True, em=True, n='scale_OFST')
    cmds.scale(70, 70, 70, 'scale_OFST')
    
    for ctrl in allController:
        #print(ctrl)
        cmds.parent(ctrl, 'scale_OFST')

    cmds.parent('scale_OFST', 'FKIK_SWITCH_GRP')

    #1モノによって数値を変える必要あり
    cmds.scale(ctlScale, ctlScale, ctlScale, 'FKIK_SWITCH_GRP')

    HToolsLib.setKeyAbleTRS('scale_OFST', 1, 1, 1)

    HToolsLib.setKeyAbleTRS('curve_FK', 1, 1, 1)
    HToolsLib.setKeyAbleTRS('curve_IK', 1, 1, 1)
    HToolsLib.setKeyAbleTRS(baseHandCtrlName + '_L', 0, 1, 1)
    HToolsLib.setKeyAbleTRS(baseHandCtrlName + '_R', 0, 1, 1)
    HToolsLib.setKeyAbleTRS(baseLegCtrlName + '_L', 0, 1, 1)
    HToolsLib.setKeyAbleTRS(baseLegCtrlName + '_R', 0, 1, 1)

    HToolsLib.setKeyAbleT(baseHandCtrlName + '_L', 1, 1, 0)
    HToolsLib.setKeyAbleT(baseHandCtrlName + '_R', 1, 1, 0)
    HToolsLib.setKeyAbleT(baseLegCtrlName + '_L', 1, 1, 0)
    HToolsLib.setKeyAbleT(baseLegCtrlName + '_R', 1, 1, 0)
    
    #↓このままではシェイプいじらないといけない
    #cmds.setAttr('curve_FK.overrideEnabled', 1)
    #cmds.setAttr('curve_FK.overrideDisplayType', 2)

    #setAttr "curve_IK.overrideEnabled" 1;
    #setAttr "curve_IK.overrideDisplayType" 2;

    cmds.select(cl=True)