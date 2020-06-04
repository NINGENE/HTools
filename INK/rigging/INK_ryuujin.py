# __*__ coding: utf-8 __*__
from maya import cmds, mel
from HTools.lib import HToolsLib, CreateShapes
reload(HToolsLib)
reload(CreateShapes)

'''
開始日 2020/5/18
isUpはクラスにしたいな～
そもそもisUpのチェックは関数化したい
'''

#colors = {'red':13, 'yellow':22, 'blue':15}
nameSpaceName = ''

POS_LIST = ('_L', '_R')

#ARM_LIMBS = ('shoulder', 'arm', 'hand', 'weapon')
ARM_LIMBS = ('shoulder', 'arm', 'hand')
LEG_LIMBS = ('thigh', 'leg', 'foot')

IK_ARM_CTRLS = ('PV_IK_arm', 'IK_hand') #'CTRL_PV_IK_arm_L'
IK_LEG_CTRLS = ('PV_IK_leg', 'IK_foot')

IKGRP = 'IK_GRP'

def main():
    #とりあえずspineはおっけーそうなので、手足と頭のセカンダリをやる
    #頭は移動出来るように

    checkNamespace()

    #ほんちゃんデータでは要らない
    #constAllJoints()

    createGeneCtrl()

    childController = 'CTRL_tr_C'
    cmds.parent(childController, 'CTRL_Root')
    HToolsLib.setKeyAble(childController, 0, 0, 1)

    head = HeadUnit()
    head.createHUControllers()
    head.parentHUC()
    head.constHUC()
    #print(head.rootController)

    spines = []
    for i in range(1, 10):
        jointName = 'spine%02d' % i
        pos = '_C'
        spine = SpineController(jointName, pos)
        spine.createController()

        spines.append(spine)
    
    lastChild = ''    
    for spine in spines:
        if spine == spines[0]:
            pass
        else:
            parent = lastChild
            child  = spine.ofstName
            cmds.parent(child, parent)

        lastChild = spine.ctrlName
        print(lastChild)
    
    for spine in spines:
        cmds.parentConstraint(spine.ctrlName, spine.jointName)

    #FKLimbs = []
    for pos in POS_LIST:
        armFKLimb = LimbUnitFK(ARM_LIMBS, pos)
        armFKLimb.createFKLimbs()
        armFKLimb.parentFKLimbs()
        armFKLimb.constFKLimbs()
        #FKLimbs.append(armFKLimb)
        
        legFKLimb = LimbUnitFK(LEG_LIMBS, pos)
        legFKLimb.createFKLimbs()
        legFKLimb.parentFKLimbs()
        legFKLimb.constFKLimbs()
        #FKLimbs.append(legFKLimb)

        armIKLimb = LimbUnitIK(ARM_LIMBS, pos)
        armIKLimb.createIKLimbs(False)
        armIKLimb.createIK()

        legIKLimb = LimbUnitIK(LEG_LIMBS, pos)
        legIKLimb.createIKLimbs(True)
        legIKLimb.createIK()

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
    
    for pos in POS_LIST:
        parentName = legsGroup
        childName  = 'FK_thigh' + pos
        cmds.parent(childName, parentName)

        childName = 'IK_thigh' + pos
        cmds.parent(childName, parentName)

    cmds.parent(armsGroup, 'CTRL_spine03_C')
    cmds.parent(legsGroup, 'CTRL_spine06_C')

    CreateShapes.createFKIKSwitch(0.025)

    for pos in POS_LIST:
        setLimbsFKSwitch(True, pos)
        setLimbsIKSwitch(True, pos)   
        
        setLimbsFKSwitch(False, pos)
        setLimbsIKSwitch(False, pos)            

    cmds.select('FKIK_SWITCH_GRP')
    cmds.move(5, 5, 0)
    cmds.rotate(90, 0, 0)
    cmds.select(cl=True)

    cmds.group(w=True, em=True, n=IKGRP)
    for pos in POS_LIST:
        createIKGroup(True, pos)
        createIKGroup(False, pos)
    cmds.parent(IKGRP, 'CTRL_Root')
    
    cmds.parent('FKIK_SWITCH_GRP', 'CTRL_tr_C')

    #ユニットのトップノードをペアレント
    parentController = 'CTRL_tr_C'
    childController = 'OFST_head_C'
    cmds.parent(childController, parentController)
    HToolsLib.setKeyAble(childController, 0, 0, 1)

    childController = 'OFST_spine01_C'
    cmds.parent(childController, parentController)
    #HToolsLib.setKeyAble(childController, 0, 0, 1)

    parentController = 'CTRL_spine03_C'
    for pos in POS_LIST:
        childController = 'OFST_FK_shoulder' + pos
        cmds.parent(childController, parentController)
        HToolsLib.setKeyAble(childController, 0, 0, 1)

    parentController = 'CTRL_spine06_C'
    for pos in POS_LIST:
        childController = 'OFST_FK_thigh' + pos
        cmds.parent(childController, parentController)
        HToolsLib.setKeyAble(childController, 0, 0, 1)        

    armsGroup = 'armsIK_CTRL_GRP'
    legsGroup = 'legsIK_CTRL_GRP'
    cmds.group(w=True, em=True, n=armsGroup)
    cmds.group(w=True, em=True, n=legsGroup)

    for pos in POS_LIST:
        armAdjuster = CreateIK_TR_Controller('IK_shoulder', 'IKArmAdjuster' ,pos)
        armAdjuster.createIKTRC()
        parentList = ['OFST_IK_hand' + pos, 'CTRL_PV_IK_arm' + pos]
        armAdjuster.parentIKTRC(parentList, armsGroup)
        armAdjuster.constIKTRC('handCtrl_SWTC'+pos)

        legAdjuster = CreateIK_TR_Controller('IK_thigh', 'IKLegAdjuster' ,pos)
        legAdjuster.createIKTRC()
        parentList = ['OFST_IK_foot' + pos, 'CTRL_PV_IK_leg' + pos]
        legAdjuster.parentIKTRC(parentList, legsGroup)
        legAdjuster.constIKTRC('footCtrl_SWTC'+pos)

    
    parentController = 'CTRL_spine03_C'
    childController = 'armsIK_CTRL_GRP'
    cmds.parent(childController, parentController)
    HToolsLib.setKeyAble(childController, 0, 0, 1)
    
    parentController = 'CTRL_spine06_C'
    childController = 'legsIK_CTRL_GRP'
    cmds.parent(childController, parentController)
    HToolsLib.setKeyAble(childController, 0, 0, 1)

    #createDL()

    #cmds.confirmDialog(t='test', m='It dosent have special IK yet.')




