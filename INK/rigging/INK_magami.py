# __*__ coding: utf-8 __*__
from maya import cmds, mel
from HTools.lib import HToolsLib, CreateShapes
reload(HToolsLib)
reload(CreateShapes)

'''
開始日 2020/5/21
isUpはクラスにしたいな～
そもそもisUpのチェックは関数化したい
'''

#colors = {'red':13, 'yellow':22, 'blue':15}
nameSpaceName = ''

POS_LIST = ('_L', '_R')

#ARM_LIMBS = ('shoulder', 'arm', 'hand', 'weapon')
ARM_LIMBS = ('shoulder', 'arm', 'hand')
LEG_LIMBS = ('hip', 'thigh', 'leg', 'foot')
#LEG_LIMBS = ('thigh', 'leg', 'foot')

IK_ARM_CTRLS = ('PV_IK_arm', 'IK_hand') #'CTRL_PV_IK_arm_L'
IK_LEG_CTRLS = ('PV_IK_leg', 'IK_foot')

IKGRP = 'IK_GRP'

def main():
    checkNamespace()

    createGeneCtrl()

    childController = 'CTRL_tr_C'
    cmds.parent(childController, 'CTRL_Root')
    HToolsLib.setKeyAble(childController, 0, 0, 1)

    headUnitCreate()
    spinneUnitCreate()
    tailUnitCreate()
    magamiGlitchUnitCreate()

    #FKIKコントローラー作成　関数化する
    for pos in POS_LIST:
        limbUnitFKCreate(ARM_LIMBS, pos)
        limbUnitFKCreate(LEG_LIMBS, pos)

        #複製したジョイントと表示切替のためのコントローラーの名前が欲しい
        limbUnitIKCreate(ARM_LIMBS, pos, False)

    armsGroup = 'armsFKIK_JNT_GRP'
    legsGroup = 'legsFKIK_JNT_GRP'

    cmds.group(w=True, em=True, n=armsGroup)
    cmds.group(w=True, em=True, n=legsGroup)

    for pos in POS_LIST:
        parentName = armsGroup
        childName  = 'FK_shoulder' + pos
        cmds.parent(childName, parentName)

        childName = 'IK_shoulder' + pos
        cmds.parent(childName, parentName)

        parentName = legsGroup
        childName  = 'FK_hip' + pos
        cmds.parent(childName, parentName)

    cmds.parent(armsGroup, 'CTRL_spine02_C')
    #cmds.parent(legsGroup, 'CTRL_spine06_C')
    
    CreateShapes.createFKIKSwitch(0.025)
    for pos in POS_LIST:
        FKIK = FKIKUnit(True, pos)
        FKIK.checkLimbs()
        FKIK.setLimbsFKSwitch()
        FKIK.setLimbsIKSwitch()



    for pos in POS_LIST:
        makeDogLegRig(pos)

        FKIK = FKIKUnit(False, pos)
        FKIK.checkLimbs()
        FKIK.setLimbsFKSwitch()

        setDogLegIKSwitch(pos)

    parentTopOfUnitController()

    cmds.select('FKIK_SWITCH_GRP')
    cmds.move(5, 5, 0)
    cmds.rotate(90, 0, 0)
    cmds.select(cl=True)
    cmds.parent('FKIK_SWITCH_GRP', 'CTRL_tr_C')     

def parentTopOfUnitController():
    #各ユニットのトップノードをペアレント
    parentController = 'CTRL_tr_C'
    childController  = 'OFST_hip_C'
    cmds.parent(childController, parentController)

    parentController = 'CTRL_hip_C'
    childController  = 'OFST_tail01_C'
    cmds.parent(childController, parentController)

    parentController = 'CTRL_spine02_C'
    childController  = 'OFST_neck01_C'
    cmds.parent(childController, parentController)
    
    childController  = 'OFST_cloud01_C'
    cmds.parent(childController, parentController)

    for pos in POS_LIST:
        childController  = 'OFST_FK_shoulder' + pos
        cmds.parent(childController, parentController)
        childController  = 'OFST_FK_hip' + pos
        cmds.parent(childController, parentController)
        

    #IKまわり
    cmds.group(w=True, em=True, n=IKGRP)
    for pos in POS_LIST:
        createIKGroup(True, pos)
        #createIKGroup(False, pos)
    cmds.parent(IKGRP, 'CTRL_Root')
    
    armsGroup = 'armsIK_CTRL_GRP'
    cmds.group(w=True, em=True, n=armsGroup)
    for pos in POS_LIST:
        cmds.parent('CTRL_PV_IK_arm' + pos, armsGroup)
        cmds.parent('OFST_IK_hand' + pos, armsGroup)
    cmds.parent(armsGroup, 'CTRL_tr_C')


    legsGroup = 'footIK_CTRL_GRP'
    cmds.parent(legsGroup, 'CTRL_tr_C')

    cmds.parent('legsFKIK_JNT_GRP', 'CTRL_hip_C')
    
    cmds.parent('DogLegIK_GRP', 'CTRL_tr_C')


    #legsGroup = 'legsIK_CTRL_GRP'

    #cmds.group(w=True, em=True, n=legsGroup)



