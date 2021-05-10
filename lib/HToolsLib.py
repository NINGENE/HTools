# __*__ coding: utf-8 __*__
from maya import cmds, mel

'''
作成日 2020/3/23

概要
bbdsNeoRigLibを改めて整理するためにコピーしたもの
（リグ作成で使っていた関数をモジュールとしてまとめなおしたものに追記していく）
'''
class CreateControllers():  #I've not debugged yet. It is here?
	def __init__(self, joint, position):
		
		self.orgJoint = joint
		self.pos = position
		self.ctrlName = self.orgJoint + '_CTRL' + self.pos
		self.ofstName = self.orgJoint + '_OFST' + self.pos
		self.jntName = 'MODEL:' + self.orgJoint +  '_JNT' + self.pos
		self.tempName = 'temp'

	#コントローラー作成系メソッドに仕込んであるので基本単体で呼び出すことはない
	#なんかメンバー関数？的な記述方法あるのかしら
    #これは分けて使いたいかもしれない(19/12/16)
	def normalizeController(self, rx, ry, rz, sx, sy, sz, color):
		#color 13 = red
		#color 22 = yellow
		#color 15 = blue
		bbdsNeoRigLib.renameAndColor(self.tempName, self.ctrlName, color)

		bbdsNeoRigLib.creatOffset(self.ofstName, self.ctrlName, self.jntName)

		cmds.select(self.ctrlName, r=True)
		cmds.rotate(rx, ry, rz)
		cmds.scale(sx, sy, sz)
		
		bbdsNeoRigLib.freezeAndDeletehistory()

	def createCross(self, rx, ry, rz, sx, sy, sz, color):

		self.tempName = cmds.curve(d=1, p=[(0.4, 0, -0.4), (0.4, 0, -2), (-0.4, 0, -2),
								(-0.4, 0, -0.4), (-2, 0, -0.4), (-2, 0, 0.4),
								(-0.4, 0, 0.4), (-0.4, 0, 2), (0.4, 0, 2),
								(0.4, 0, 0.4), (2, 0, 0.4), (2, 0, -0.4), (0.4, 0, -0.4)],
								k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])	
		
		self.normalizeController(rx, ry, rz, sx, sy, sz, color)

	def createCircle(self, rx, ry, rz, sx, sy, sz, color):
		self.tempName = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=0.5, d=3, ut=False, s=8, ch=True)
		self.tempName = self.tempName[0]
		self.normalizeController(rx, ry, rz, sx, sy, sz, color)

	def createSphere(self, rx, ry, rz, sx, sy, sz, color):
		self.tempName = bbdsNeoRigLib.createSimpleSphere()
		self.normalizeController(rx, ry, rz, sx, sy, sz, color)

	def createCL(self, rx, ry, rz, sx, sy, sz, color):
		self.tempName = bbdsNeoRigLib.createCandyLike()
		self.normalizeController(rx, ry, rz, sx, sy, sz, color)

	def createPoleVector(self):#極座標コントローラー作成
		self.tempName = bbdsNeoRigLib.createFSPyramid()
		bbdsNeoRigLib.renameAndColor(self.tempName, self.ctrlName, 22)

		cmds.pointConstraint(self.jntName, self.ctrlName)

		cmds.delete(cn=True)
		cmds.select(self.ctrlName, r=True)
		cmds.scale(25, 20, 25)
		cmds.rotate(-90, 0, 0)
		cmds.move(0, 0, -100, r=True)

		bbdsNeoRigLib.freezeAndDeletehistory()

	def createIKBox(self, rx, ry, rz, sx, sy, sz, color):
		self.tempName = bbdsNeoRigLib.createBox()
		self.normalizeController(rx, ry, rz, sx, sy, sz, color)
		cmds.select(self.ctrlName, r=True)
		cmds.delete(cn=True)

	def createOval(self, rx, ry, rz, sx, sy, sz, color):
		self.tempName = bbdsNeoRigLib.createBakaukeShape()
		self.normalizeController(rx, ry, rz, sx, sy, sz, color)