def checkNamespace():
    global nameSpaceName
    if cmds.objExists('MODEL:Root'):
        nameSpaceName = 'MODEL:'
        print('NameSpace is ' + str(nameSpaceName))
    else:
        print('It has no NameSpace.')

def createDL():
    geoName = nameSpaceName + 'body'
    
    cmds.select(cl=True)
    cmds.select(geoName)
    cmds.createDisplayLayer( noRecurse=True, name='geo_layer' )

    cmds.select(cl=True)
    cmds.select('CTRL_ScaleGround_C')
    cmds.select('CTRL_ScaleCenter_C', add=True)
    cmds.createDisplayLayer( noRecurse=True, name='scale_controller_layer' )
    cmds.select(cl=True)

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

#↓使ってない
def createCoreContoroller():
    ##Hipコントローラー
    '''    
    orgJointName = 'hip'
    pos = '_C'
    ctrlName   = 'CTRL_' + orgJointName + pos
    ofstName   = 'OFST_' + orgJointName + pos #墨兵用
    jointName  = nameSpaceName + orgJointName + pos

    tempName = CreateShapes.cross()
    HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')
    HToolsLib.creatOffset(ofstName, ctrlName, jointName, False) #墨兵用

    cmds.select(ctrlName, r=True)
    cmds.rotate(0, 0, 0)
    cmds.scale(0.5, 0.5, 0.5)

    HToolsLib.freezeAndDeletehistory()
    '''
    ##creating FK controller of core joints.
    coreJoints = ('head', 'mouth')
    pos = '_C'
    for joint in coreJoints:
        primJntName = joint
        jointName  = nameSpaceName + primJntName + pos
        ofstName  = 'OFST_' + primJntName + pos
        ctrlName  = 'CTRL_' + primJntName + pos

        tempName = CreateShapes.ototsuCircle()

        HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')
        HToolsLib.creatOffset(ofstName, ctrlName, jointName)

        dstName = ofstName

        cmds.parentConstraint(jointName, dstName)
        cmds.select(dstName, r=True)
        cmds.delete(cn=True)

        cmds.select(ctrlName, r=True)
        cmds.rotate(0, 180, 90)
        cmds.scale(1.2, 1.2, 1.2)

        HToolsLib.freezeAndDeletehistory()