def checkNamespace():
    global nameSpaceName
    if cmds.objExists('MODEL:Root'):
        nameSpaceName = 'MODEL:'
        print('NameSpace is ' + str(nameSpaceName))
    else:
        print('It has no NameSpace.')

def check_weponJoint(pos):
    #IK使用時に非表示なるので、spineの子にする（墨兵はヒップ
    if cmds.objExists(nameSpaceName + 'weapon' + pos):
        ofstName  = 'OFST_FK_weapon' + pos
        ctrlName  = 'CTRL_FK_weapon' + pos
    
        cmds.parent(ofstName, 'CTRL_hip_C')
        HToolsLib.setKeyAble(ctrlName, 0, 0, 1)


def createGeneCtrl():
    ##ルートコントローラー作成（円）
    ctrlName = 'CTRL_Root'

    tempName = CreateShapes.linerCircle()
    HToolsLib.renameAndColorV2(tempName, ctrlName, 'red')
    cmds.select(ctrlName, r=True)
    HToolsLib.freezeAndDeletehistory()

    ##移動コントローラーの作成（十字矢印）
    ctrlName = 'CTRL_tr_C'

    tempName = CreateShapes.arrowCross()
    HToolsLib.renameAndColorV2(tempName, ctrlName, 'red')
    cmds.select(ctrlName, r=True)
    #cmds.scale(svalu, svalu, svalu)
    HToolsLib.freezeAndDeletehistory()

def spinneUnitCreate():
    uHip = ControllerCreator(nameSpaceName, 'hip')
    tempName = CreateShapes.cross()
    uHip.createControllers(tempName)
    uHip.setRotate((180, 0, 90))
    uHip.setScale((1, 1, 1))
    HToolsLib.setKeyAble(uHip.ctrlName, 0, 0, 1)

    uSpines = []
    for i in range(1, 3):
        uSpine = ControllerCreator(nameSpaceName, 'spine%02d' %i)
        tempName = CreateShapes.ototsuCircle()
        uSpine.createControllers(tempName)
        uSpine.setRotate((180, 0, 90))
        uSpine.setScale((1.5, 1.5, 1.5))
        HToolsLib.setKeyAble(uSpine.ctrlName, 1, 0, 1)

        uSpines.append(uSpine)
    
    uSpines[0].parentController(uHip.ctrlName)
    uSpines[1].parentController(uSpines[0].ctrlName)

    uHip.constraintController()
    for uSpine in uSpines:
        uSpine.constraintController()

    return uHip
    
def headUnitCreate():
    uNeck = ControllerCreator(nameSpaceName, 'neck01')
    tempName = CreateShapes.ototsuCircle()
    uNeck.createControllers(tempName)
    uNeck.setRotate((180, 0, 90))
    uNeck.setScale((1.5, 1.5, 1.5))
    HToolsLib.setKeyAble(uNeck.ctrlName, 1, 0, 1)

    uHead = ControllerCreator(nameSpaceName, 'head01')
    tempName = CreateShapes.ototsuCircle()
    uHead.createControllers(tempName)
    uHead.setRotate((180, 0, 90))
    uHead.setScale((1.5, 1.5, 1.5))
    HToolsLib.setKeyAble(uHead.ctrlName, 1, 0, 1)

    uJaw = ControllerCreator(nameSpaceName, 'jaw01')
    tempName = CreateShapes.linerCircle()
    uJaw.createControllers(tempName)
    uJaw.setRotate((90, 0, 90))
    uJaw.setScale((1.5, 1, 1))
    HToolsLib.setKeyAble(uJaw.ctrlName, 1, 0, 1)

    uHead.parentController(uNeck.ctrlName)
    uJaw.parentController(uHead.ctrlName)

    uNeck.constraintController()
    uHead.constraintController()
    uJaw.constraintController()

    return uNeck

def tailUnitCreate():
    uTails = []
    i = 1
    while True:
        uTail = ControllerCreator(nameSpaceName, 'tail%02d' %i)
        if cmds.objExists(uTail.jointName):
            tempName = CreateShapes.ototsuCircle()
            uTail.createControllers(tempName)
            uTail.setRotate((180, 0, 90))
            uTail.setScale((1.5, 1.5, 1.5))
            HToolsLib.setKeyAble(uTail.ctrlName, 1, 0, 1)

            uTails.append(uTail)

            i += 1
        else:
            break
    
    for i in range(1, len(uTails)):
        #print(uTails[i].ctrlName)
        uTails[i].parentController(uTails[i-1].ctrlName)

    for uTail in uTails:
        uTail.constraintController()

    return uTails[0]