def pickJoint(tempSrcCtrls):    #This is just copied.
	print(tempSrcCtrls)
	cmds.select(cl=True)
	for tempCtrl in tempSrcCtrls:
		#if '_JNT_' in tempCtrl:
		if cmds.nodeType(tempCtrl) == 'joint':
			cmds.select(tempCtrl, add=True)
		else:
			print(tempCtrl + "_end")


#作成したカーブに正式名称をctrlNameとし、colNumで指定した色にする
#中で辞書作成して外からはストリングで色指定出来るようにしよう
def renameAndColor(oldName, newName, colNum):
    cmds.rename(oldName, newName)
    if colNum == 'None':
        pass
        #print('None')
    else:
        cmds.setAttr(newName + 'Shape.overrideEnabled', True)
        cmds.setAttr(newName + 'Shape.overrideColor', colNum)

def renameAndColorV2(oldName, newName, color):
    colors = {'red':13, 'yellow':22, 'blue':15}
    cmds.rename(oldName, newName)
    if color == 'None':
        pass
        #print('None')
    else:
        cmds.setAttr(newName + 'Shape.overrideEnabled', True)
        cmds.setAttr(newName + 'Shape.overrideColor', colors[color])

#オフセット用のNULLを作成
def creatOffset(osName, crName, jointName, isParent=True):
    cmds.group(n=osName, w=True, em=True)
    cmds.parent(crName, osName)
    
    if cmds.objExists(jointName):
        if isParent:
            cmds.parentConstraint(jointName, osName)
            cmds.select(osName, r=True)
            cmds.delete(cn=True)
        else:
            cmds.pointConstraint(jointName, osName)
            cmds.select(osName, r=True)
            cmds.delete(cn=True)        
	
def freezeAndDeletehistory(node=None):
    if node:
        cmds.select(node, r=True)
    else:
        pass
        
    cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
    mel.eval('DeleteHistory')

##ここは整理したい
def setKeyAble(ctrlName, t, r, s):
	if t==1:
		cmds.setAttr(ctrlName + '.tx', keyable=False, lock=True)
		cmds.setAttr(ctrlName + '.ty', keyable=False, lock=True)
		cmds.setAttr(ctrlName + '.tz', keyable=False, lock=True)
	if r==1:
		cmds.setAttr(ctrlName + '.rx', keyable=False, lock=True)
		cmds.setAttr(ctrlName + '.ry', keyable=False, lock=True)
		cmds.setAttr(ctrlName + '.rz', keyable=False, lock=True)
	if s==1:
		cmds.setAttr(ctrlName + '.sx', keyable=False, lock=True)
		cmds.setAttr(ctrlName + '.sy', keyable=False, lock=True)
		cmds.setAttr(ctrlName + '.sz', keyable=False, lock=True)

def setKeyAbleTRS(ctrlName, t, r, s):
    setKeyAbleT(ctrlName, t, t, t)
    setKeyAbleR(ctrlName, r, r, r)
    setKeyAbleS(ctrlName, s, s, s)

def setKeyAbleT(ctrlName, tx, ty, tz):
    if tx==1:
		cmds.setAttr(ctrlName + '.tx', keyable=False, lock=True)
    if ty==1:
		cmds.setAttr(ctrlName + '.ty', keyable=False, lock=True)
    if tz==1:
		cmds.setAttr(ctrlName + '.tz', keyable=False, lock=True)

def setKeyAbleR(ctrlName, rx, ry, rz):
    if rx==1:
		cmds.setAttr(ctrlName + '.rx', keyable=False, lock=True)
    if ry==1:
		cmds.setAttr(ctrlName + '.ry', keyable=False, lock=True)
    if rz==1:
		cmds.setAttr(ctrlName + '.rz', keyable=False, lock=True)

def setKeyAbleS(ctrlName, sx, sy, sz):
    if sx==1:
		cmds.setAttr(ctrlName + '.sx', keyable=False, lock=True)
    if sy==1:
		cmds.setAttr(ctrlName + '.sy', keyable=False, lock=True)
    if sz==1:
		cmds.setAttr(ctrlName + '.sz', keyable=False, lock=True)