class HeadUnit():
    def __init__(self):
        self.headJointsA  = ['head', 'jaw']
        self.headSubJoint = ['beard']
        
        self.rootController = 'CTRL_head_C'
    
    def createHUControllers(self):
        pos = '_C'
        
        primJntName = self.headJointsA[0]
        jointName  = nameSpaceName + primJntName + pos
        ofstName   = 'OFST_' + primJntName + pos
        ctrlName   = 'CTRL_' + primJntName + pos
        
        tempName = CreateShapes.cross()

        HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')
        HToolsLib.creatOffset(ofstName, ctrlName, jointName)

        dstName = ofstName

        cmds.parentConstraint(jointName, dstName)
        cmds.select(dstName, r=True)
        cmds.delete(cn=True)

        cmds.select(ctrlName, r=True)
        cmds.rotate(0, 180, 90)
        cmds.scale(1.2, 1.2, 1.2)

        HToolsLib.freezeAndDeletehistory()

        primJntName = self.headJointsA[1]
        jointName  = nameSpaceName + primJntName + pos
        ofstName  = 'OFST_' + primJntName + pos
        ctrlName  = 'CTRL_' + primJntName + pos

        tempName = CreateShapes.linerCircle()

        HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')
        HToolsLib.creatOffset(ofstName, ctrlName, jointName)

        dstName = ofstName

        cmds.parentConstraint(jointName, dstName)
        cmds.select(dstName, r=True)
        cmds.delete(cn=True)

        cmds.select(ctrlName, r=True)
        cmds.rotate(90, 0, 90)
        cmds.scale(1.2, 1.2, 1.2)

        HToolsLib.freezeAndDeletehistory()        

        for pos in POS_LIST:
            for i in range(1, 3):
                primJntName = self.headSubJoint[0] + '%02d' % i
                jointName  = nameSpaceName + primJntName + pos
                ofstName  = 'OFST_' + primJntName + pos
                ctrlName  = 'CTRL_' + primJntName + pos

                tempName = CreateShapes.linerCircle()

                HToolsLib.renameAndColorV2(tempName, ctrlName, 'blue')
                HToolsLib.creatOffset(ofstName, ctrlName, jointName)

                dstName = ofstName

                cmds.parentConstraint(jointName, dstName)
                cmds.select(dstName, r=True)
                cmds.delete(cn=True)

                cmds.select(ctrlName, r=True)
                cmds.rotate(0, 180, 90)
                cmds.scale(0.3, 0.3, 0.3)

                HToolsLib.freezeAndDeletehistory()

    def parentHUC(self):
        parent = 'CTRL_head_C'
        child  = 'OFST_jaw_C'
        cmds.parent(child, parent)
        #ひげ
        for pos in POS_LIST:
            parent = 'CTRL_head_C'
            child  = 'OFST_beard01' + pos
            cmds.parent(child, parent)

            parent = 'CTRL_beard01' + pos
            child  = 'OFST_beard02' + pos
            cmds.parent(child, parent)
        
    def constHUC(self):
        primJoint = 'head_C'
        driver = 'CTRL_' + primJoint
        driven = nameSpaceName + primJoint
        cmds.parentConstraint(driver, driven, mo=True)

        primJoint = 'jaw_C'
        driver = 'CTRL_' + primJoint
        driven = nameSpaceName + primJoint
        cmds.orientConstraint(driver, driven, mo=True)

        for pos in POS_LIST:
            for i in range(1, 3):
                primJoint = 'beard%02d' % i + pos
                driver = 'CTRL_' + primJoint
                driven = nameSpaceName + primJoint
                cmds.orientConstraint(driver, driven, mo=True)


#おいおいやる
'''
class ControllerUnit():
    def __init__(self, joint, pos):
        self.primJntName   = joint
        self.pos           = pos
        self.ctrlName      = 'CTRL_' + joint + self.pos
        self.ofstName      = 'OFST_' + joint + self.pos
        self.jointName     = nameSpaceName + self.primJntName + self.pos

        self.rot   = [0, 0, 0]
        self.scale = [1, 1, 1]
'''