def magamiGlitchUnitCreate():
    scaleVal = [0.8, 0.8, 0.8]
    uG_C = ControllerCreator(nameSpaceName, 'cloud01')
    tempName = CreateShapes.sphere(uG_C.ctrlName)
    uG_C.createControllers(tempName)
    uG_C.setScale(scaleVal)
    HToolsLib.setKeyAble(uG_C.ctrlName, 0, 0, 1)

    uG_C.constraintController()
    unitTopController = uG_C.ctrlName
    
    for pos in POS_LIST:
        uG_LR = ControllerCreator(nameSpaceName, 'cloud01', pos)
        tempName = CreateShapes.sphere(uG_LR.ctrlName)
        uG_LR.createControllers(tempName)
        uG_LR.setScale(scaleVal)
        HToolsLib.setKeyAble(uG_LR.ctrlName, 0, 0, 1)

        uG_LR.parentController(unitTopController)
        uG_LR.constraintController()
    
    clouds = ['A', 'B', 'C']
    for cloud in clouds:
        uG_N = ControllerCreator(nameSpaceName, 'cloud' + cloud + '01', '_N')
        tempName = CreateShapes.sphere(uG_N.ctrlName)
        uG_N.createControllers(tempName)
        uG_N.setScale(scaleVal)
        HToolsLib.setKeyAble(uG_N.ctrlName, 0, 0, 1)

        uG_N.parentController(unitTopController)
        uG_N.constraintController()

def limbUnitFKCreate(limbs, pos):
    baseDupJoint = nameSpaceName + limbs[0] + pos
    dupList = dupulicateJoint(baseDupJoint, 'FK', nameSpaceName)

    for dJoint in dupList:
        jointName = dJoint
        ofstName  = 'OFST_' + dJoint
        ctrlName  = 'CTRL_' + dJoint
        
        tempName = CreateShapes.linerCircle()
        HToolsLib.renameAndColorV2(tempName, ctrlName, 'blue')
        HToolsLib.creatOffset(ofstName, ctrlName, jointName)

        cmds.parentConstraint(jointName, ofstName)
        cmds.select(ofstName, r=True)
        cmds.delete(cn=True)

        cmds.select(ctrlName, r=True)
        #cmds.rotate(rx, ry, rz)
        cmds.rotate(0, 0, 90)
        #cmds.scale(sx, sy, sz)
        cmds.scale(1, 1, 1)

        HToolsLib.freezeAndDeletehistory()
    
    lastChild = ''
    #print(lastSpineName)
    for limb in limbs:
        if limb == limbs[0]:
            pass    
        else:
            parent  = lastChild
            child   = 'OFST_FK_' + limb + pos
        
            cmds.parent(child, parent)
        
        ctrl  = 'CTRL_FK_' + limb + pos
        HToolsLib.setKeyAble(ctrl, 1, 0, 1)
        lastChild = ctrl

    for limb in limbs:
        driver = 'CTRL_FK_' + limb + pos
        driven = 'FK_' + limb + pos
        cmds.parentConstraint(driver, driven, mo=True)

def limbUnitIKCreate(limbs, pos, isPositive=False):
    #def createIKLimbs(self, isPositive):
    vecZPos = 0.75
    vecXRot = 90
    if isPositive:
        pass
    else:
        vecZPos *= -1
        vecXRot *= -1

    baseDupJoint = nameSpaceName + limbs[0] + pos
    dupList = dupulicateJoint(baseDupJoint, 'IK', nameSpaceName)
    
    ##creating IK Pole vector controller. 
    jointName = dupList[1]
    ctrlName  = 'CTRL_PV_' + dupList[1]
    
    tempName = CreateShapes.pyramid()

    HToolsLib.renameAndColorV2(tempName, ctrlName, 'blue')

    cmds.parentConstraint(jointName, ctrlName)
    cmds.select(ctrlName, r=True)
    cmds.delete(cn=True)

    cmds.select(ctrlName, r=True)
    cmds.move(0, 0, vecZPos, r=True, wd=True)
    cmds.rotate(vecXRot, 0, 0)
    cmds.scale(0.5, 0.5, 0.5)

    HToolsLib.freezeAndDeletehistory()

    ##creating IK controller.
    jointName = dupList[2]
    ctrlName  = 'CTRL_' + dupList[2]
    ofstName  = 'OFST_' + dupList[2]

    tempName = CreateShapes.box()

    HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')
    HToolsLib.creatOffset(ofstName, ctrlName, jointName)

    dstName = ofstName
    cmds.parentConstraint(jointName, dstName)
    cmds.select(dstName, r=True)
    cmds.delete(cn=True)

    cmds.select(ctrlName, r=True)
    cmds.rotate(0, 0, 0)
    cmds.scale(1, 1, 1)

    HToolsLib.freezeAndDeletehistory()

    prefferdAngle = dupList[1] + '.preferredAngleY'
    angle = cmds.getAttr(prefferdAngle)
    #print(angle)
    if (angle <= 45):
        print('angle is OK')
    else:
        cmds.setAttr(prefferdAngle, 45)

    #def createIK(self):
    ctrlName = 'CTRL_IK_' + limbs[2] + pos
    pvName   = 'CTRL_PV_IK_'  + limbs[1] + pos
    ikName   = 'IKIK_' + limbs[2] + pos
    pVector  = ikName + '.poleVector'
    PVOffset = ikName + '_poleVectorConstraint1.offset'
    sJoint   = 'IK_' + limbs[0] + pos
    eEfector = 'IK_' + limbs[2] + pos

    cmds.ikHandle(n=ikName, sol='ikRPsolver', sj=sJoint, ee=eEfector)

    prePVValuX = cmds.getAttr(pVector + 'X')
    prePVValuY = cmds.getAttr(pVector + 'Y')
    prePVValuZ = cmds.getAttr(pVector + 'Z')
    
    cmds.pointConstraint(ctrlName, ikName, mo=True)

    cmds.poleVectorConstraint(pvName, ikName)
    pVValuX = cmds.getAttr(pVector + 'X')
    pVValuY = cmds.getAttr(pVector + 'Y')
    pVValuZ = cmds.getAttr(pVector + 'Z')

    setX = prePVValuX - pVValuX
    setY = prePVValuY - pVValuY
    setZ = prePVValuZ - pVValuZ

    cmds.setAttr(PVOffset + 'X', setX)
    cmds.setAttr(PVOffset + 'Y', setY)
    cmds.setAttr(PVOffset + 'Z', setZ)
    
    ##回転のコンスト
    srcCTRL = ctrlName
    dstJNT = 'IK_' + limbs[2] + pos
    cmds.orientConstraint(srcCTRL, dstJNT, mo=True)    