def checkNamespace():
    global nameSpaceName
    if cmds.objExists('MODEL:Root'):
        nameSpaceName = 'MODEL:'
    else:
        print('It has no NameSpace.')

def dupulicateJoint(jointName, FKIKtype, NameSpace = None):
    tempDupNames = cmds.duplicate(jointName)
    cmds.parent(tempDupNames[0], w=True)

    cmds.select(cl=True)
    if not NameSpace:
        cmds.select(jointName, hi=True)
        originalJointNames = cmds.ls(sl=True)
        cmds.select(cl=True)
        #print(1)
    else:
        originalJointNames = tempDupNames

    newJoints = []

    i = 0
    for oldName in tempDupNames:
        newName = FKIKtype + '_' + originalJointNames[i]
        newJoints.append(newName)
        cmds.rename(oldName, newName)

        i+=1

    #print(newJoints)

    return newJoints
#形状は別のスクリプトにしようかな
##移植済み


def createToe():
    cmds.curve(d=3, p=[(15, 0, 0), (14.9, 0, 3.5), (14.5, 0, 11),
											(12, 0, 19), (5, 0, 25), (0, 0, 15),
											(-5, 0, 25), (-12, 0, 19), (-14.5, 0, 11),
											(-14.9, 0, 3.5), (-15, 0, 0)])

def createTriangle():
    tempName = cmds.curve(d=1, p=[(0, 0, -50), (-50, 0, 50), (50, 0, 50), (0, 0, -50)],
                          k=[0, 1, 2, 3])

    return tempName



def createSimpleSphere():
    cmds.curve(d=1, p=[(0, 0, 1), (0, 0.5, 0.866025), (0, 0.866025, 0.5), 
										  (0, 1, 0), (0, 0.866025, -0.5), (0, 0.5, -0.866025), 
										  (0, 0, -1), (0, -0.5, -0.866025), (0, -0.866025, -0.5), 
										  (0, -1, 0), (0, -0.866025, 0.5), (0, -0.5, 0.866025), 
										  (0, 0, 1), (0.707107, 0, 0.707107), (1, 0, 0), 
										  (0.707107, 0, -0.707107), (0, 0, -1), (-0.707107, 0, -0.707107), 
										  (-1, 0, 0), (-0.866025, 0.5, 0), (-0.5, 0.866025, 0), 
										  (0, 1, 0), (0.5, 0.866025, 0), (0.866025, 0.5, 0), 
										  (1, 0, 0), (0.866025, -0.5, 0), (0.5, -0.866025, 0), 
										  (0, -1, 0), (-0.5, -0.866025, 0), (-0.866025, -0.5, 0), 
										  (-1, 0, 0), (-0.707107, 0, 0.707107), (0, 0, 1)], 
										k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 
										   17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32])



##移植済み
def createFSPyramid():
    tempName = cmds.curve(d=1, p=[(0.5, -1, 0.87), (-0.5, -1, 0.87), (0, 1, 0),
                            (0.5, -1, 0.87), (1, -1, 0), (0, 1, 0),
                            (0.5, -1, -0.87), (1, -1, 0), (0, 1, 0),
                            (-0.5, -1, -0.87), (0.5, -1, -0.87), (0, 1, 0),
                            (-1, -1, 0), (-0.5, -1, -0.87), (0, 1, 0),
                            (-0.5, -1, 0.87), (-1, -1, 0)],
                            k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
    
    return tempName


def createBakaukeShape():
    tempName = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=False, s=8, ch=True)

    cmds.setAttr(tempName[0] + '.cv[0].xValue', -0.6)
    cmds.setAttr(tempName[0] + '.cv[0].yValue', 1.7)
    cmds.setAttr(tempName[0] + '.cv[0].zValue', 1.25)
    cmds.setAttr(tempName[0] + '.cv[1].yValue', 2)
    cmds.setAttr(tempName[0] + '.cv[1].zValue', 1.4)
    cmds.setAttr(tempName[0] + '.cv[2].xValue', 0.6)
    cmds.setAttr(tempName[0] + '.cv[2].yValue', 1.7)
    cmds.setAttr(tempName[0] + '.cv[2].zValue', 1.25)
    cmds.setAttr(tempName[0] + '.cv[3].xValue', 0.8)
    cmds.setAttr(tempName[0] + '.cv[3].yValue', 1)
    cmds.setAttr(tempName[0] + '.cv[3].zValue', 0.6)
    cmds.setAttr(tempName[0] + '.cv[4].xValue', 0.6)
    cmds.setAttr(tempName[0] + '.cv[4].yValue', 0.3)
    cmds.setAttr(tempName[0] + '.cv[4].zValue', -0.3)
    cmds.setAttr(tempName[0] + '.cv[5].zValue', -0.8)
    cmds.setAttr(tempName[0] + '.cv[6].xValue', -0.6)
    cmds.setAttr(tempName[0] + '.cv[6].yValue', 0.3)
    cmds.setAttr(tempName[0] + '.cv[6].zValue', -0.3)
    cmds.setAttr(tempName[0] + '.cv[7].xValue', -0.8)
    cmds.setAttr(tempName[0] + '.cv[7].yValue', 1)
    cmds.setAttr(tempName[0] + '.cv[7].zValue', 0.6)

    return tempName[0]