class SpineController():
    def __init__(self, joint, pos):
        self.primJntName   = joint
        self.pos           = pos
        self.ctrlName      = 'CTRL_' + joint + self.pos
        self.ofstName      = 'OFST_' + joint + self.pos
        self.jointName     = nameSpaceName + self.primJntName + self.pos

    def createController(self):
        tempName = CreateShapes.ototsuCircle()
        HToolsLib.renameAndColorV2(tempName, self.ctrlName, 'yellow')
        HToolsLib.creatOffset(self.ofstName, self.ctrlName, self.jointName)

        cmds.select(self.ctrlName, r=True)
        cmds.rotate(0, 0, 90)
        cmds.scale(1, 1, 1)

        HToolsLib.freezeAndDeletehistory()
        HToolsLib.setKeyAble(self.ctrlName, 1, 0, 1)

    #def parentIKTRC(self):
    #    PARENT_LIST = ('OFST_IK_hand'+ self.pos, 'CTRL_PV_IK_arm'+ self.pos)
    #    parentName = self.ctrlName
    #    for childController in PARENT_LIST:
    #        cmds.parent(childController, parentName)

    #    parentName='armsFKIK_CTRL_GRP'
    #    childController = self.ofstName
    #    cmds.parent(childController, parentName)

    def constController(self):
        driver = self.ctrlName
        driven = self.jointName
        cmds.parentConstraint(driver, driven, mo=True)

        #switchName     = 'handCtrl_SWTC' + self.pos
        #ctrlVisibility = self.ctrlName + '.visibility'
        #cmds.connectAttr(switchName + '.translateZ', ctrlVisibility, f=True)

#FKとIKのクラスは一緒にしたい
class LimbUnitFK():
    def __init__(self, limbs, pos):
        self.limbs = limbs
        self.pos   = pos

    def createFKLimbs(self):
        baseDupJoint = nameSpaceName + self.limbs[0] + self.pos
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

    def parentFKLimbs(self):
        lastChild = ''
        #print(lastSpineName)
        for limb in self.limbs:
            if limb == self.limbs[0]:
                pass    
            else:
                parent  = lastChild
                child   = 'OFST_FK_' + limb + self.pos
            
                cmds.parent(child, parent)
            
            ctrl  = 'CTRL_FK_' + limb + self.pos
            HToolsLib.setKeyAble(ctrl, 0, 0, 1)
            lastChild = ctrl

    def constFKLimbs(self):
        for limb in self.limbs:
            driver = 'CTRL_FK_' + limb + self.pos
            driven = 'FK_' + limb + self.pos
            cmds.parentConstraint(driver, driven, mo=True)

#FKとIKのクラスは一緒にしたい
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
            print('OK')
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

#↓使ってない
def parentCorecontroller():
    ##parent a Root ~ Head.
    childController = 'CTRL_tr_C'
    cmds.parent(childController, 'CTRL_Root')
    HToolsLib.setKeyAble(childController, 0, 0, 1)
    lastSpineName = childController

    #childController = 'CTRL_hip_C'
    childController = 'OFST_hip_C' #墨兵用
    cmds.parent(childController, lastSpineName)
    HToolsLib.setKeyAble(childController, 0, 0, 1)
    #lastSpineName = childController
    lastSpineName = 'CTRL_hip_C' 

    childController = 'CTRL_hair01_C'
    cmds.parent(childController, lastSpineName)
    HToolsLib.setKeyAble(childController, 0, 0, 1)
    lastSpineName = childController

    childController = 'CTRL_hair02_C'
    cmds.parent(childController, lastSpineName)
    HToolsLib.setKeyAble(childController, 0, 0, 1)
    lastSpineName = childController



def check_weponJoint(pos):
    #IK使用時に非表示なるので、spineの子にする（墨兵はヒップ
    if cmds.objExists(nameSpaceName + 'weapon' + pos):
        ofstName  = 'OFST_FK_weapon' + pos
        ctrlName  = 'CTRL_FK_weapon' + pos
    
        cmds.parent(ofstName, 'CTRL_hip_C')
        HToolsLib.setKeyAble(ctrlName, 0, 0, 1)