class BaseController():
    def __init__(self, nameSpaceName, primJointName, pos='_C', nodeType=''):
        self.primJntName   = primJointName
        self.pos           = pos
        self.NType         = nodeType
        self.ctrlName      = 'CTRL_' + self.primJntName + self.pos
        self.ofstName      = 'OFST_' + self.primJntName + self.pos
        self.jointName     = nameSpaceName + self.NType + self.primJntName + self.pos

    def setRotate(self, vec):
        #cmds.rotate(0, 180, 90)
        cmds.select(self.ctrlName, r=True)
        cmds.rotate(vec[0], vec[1], vec[2])
        HToolsLib.freezeAndDeletehistory()
        cmds.select(cl=True)

    def setScale(self, vec):
        #cmds.scale(1.2, 1.2, 1.2)
        cmds.select(self.ctrlName, r=True)
        cmds.scale(vec[0], vec[1], vec[2])
        HToolsLib.freezeAndDeletehistory()
        cmds.select(cl=True)

class ControllerCreator(BaseController):
    
    def createControllers(self, tempName):

        HToolsLib.renameAndColorV2(tempName, self.ctrlName, 'yellow')
        HToolsLib.creatOffset(self.ofstName, self.ctrlName, self.jointName)

        dstName = self.ofstName

        cmds.parentConstraint(self.jointName, dstName)
        cmds.select(dstName, r=True)
        cmds.delete(cn=True)

        cmds.select(self.ctrlName, r=True)

    def parentController(self, parent):
        #parent = 'CTRL_head_C'
        child  = self.ofstName
        cmds.parent(child, parent)
        
    def constraintController(self):
        #primJoint = 'head_C'
        driver = self.ctrlName
        driven = self.jointName
        cmds.parentConstraint(driver, driven, mo=True)

#使ってない
class LimbUnitIK():
    def __init__(self, limbs, pos):
        self.limbs = limbs
        self.pos   = pos    


    def createIKLimbs(self, isPositive):
        vecZPos = 0.5
        vecXRot = 90
        if isPositive:
            pass
        else:
            vecZPos *= -1
            vecXRot *= -1
        baseDupJoint = nameSpaceName + self.limbs[0] + self.pos
        dupList = dupulicateJoint(baseDupJoint, 'IK', nameSpaceName)
        ##creating IK Pole vector controller. 
        jointName = dupList[1]
        ctrlName  = 'CTRL_PV_' + dupList[1]
        
        tempName = CreateShapes.pyramid()

        HToolsLib.renameAndColorV2(tempName, ctrlName, 'blue')

        cmds.parentConstraint(jointName, ctrlName)
        cmds.select(ctrlName, r=True)
        cmds.delete(cn=True)

        cmds.select(ctrlName, r=True)
        cmds.move(0, 0, vecZPos, r=True, wd=True)
        cmds.rotate(vecXRot, 0, 0)
        cmds.scale(0.5, 0.5, 0.5)

        HToolsLib.freezeAndDeletehistory()

        ##creating IK controller.
        jointName = dupList[2]
        ctrlName  = 'CTRL_' + dupList[2]
        ofstName  = 'OFST_' + dupList[2]

        tempName = CreateShapes.box()

        HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')
        HToolsLib.creatOffset(ofstName, ctrlName, jointName)

        dstName = ofstName
        cmds.parentConstraint(jointName, dstName)
        cmds.select(dstName, r=True)
        cmds.delete(cn=True)

        cmds.select(ctrlName, r=True)
        cmds.rotate(0, 0, 0)
        cmds.scale(1, 1, 1)

        HToolsLib.freezeAndDeletehistory()

        prefferdAngle = dupList[1] + '.preferredAngleY'
        angle = cmds.getAttr(prefferdAngle)
        print(angle)
        if (angle <= 45):
            print('angle is OK')
        else:
            cmds.setAttr(prefferdAngle, 45)

    def createIK(self):
        ctrlName = 'CTRL_IK_' + self.limbs[2] + self.pos
        pvName   = 'CTRL_PV_IK_'  + self.limbs[1] + self.pos
        ikName   = 'IKIK_' + self.limbs[2] + self.pos
        pVector  = ikName + '.poleVector'
        PVOffset = ikName + '_poleVectorConstraint1.offset'
        sJoint   = 'IK_' + self.limbs[0] + self.pos
        eEfector = 'IK_' + self.limbs[2] + self.pos

        cmds.ikHandle(n=ikName, sol='ikRPsolver', sj=sJoint, ee=eEfector)

        prePVValuX = cmds.getAttr(pVector + 'X')
        prePVValuY = cmds.getAttr(pVector + 'Y')
        prePVValuZ = cmds.getAttr(pVector + 'Z')
        
        cmds.pointConstraint(ctrlName, ikName, mo=True)

        cmds.poleVectorConstraint(pvName, ikName)
        pVValuX = cmds.getAttr(pVector + 'X')
        pVValuY = cmds.getAttr(pVector + 'Y')
        pVValuZ = cmds.getAttr(pVector + 'Z')

        setX = prePVValuX - pVValuX
        setY = prePVValuY - pVValuY
        setZ = prePVValuZ - pVValuZ

        cmds.setAttr(PVOffset + 'X', setX)
        cmds.setAttr(PVOffset + 'Y', setY)
        cmds.setAttr(PVOffset + 'Z', setZ)
        
        ##回転のコンスト
        srcCTRL = ctrlName
        dstJNT = 'IK_' + self.limbs[2] + self.pos
        cmds.orientConstraint(srcCTRL, dstJNT, mo=True)       