#FKIK切り替えコントローラーの作成
def createFKIKSwitch():
    allController = []  #最後のペアレント用のリスト

    #'FK'文字の作成
    ctrlName = 'curve_FK'
    allController.append(ctrlName)

    tempName = cmds.curve(d=1, p=[(-7, 0, -25), (-25, 0, -25), (-28, 0, 25), 
                                  (-22, 0, 25), (-19, 0, 2), (-8, 0, 1), 
                                  (-9, 0, -8), (-19, 0, -6), (-17, 0, -14), 
                                  (-9, 0, -15), (-7, 0, -25)], 
                               k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    renameAndColor(tempName, ctrlName, 16)
    

    ctrlName = 'curve_FK_K' #テンポラリのノードなのでappendしない

    tempName = cmds.curve(d=1, p=[(5, 0, -27), (-1, 0, 25), (6, 0, 27), 
                                  (9, 0, 8), (17, 0, 25), (24, 0, 25), 
                                  (15, 0, 2), (28, 0, -15), (20, 0, -21), 
                                  (11, 0, -6), (14, 0, -26), (5, 0, -27)], 
                               k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

    renameAndColor(tempName, ctrlName, 16)

    cmds.parent('curve_FK_KShape', 'curve_FK', r=True, s=True)
    cmds.rename('curve_FKShape', 'curve_FK_FShape')
    cmds.delete('curve_FK_K')
    cmds.move(0, 0, -30, 'curve_FK', r=True)
    freezeAndDeletehistory('curve_FK')
    
    
    #'IK'文字の作成
    ctrlName = 'curve_IK'
    allController.append(ctrlName)

    tempName = cmds.curve(d=1, p=[(-29, 0, -23), (-14, 0, -21), (-16, 0, -16), 
                                  (-20, 0, -16), (-21, 0, 15), (-15, 0, 19), 
                                  (-17, 0, 24), (-30, 0, 21), (-30, 0, 13), 
                                  (-27, 0, 14), (-26, 0, -16), (-30, 0, -16), (-29, 0, -23)], 
                               k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    renameAndColor(tempName, ctrlName, 16)

    
    ctrlName = 'curve_IK_K' #テンポラリのノードなのでappendしない

    tempName = cmds.curve(d=1, p=[(2, 0, -21), (-1, 0, 25), (6, 0, 23), 
                                  (8, 0, 7), (18, 0, 25), (26, 0, 23), 
                                  (13, 0, -1), (30, 0, -20), (15, 0, -22), 
                                  (10, 0, -7), (10, 0, -22), (2, 0, -21)], 
                               k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

    renameAndColor(tempName, ctrlName, 16)

    cmds.parent('curve_IK_KShape', 'curve_IK', r=True, s=True)

    cmds.rename('curve_IKShape', 'curve_IK_IShape')
    cmds.delete('curve_IK_K')
    cmds.move(0, 0, 30, 'curve_IK', r=True)
    freezeAndDeletehistory('curve_IK')

    #HandSwitcherの作成
    ctrlName = 'HandCtrl_SWTC_L'
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

    renameAndColor(tempName, ctrlName, 16)

    ctrlName = 'HandCtrl_SWTC_R'
    allController.append(ctrlName)

    tempName = cmds.duplicate('HandCtrl_SWTC_L')
    cmds.rename(tempName, ctrlName)
    cmds.select(ctrlName, r=True)
    cmds.scale(-1, 1, 1)

    cmds.move(45, 0, -50, 'HandCtrl_SWTC_L')
    freezeAndDeletehistory('HandCtrl_SWTC_L')

    cmds.move(-45, 0, -50, 'HandCtrl_SWTC_R')
    freezeAndDeletehistory('HandCtrl_SWTC_R')

    cmds.select('HandCtrl_SWTC_L', r=True)
    cmds.transformLimits(etz=(True, True), tz=(0, 1))

    cmds.select('HandCtrl_SWTC_R', r=True)
    cmds.transformLimits(etz=(True, True), tz=(0, 1))


    #LegSwitcherの作成
    ctrlName = 'LegCtrl_SWTC_L'
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

    renameAndColor(tempName, ctrlName, 16)


    ctrlName = 'LegCtrl_SWTC_R'
    allController.append(ctrlName)

    tempName = cmds.duplicate('LegCtrl_SWTC_L')
    cmds.rename(tempName, ctrlName)
    cmds.select(ctrlName, r=True)
    cmds.scale(-1, 1, 1)

    cmds.move(45, 0, -20, 'LegCtrl_SWTC_L')
    cmds.select('LegCtrl_SWTC_L')
    freezeAndDeletehistory()

    cmds.move(-45, 0, -20, 'LegCtrl_SWTC_R')
    cmds.select('LegCtrl_SWTC_R')
    freezeAndDeletehistory()

    #↓なんであるのか覚えてない、要らなくない？
    #cmds.select(ctrlName, r=True)
    #cmds.transformLimits(tz=(-50, 50))
    #cmds.transformLimits(etz=(True, True))

    cmds.select('LegCtrl_SWTC_L', r=True)
    cmds.transformLimits(etz=(True, True), tz=(0, 1))

    cmds.select('LegCtrl_SWTC_R', r=True)
    cmds.transformLimits(etz=(True, True), tz=(0, 1))

    #スイッチャーのグループ化
    cmds.group(w=True, em=True, n='FKIK_SWITCH_GRP')
    cmds.group(w=True, em=True, n='scale_OFST')
    cmds.scale(70, 70, 70, 'scale_OFST')
    
    for ctrl in allController:
        #print(ctrl)
        cmds.parent(ctrl, 'scale_OFST')

    cmds.parent('scale_OFST', 'FKIK_SWITCH_GRP')

    setKeyAbleTRS('scale_OFST', 1, 1, 1)

    setKeyAbleTRS('curve_FK', 1, 1, 1)
    setKeyAbleTRS('curve_IK', 1, 1, 1)
    setKeyAbleTRS('HandCtrl_SWTC_L', 0, 1, 1)
    setKeyAbleTRS('HandCtrl_SWTC_R', 0, 1, 1)
    setKeyAbleTRS('LegCtrl_SWTC_L', 0, 1, 1)
    setKeyAbleTRS('LegCtrl_SWTC_R', 0, 1, 1)

    setKeyAbleT('HandCtrl_SWTC_L', 1, 1, 0)
    setKeyAbleT('HandCtrl_SWTC_R', 1, 1, 0)
    setKeyAbleT('LegCtrl_SWTC_L', 1, 1, 0)
    setKeyAbleT('LegCtrl_SWTC_R', 1, 1, 0)
    
    #↓このままではシェイプいじらないといけない
    #cmds.setAttr('curve_FK.overrideEnabled', 1)
    #cmds.setAttr('curve_FK.overrideDisplayType', 2)

    #setAttr "curve_IK.overrideEnabled" 1;
    #setAttr "curve_IK.overrideDisplayType" 2;

    cmds.select(cl=True)

    