#使ってない
def parentFKIKJoints(isUp, pos, greatParent):
    #こういうのクラスでもいいかも？if以下はほぼ同じ事やってるし
    ##parenting FK and IK joints.
    armsGroup = 'armsFKIK_JNT_GRP'
    legsGroup = 'legsFKIK_JNT_GRP'
    isChild   = True
    if isUp:
        if not cmds.objExists(armsGroup):
            cmds.group(w=True, em=True, n=armsGroup)
            isChild = False
        parentName = armsGroup
        jointName  = ARM_LIMBS[0]
    else:
        if not cmds.objExists(legsGroup):
            cmds.group(w=True, em=True, n=legsGroup)
            isChild = False
        parentName = legsGroup
        jointName  = LEG_LIMBS[0]

    childName = 'FK_' + jointName + pos
    cmds.parent(childName, parentName)

    childName = 'IK_' + jointName + pos
    cmds.parent(childName, parentName)
    
    if not isChild:
        cmds.parent(parentName, greatParent)

def parentIKControllers(isUp, pos):
    ##parenting IK contollers.
    parentName = 'CTRL_tr_C'
    isChild = True
    if isUp:
        groupName = 'armsFKIK_CTRL_GRP'
        IKControllers = IK_ARM_CTRLS
    else:
        groupName = 'legsFKIK_CTRL_GRP'
        IKControllers = IK_LEG_CTRLS
    
    if not cmds.objExists(groupName):
        cmds.group(w=True, em=True, n=groupName)
        isChild = False
    
    for i in range(2):
        if i == 0:
            childName = 'CTRL_' + IKControllers[i] + pos
        else:
            childName = 'OFST_' + IKControllers[i] + pos
        cmds.parent(childName, groupName)
    
    if not isChild:
        cmds.parent(groupName, parentName)

def contollerConst():
    constList = ['Root', 'hip_C']
    for const in constList:
        driver = 'CTRL_' + const
        driven = nameSpaceName + const
        cmds.parentConstraint(driver, driven, mo=True)

    constList = ['hair01_C', 'hair02_C']

    for const in constList:
        driver = 'CTRL_' + const
        driven = nameSpaceName + const
        cmds.parentConstraint(driver, driven, mo=True)

    constList = ['weapon_L', 'weapon_R']
    
    for const in constList:
        driver = 'CTRL_FK_' + const
        driven = nameSpaceName + const
        cmds.parentConstraint(driver, driven, mo=True)     

    cmds.parentConstraint('MODEL:hand_L', 'OFST_FK_weapon_L', mo=True)        
    cmds.parentConstraint('MODEL:hand_R', 'OFST_FK_weapon_R', mo=True)        

    ##FKコントローラーとFK用ジョイントのコンストレイント
    #weaponジョイントは大本で操作したいのでここでは外す

    for pos in POS_LIST:
        for limb in ARM_LIMBS:
            driver = 'CTRL_FK_' + limb  + pos
            driven = 'FK_' + limb + pos

            cmds.parentConstraint(driver, driven, mo=True)

#↓使ってない
def createIK(isUp, pos):

    if isUp:
        limbs = ARM_LIMBS
    else:
        limbs = LEG_LIMBS

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

def setLimbsFKSwitch(isUp, pos):
    if isUp:
        limbs = ARM_LIMBS
        switchName = 'handCtrl_SWTC' + pos
    else:
        limbs = LEG_LIMBS
        switchName = 'footCtrl_SWTC' + pos

    reverseName = 'rev' + limbs[2] + 'FK' + pos

    tempNodeName = cmds.shadingNode('reverse', asUtility=True)
    cmds.rename(tempNodeName, reverseName)		
    cmds.connectAttr(switchName + '.translateZ', reverseName + '.inputZ', f=True)


    for i in range(3): #weponジョイントは操作したくない
        #ベイクジョイントとFK操作ジョイントのコンストレイント
        primName = limbs[i] + pos
        srcJoint = 'FK_' + primName
        dstJoint = nameSpaceName + primName
        dstJointconst = primName + '_parentConstraint1.'
        cmds.parentConstraint(srcJoint, dstJoint, mo=True)

        #reverseノードのアウトプットをウェイトとvisibilityに繋げる
        constWeight    = dstJointconst + srcJoint + 'W0'
        ctrlVisibility = 'CTRL_' + srcJoint + '.visibility'

        cmds.connectAttr(reverseName + '.outputZ', constWeight, f=True)
        cmds.connectAttr(reverseName + '.outputZ', ctrlVisibility, f=True)