class FKIKUnit():
    def __init__(self, isUp, pos):
        self.isUp = isUp
        self.pos  = pos

        self.limbs = ''
        self.switchName  = ''

    def checkLimbs(self):
        if self.isUp:
            self.limbs = ARM_LIMBS
            self.switchName = 'handCtrl_SWTC' + self.pos
        else:
            self.limbs = LEG_LIMBS
            self.switchName = 'footCtrl_SWTC' + self.pos
    
    def setLimbsFKSwitch(self):
        reverseName = 'rev' + self.limbs[2] + 'FK' + self.pos

        tempNodeName = cmds.shadingNode('reverse', asUtility=True)
        cmds.rename(tempNodeName, reverseName)		
        cmds.connectAttr(self.switchName + '.translateZ', reverseName + '.inputZ', f=True)


        for i in range(len(self.limbs)): #weponジョイントは操作したくない
            #ベイクジョイントとFK操作ジョイントのコンストレイント
            primName = self.limbs[i] + self.pos
            srcJoint = 'FK_' + primName
            dstJoint = nameSpaceName + primName
            dstJointconst = primName + '_parentConstraint1.'
            cmds.parentConstraint(srcJoint, dstJoint, mo=True)

            #reverseノードのアウトプットをウェイトとvisibilityに繋げる
            constWeight    = dstJointconst + srcJoint + 'W0'
            ctrlVisibility = 'CTRL_' + srcJoint + '.visibility'

            cmds.connectAttr(reverseName + '.outputZ', constWeight, f=True)
            cmds.connectAttr(reverseName + '.outputZ', ctrlVisibility, f=True)


    def setLimbsIKSwitch(self):

        for i in range(3): #weponジョイントは操作したくない
            #ベイクジョイントとIK操作ジョイントのコンストレイント
            primName = self.limbs[i] + self.pos
            srcJoint = 'IK_' + primName
            dstJoint = nameSpaceName + primName
            dstJointconst = primName + '_parentConstraint1.'
            cmds.parentConstraint(srcJoint, dstJoint, mo=True)

            #reverseノードのアウトプットをウェイトとvisibilityに繋げる
            constWeight = dstJointconst + srcJoint + 'W1'
            cmds.connectAttr(self.switchName + '.translateZ', constWeight, f=True)


        ctrlVisibility = 'CTRL_IK_' + self.limbs[2] + self.pos + '.visibility'
        cmds.connectAttr(self.switchName + '.translateZ', ctrlVisibility, f=True)

        ctrlVisibility = 'CTRL_PV_IK_' + self.limbs[1] + self.pos + '.visibility'
        cmds.connectAttr(self.switchName + '.translateZ', ctrlVisibility, f=True)

def createIKGroup(isUp, pos):
    if isUp:
        IK = 'hand'
    else:
        IK = 'foot'
    IKName = 'IKIK_' + IK + pos #IKIK_hand_L
    cmds.parent(IKName, IKGRP)

class CreateIK_TR_Controller():
    def __init__(self, prim, adjuster, pos):
        #IK_shoulder_L
        self.primJntName   = prim     #'IK_shoulder'
        self.adjusterName  = adjuster #'IKArmAdjuster'
        #orgJointName  = primJntName + '%02d' % i
        #pos           = '_C'
        self.pos           = pos
        self.ctrlName      = 'CTRL_' + self.adjusterName + self.pos
        self.ofstName      = 'OFST_' + self.adjusterName + self.pos
        #jointName     = nameSpaceName + orgJointName + pos
        self.jointName     = self.primJntName + self.pos

        #self.parentList    = ['OFST_IK_hand'+ self.pos, 'CTRL_PV_IK_arm'+ self.pos]
        #self.parentName    = 'armsFKIK_CTRL_GRP'

    def createIKTRC(self):
        tempName = CreateShapes.gear()
        HToolsLib.renameAndColorV2(tempName, self.ctrlName, 'red')
        HToolsLib.creatOffset(self.ofstName, self.ctrlName, self.jointName)

        cmds.select(self.ctrlName, r=True)
        cmds.rotate(0, 0, 90)
        cmds.scale(0.025, 0.025, 0.025)

        HToolsLib.freezeAndDeletehistory()
        HToolsLib.setKeyAble(self.ctrlName, 0, 0, 1)
    
    def parentIKTRC(self, parentList, grandParent):
        parentName = self.ctrlName
        for childController in parentList:
            cmds.parent(childController, parentName)

        childController = self.ofstName
        cmds.parent(childController, grandParent)
    
    def constIKTRC(self, switchName): #'handCtrl_SWTC' + self.pos
        driver = self.ctrlName
        driven = self.jointName
        cmds.parentConstraint(driver, driven, mo=True)

        ctrlVisibility = self.ctrlName + '.visibility'
        cmds.connectAttr(switchName + '.translateZ', ctrlVisibility, f=True)

def makeDogLegRig(pos):

    nameSpaceName = 'MODEL:'
    baseDupJoint = nameSpaceName + LEG_LIMBS[0] + pos

    #アッタチするための階層が綺麗なジョイントの作成（ベースジョイント）
    dupList = dupulicateJoint(baseDupJoint, 'IK', nameSpaceName)
    #コピーしたジョイントをリネーム
    IKBaseJoints = []
    for tempJoint in dupList:
        #print(tempJoint)
        cmds.rename(tempJoint, 'Base_' + tempJoint)
        IKBaseJoints.append('Base_' + tempJoint)
    print(IKBaseJoints)

    #4本をまとめて動かすジョイントの作成（名前考え中）
    dupList = dupulicateJoint(baseDupJoint, 'IK', nameSpaceName)
    #コピーしたジョイントをリネーム
    topHieralkyJoints = []
    for tempJoint in dupList:
        #print(tempJoint)
        cmds.rename(tempJoint, 'Top_' + tempJoint)
        topHieralkyJoints.append('Top_' + tempJoint)
    print(topHieralkyJoints[0])

	#上の奴（名前考え中）にIK通す
    topIK = cmds.ikHandle(n='top_IK_foot' + pos, sol='ikRPsolver', sj=topHieralkyJoints[0], ee=topHieralkyJoints[3])	#example of IK name 'aim_front_IK_L'
    cmds.setAttr(topIK[0] + '.visibility', 0)

	#太もも調整用のジョイントを作成（上下でセパレートしたやつ）
	#上側
    dupList = dupulicateJoint(baseDupJoint, 'IK', nameSpaceName)
    upJoints = []
    i=0
    for tempJoint in dupList:
        if i < 2:
            cmds.rename(tempJoint, 'Up_' + tempJoint)
            upJoints.append('Up_' + tempJoint)
        else:
            cmds.delete(tempJoint)
            break
        i+=1
	
	#print(upJoints)

	#下側
    dupList = dupulicateJoint(baseDupJoint, 'IK', nameSpaceName)
    downJoints = []
    for tempJoint in dupList:
        cmds.rename(tempJoint, 'Down_' + tempJoint)
        downJoints.append('Down_' + tempJoint)
	
    cmds.parent(downJoints[1], w=True)
    cmds.delete(downJoints[0])
	
	#上下でセパレートしたやつジョイントにIKを通す
    downIK = cmds.ikHandle(n='down_IK_foot' + pos, sol='ikRPsolver', sj=downJoints[1], ee=downJoints[3])	#example of IK name 'aim_front_IK_L'
    cmds.setAttr(downIK[0] + '.visibility', 0)

	#upとdownをコンストレイント
    cmds.pointConstraint(upJoints[1], downJoints[1])
	#名前考え中と上下でセパレートしやつをコネクト（子になるのは上下でセパレートしたやつ）

    uHip = ControllerCreator(nameSpaceName, 'hip', pos)
    tempName = CreateShapes.box()
    uHip.ctrlName = 'CTRL_IK_hip' + pos
    uHip.ofstName = 'OFST_IK_hip' + pos
    uHip.createControllers(tempName)
    #uHip.setRotate((180, 0, 90))
    uHip.setScale((1.5, 1, 1))
    HToolsLib.setKeyAble(uHip.ctrlName, 1, 0, 1)

    cmds.parentConstraint(topHieralkyJoints[0], uHip.ofstName)
    cmds.parentConstraint(uHip.ctrlName, upJoints[0])
    #ベースジョイントを上下セパの子にする
    cmds.parentConstraint(upJoints[0], IKBaseJoints[0])
    numOfJoint = len(IKBaseJoints)
    i = 1
    while i < numOfJoint:
        cmds.parentConstraint(downJoints[i], IKBaseJoints[i])
        i+=1

    #footのIKコントローラー作成（IK自体は仕込まない）
    #普通のlegと一緒にしたいなぁ
    uFoot = ControllerCreator(nameSpaceName, 'IK_foot', pos)
    tempName = CreateShapes.box()
    uFoot.jointName = 'Base_IK_foot' + pos
    uFoot.createControllers(tempName)
    #uFoot.setRotate((180, 0, 90))
    uFoot.setScale((1, 1, 1))

    #ポールベクター作成
    vecZPos = 0.75
    vecXRot = 90
    isPositive = True
    if isPositive:
        pass
    else:
        vecZPos *= -1
        vecXRot *= -1
    
    ##creating IK Pole vector controller. 
    jointName = IKBaseJoints[1]
    ctrlName  = 'CTRL_leg_TW' + pos #'CTRL_PV_' + IKBaseJoints[1]
    
    tempName = CreateShapes.pyramid()

    HToolsLib.renameAndColorV2(tempName, ctrlName, 'blue')

    cmds.parentConstraint(jointName, ctrlName)
    cmds.select(ctrlName, r=True)
    cmds.delete(cn=True)

    cmds.select(ctrlName, r=True)
    cmds.move(0, 0, vecZPos, r=True, wd=True)
    cmds.rotate(vecXRot, 0, 0)
    cmds.scale(0.25, 0.4, 0.25)

    HToolsLib.freezeAndDeletehistory()

    parentDogLeg(pos)



    constDogLegIK(pos)