def setLimbsIKSwitch(isUp, pos):

    if isUp :
        limbs = ARM_LIMBS
        switchName = 'handCtrl_SWTC' + pos
    else:
        limbs = LEG_LIMBS
        switchName = 'footCtrl_SWTC' + pos

    for i in range(3): #weponジョイントは操作したくない
        #ベイクジョイントとIK操作ジョイントのコンストレイント
        primName = limbs[i] + pos
        srcJoint = 'IK_' + primName
        dstJoint = nameSpaceName + primName
        dstJointconst = primName + '_parentConstraint1.'
        cmds.parentConstraint(srcJoint, dstJoint, mo=True)

        #reverseノードのアウトプットをウェイトとvisibilityに繋げる
        constWeight = dstJointconst + srcJoint + 'W1'
        cmds.connectAttr(switchName + '.translateZ', constWeight, f=True)


    ctrlVisibility = 'CTRL_IK_' + limbs[2] + pos + '.visibility'
    cmds.connectAttr(switchName + '.translateZ', ctrlVisibility, f=True)

    ctrlVisibility = 'CTRL_PV_IK_' + limbs[1] + pos + '.visibility'
    cmds.connectAttr(switchName + '.translateZ', ctrlVisibility, f=True)

def createIKGroup(isUp, pos):
    if isUp:
        IK = 'hand'
    else:
        IK = 'foot'
    IKName = 'IKIK_' + IK + pos #IKIK_hand_L
    cmds.parent(IKName, IKGRP)

#ここからサブ
#このテイル系はクラスに出来そう
def createTail():
    i = 1
    while True:
        primJntName   = 'tail'
        orgJointName  = primJntName + '%02d' % i
        pos           = '_C'
        ctrlName      = 'CTRL_' + orgJointName + pos
        ofstName      = 'OFST_' + orgJointName + pos
        jointName     = nameSpaceName + orgJointName + pos

        if cmds.objExists(jointName):
            tempName = CreateShapes.linerCircle()
            HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')
            HToolsLib.creatOffset(ofstName, ctrlName, jointName)

            cmds.select(ctrlName, r=True)
            cmds.rotate(0, 0, 90)
            cmds.scale(0.3, 0.3, 0.3)

            HToolsLib.freezeAndDeletehistory()
            
            HToolsLib.setKeyAble(ctrlName, 0, 0, 1)

            i += 1
        else:
            break    

def parentTail():
    i = 1
    while True:
        primJntName   = 'tail'
        orgJointName  = primJntName + '%02d' % i
        pos           = '_C'
        #ctrlName      = 'CTRL_' + orgJointName + pos
        ctrlName      = 'CTRL_' + primJntName + '%02d' % (i-1) + pos
        ofstName      = 'OFST_' + orgJointName + pos
        jointName     = nameSpaceName + orgJointName + pos
        grandParent   = 'CTRL_hip_C'

        if cmds.objExists(jointName):
            if i == 1:
                childController = ofstName
                parentName      = grandParent
            else:
                childController = ofstName
                parentName      = ctrlName
            cmds.parent(childController, parentName)
            i += 1
        else:
            break    

def constTail():
    i = 1
    while True:
        primJntName   = 'tail'
        orgJointName  = primJntName + '%02d' % i
        pos           = '_C'
        ctrlName      = 'CTRL_' + orgJointName + pos
        #ctrlName      = 'CTRL_' + primJntName + '%02d' % (i-1) + pos
        #ofstName      = 'OFST_' + orgJointName + pos
        jointName     = nameSpaceName + orgJointName + pos

        driver = ctrlName
        driven = jointName
        #grandParent   = 'CTRL_hip_C'

        if cmds.objExists(jointName):
            cmds.parentConstraint(driver, driven, mo=True)
            i += 1
        else:
            break   

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


#↓こいつはここじゃない場所で管理する
def dupulicateJoint(jointName, FKIKtype, NameSpace = None):
    tempDupNames = cmds.duplicate(jointName)
    cmds.parent(tempDupNames[0], w=True)

    cmds.select(cl=True)
    if not NameSpace:
        cmds.select(jointName, hi=True)
        originalJointNames = cmds.ls(sl=True)
        cmds.select(cl=True)
        print(1)
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