def parentDogLeg(pos):

    #ペアレント
    #ctrlName = 'IK_foot_CTRL' + pos

    #cmds.parent('footfinger_IK_OFST' + LR, ctrlName)
    #setKeyAble(ctrlName, 0, 0, 1)
    #setKeyAble('footfinger_IK_CTRL' + LR, 1, 0, 1)

    ikCtrlName = 'footIK_CTRL_GRP'
    if not cmds.objExists(ikCtrlName):
        cmds.group(w=True, em=True, n=ikCtrlName)

    cmds.parent('OFST_IK_foot' + pos, ikCtrlName)
    cmds.parent('CTRL_leg_TW' + pos, ikCtrlName)
    HToolsLib.setKeyAble('CTRL_IK_foot' + pos, 0, 0, 1)
    HToolsLib.setKeyAble('CTRL_leg_TW' + pos, 0, 1, 1)
    #cmds.setAttr('leg_TW_CTRL' + pos + '.ty', keyable=False, lock=True)
    #cmds.setAttr('leg_TW_CTRL' + pos + '.tz', keyable=False, lock=True)

    cmds.parent('OFST_IK_hip' + pos, 'footIK_CTRL_GRP')
    HToolsLib.setKeyAble('OFST_IK_hip' + pos, 1, 0, 1)

    IKGroupName = 'DogLegIK_GRP'
    if not cmds.objExists(IKGroupName):
        cmds.group(w=True, em=True, n=IKGroupName)

    cmds.parent('top_IK_foot' + pos, IKGroupName)
    cmds.parent('down_IK_foot' + pos, IKGroupName)

    jointGroupName = 'legsFKIK_JNT_GRP'
    if not cmds.objExists(jointGroupName):
        cmds.group(w=True, em=True, n=jointGroupName)

    #cmds.parent('thigh_JNT_FK' + pos, jointGroupName)
    cmds.parent('Base_IK_hip' + pos, jointGroupName)
    cmds.parent('Up_IK_hip' + pos, jointGroupName)
    cmds.parent('Down_IK_thigh' + pos, jointGroupName)

    cmds.parent('Top_IK_hip' + pos, 'CTRL_hip_C')#お尻振った時にthighコントローラーが付いてくるように



def constDogLegIK(pos):
	ctrlName   = 'CTRL_IK_foot' + pos
	topIKName  = 'top_IK_foot' + pos
	downIKName = 'down_IK_foot' + pos

	cmds.pointConstraint(ctrlName, topIKName, mo=True)
	cmds.pointConstraint(ctrlName, downIKName, mo=True)

	srcCTRL = 'CTRL_IK_foot' + pos
	dstJNT  = 'Down_IK_foot' + pos
	cmds.orientConstraint(srcCTRL, dstJNT, mo=True)



	#これは関数にまとめていいのではないでしょうか
	#だめっぽいです
	TWName       = 'CTRL_leg_TW' + pos
	topTwistAtt  = topIKName + '.twist'
	downTwistAtt = downIKName + '.twist'

	tempNodeName = cmds.shadingNode('multiplyDivide', asUtility=True)
	tweakTwist = cmds.rename(tempNodeName, 'MD4LegTwist')
	cmds.connectAttr(TWName + '.translateX', tweakTwist + '.input1X', f=True)
	cmds.connectAttr(tweakTwist + '.outputX', topTwistAtt, f=True)
	cmds.connectAttr(tweakTwist + '.outputX', downTwistAtt, f=True)
	cmds.setAttr(tweakTwist + '.input2X', 0.25)

def setDogLegIKSwitch(pos):
    switchName = 'footCtrl_SWTC' + pos
    '''
    if isBird:
        jointList = ('thigh', 'calf', 'foot', 'ball', 'afootfinger_01', 'afootfinger_02',
                     'bfootfinger_01', 'bfootfinger_02')
    else:
        jointList = ('thigh', 'calf', 'foot', 'ball', 'footfinger')
    '''
    for joint in LEG_LIMBS:
        #ベイクジョイントとIK操作ジョイントのコンストレイント
        srcJoint = 'Base_IK_' + joint + pos
        dstJoint = 'MODEL:' + joint + pos
        cmds.parentConstraint(srcJoint, dstJoint, mo=True)

        #スウィッチの数値をウェイトと繋げる
        constWeight = joint + pos + '_parentConstraint1.' + 'Base_IK_' + joint + pos + 'W1'

        cmds.connectAttr(switchName + '.translateZ', constWeight, f=True)

	#スイッチの数値とコントローラーの表示に繋げる
    '''
    if isBird:
        ctrlVisibilities = ('thigh_IK_CTRL' + LR, 'IK_foot_CTRL' + LR, 
                            'afootfinger_01_IK_CTRL' + LR, 'afootfinger_02_IK_CTRL' + LR,
                            'bfootfinger_01_IK_CTRL' + LR, 'bfootfinger_02_IK_CTRL' + LR,
                            'leg_TW_CTRL' + LR)
	else:
		ctrlVisibilities = ('thigh_IK_CTRL' + LR, 'IK_foot_CTRL' + LR, 'footfinger_IK_CTRL' + LR, 'leg_TW_CTRL' + LR)
    '''
    ctrlVisibilities = ('CTRL_IK_hip' + pos, 'CTRL_IK_foot' + pos, 'CTRL_leg_TW' + pos)
    for vis in ctrlVisibilities:
        cmds.connectAttr(switchName + '.translateZ', vis + '.visibility', f=True)

def hinan():

	#footfingerのコントローラーの作成
    if isBird:
        fingerType = ('a', 'b')
        i = 1
        while i < 3:
            for finger in fingerType:
                birdJointName = finger + 'footfinger_0' + str(i)
                rig = CreateControllers(birdJointName, LR)
                rig.jntName = 'Base_' + birdJointName + '_JNT_IK' + LR
                rig.ctrlName = birdJointName + '_IK_CTRL' + LR
                rig.ofstName = birdJointName + '_IK_OFST' + LR
                rig.createIKBox(0, 0, 0, scale, scale, scale, 22)

            i+=1

	else:
		rig = CreateControllers('footfinger', LR)
		rig.jntName = 'Base_footfinger_JNT_IK' + LR
		rig.ctrlName = 'footfinger_IK_CTRL' + LR
		rig.ofstName = 'footfinger_IK_OFST' + LR
		rig.createIKBox(0, 0, 0, scale, scale, scale, 22)
	
	#ツイストコントローラー作成
	ctrlName = 'leg_TW_CTRL' + LR
	jntName = 'Base_foot_JNT_IK' + LR

	NCC.createPoleVectorCTRL(ctrlName, jntName)

#↓こいつはここじゃない場所で管理する
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

def constAllJoints():
    #リグが組まれた墨兵ベースのジョイントと各職業の墨兵のジョイントをコンストする
    '''
    ALL_JOINT_01  = ('Root', 'hip_C', 'hair01_C', 'hair02_C', 'tail01_C', 'tail02_C')
    
    for joint in ALL_JOINT_01:
        for i in range(1, 5):
            driver = 'MODEL:' + joint
            driven   = 'MODEL{}:'.format(i) + joint
            cmds.parentConstraint(driver, driven, mo=True)
            cmds.scaleConstraint(driver, driven, mo=True)
    
    for joint in ARM_LIMBS:
        for pos in POS_LIST:
            for i in range(1, 5):
                driver = 'MODEL:' + joint + pos
                driven   = 'MODEL{}:'.format(i) + joint + pos
                cmds.parentConstraint(driver, driven, mo=True)
                cmds.scaleConstraint(driver, driven, mo=True)
    '''
    #龍神テスト用
    JOINT_LIST_01 = ('Root', 'head_C', 'mouth_C')
    
    for joint in JOINT_LIST_01:
        driver = nameSpaceName + joint
        driven = nameSpaceName + 'before_joint_oriented:' + joint

        cmds.parentConstraint(driver, driven, mo=True)
    
    for i in range(1, 11):
        joint = 'spine%02d' % i + '_C'
        driver = nameSpaceName + joint
        driven = nameSpaceName + 'before_joint_oriented:' + joint

        cmds.parentConstraint(driver, driven, mo=True)
    


if __name__ == '__main__':
    main()