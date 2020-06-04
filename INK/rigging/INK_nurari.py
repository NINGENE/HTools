# __*__ coding: utf-8 __*__
from maya import cmds, mel
from HTools.lib import HToolsLib, CreateShapes
reload(HToolsLib)
reload(CreateShapes)

'''
作成日 2020/4/28
'''

#colors = {'red':13, 'yellow':22, 'blue':15}
def main():
    nameSpaceName = ''
    if cmds.objExists('MODEL:Root'):
        nameSpaceName = 'MODEL:'
    else:
        print('It has no NameSpace.')

    contorollerCreate(nameSpaceName)
    
    createLimbs(nameSpaceName)

    LRList = ['_L', '_R']
    for LR in LRList:
        cmds.delete('FK_sode' + LR)
        cmds.delete('IK_sode' + LR)
        cmds.delete('OFST_FK_sode' + LR)
        
        createSode(nameSpaceName, LR)
    
    controllerParent()
    for LR in LRList:
       parentSode(LR)
    contollerConst(nameSpaceName)

    for LR in LRList:
        sode = ConstSode('sode', LR)
        sode.constSode()
    
    createIK()
    setLimbsFKSwitch()
    setLegIKSwitch()
    createIKGroup()

def contorollerCreate(nameSpaceName = ''):
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

    ##Hipコントローラー
    orgJointName = 'hip'
    pos = '_C'
    ctrlName   = 'CTRL_' + orgJointName + pos
    #ofstName   = 'OFST_' + orgJointName + pos
    jointName  = nameSpaceName + orgJointName + pos

    tempName = CreateShapes.cross()
    HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')

    cmds.pointConstraint(jointName, ctrlName)
    cmds.select(ctrlName, r=True)
    cmds.delete(cn=True)

    cmds.select(ctrlName, r=True)
    cmds.rotate(0, 0, 0)
    cmds.scale(0.75, 0.75, 0.75)

    HToolsLib.freezeAndDeletehistory()

    ##creating FK controller of core joints.
    coreJoints = ('spine01', 'spine02', 'head')
    pos = '_C'
    for coreJointName in coreJoints:
        jointName  = nameSpaceName + coreJointName + pos
        #ofstName  = 'OFST_' + coreJointName + pos
        ctrlName  = 'CTRL_' + coreJointName + pos

        tempName = CreateShapes.ototsuCircle()

        HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')
        #HToolsLib.creatOffset(ofstName, ctrlName, jointName)
        #cmds.parentConstraint(jointName, ofstName)
        cmds.pointConstraint(jointName, ctrlName)
        #cmds.select(ofstName, r=True)
        cmds.select(ctrlName, r=True)
        cmds.delete(cn=True)

        cmds.select(ctrlName, r=True)
        #cmds.rotate(0, 180, 90)
        cmds.rotate(0, 0, 0)
        cmds.scale(0.75, 0.75, 0.75)

        HToolsLib.freezeAndDeletehistory()

def createSode(nameSpaceName, LR):
    orgJointName = 'sode'
    jointName  = nameSpaceName + orgJointName + LR
    ofstName  = 'OFST_' + orgJointName + LR
    ctrlName  = 'CTRL_' + orgJointName + LR

    tempName = CreateShapes.candyLike()
    
    HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')
    HToolsLib.creatOffset(ofstName, ctrlName, jointName)
    cmds.parentConstraint(jointName, ofstName)
    #cmds.pointConstraint(jointName, ctrlName)
    #cmds.select(ofstName, r=True)
    cmds.select(ofstName, r=True)
    cmds.delete(cn=True)

    rotY = 90
    cmds.select(ctrlName, r=True)
    if LR == '_R':
        rotY *= -1
    
    cmds.rotate(0, rotY, 0)
    #cmds.rotate(0, 0, 0)
    cmds.scale(0.5, 0.5, 0.5)

    HToolsLib.freezeAndDeletehistory()


def createLimbs(nameSpaceName = ''):
    posList = ('_L', '_R')
    allLimbs = (('shoulder', 'arm', 'hand', 'wepon'), ('thigh', 'leg', 'foot'))
    
    ##creating FK controllers.
    for pos in posList:
        for limbs in allLimbs:
            dupJoint = nameSpaceName + limbs[0] + pos
            dupList = dupulicateJoint(dupJoint, 'FK', nameSpaceName)
            ##creating controllers
            for limb in dupList:
                jointName = limb
                if pos == posList[0]:
                    ofstName  = 'OFST_' + limb
                    ctrlName  = 'CTRL_' + limb
                else:
                    ofstName  = 'OFST_' + limb
                    ctrlName  = 'CTRL_' + limb
               
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
                cmds.scale(0.3, 0.3, 0.3)

                HToolsLib.freezeAndDeletehistory()

    ##creating IK sets.
    for pos in posList:
        for limbs in allLimbs:
            dupJoint = nameSpaceName + limbs[0] + pos
            dupList = dupulicateJoint(dupJoint, 'IK', 'MODEL:')
            ##creating IK Pole vector controller. 
            jointName = dupList[1]
            #ofstName  = 'OFST_PV_' + dupList[1] + '_C'
            if pos == posList[0]:
                ctrlName  = 'CTRL_PV_' + dupList[1]
            else:
                ctrlName  = 'CTRL_PV_' + dupList[1]
            

            tempName = CreateShapes.pyramid()

            HToolsLib.renameAndColorV2(tempName, ctrlName, 'blue')

            #HToolsLib.creatOffset(ofstName, ctrlName, jointName)

            cmds.parentConstraint(jointName, ctrlName)
            cmds.select(ctrlName, r=True)
            cmds.delete(cn=True)

            cmds.select(ctrlName, r=True)
            cmds.move(0, 0, -0.5, r=True, wd=True)
            cmds.rotate(0, 0, 0)
            cmds.scale(0.1, 0.1, 0.1)

            HToolsLib.freezeAndDeletehistory()

            ##creating IK controller.
            jointName = dupList[2]
            ctrlName  = 'CTRL_' + dupList[2]
            ofstName  = 'OFST_' + dupList[2]


            tempName = CreateShapes.box()

            HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')

            HToolsLib.creatOffset(ofstName, ctrlName, jointName)

            cmds.parentConstraint(jointName, ofstName)
            cmds.select(ofstName, r=True)
            cmds.delete(cn=True)

            cmds.select(ctrlName, r=True)
            cmds.rotate(0, 0, 0)
            cmds.scale(0.25, 0.25, 0.25)

            HToolsLib.freezeAndDeletehistory()

        prefferdAngle = 'IK_arm' + pos + '.preferredAngleY'
        angle = cmds.getAttr(prefferdAngle)
        print(angle)
        if (angle <= 45):
            print('OK')
        else:
            cmds.setAttr(prefferdAngle, 45)
        
        prefferdAngle = 'IK_leg' + pos + '.preferredAngleY'
        angle = cmds.getAttr(prefferdAngle)
        print(angle)
        if (angle >= 45):
            print('OK')
        else:
            cmds.setAttr(prefferdAngle, 45)
    
    CreateShapes.createFKIKSwitch(0.05)   

def controllerParent():
    ##parent a Root ~ Head.
    childController = 'CTRL_tr_C'
    cmds.parent(childController, 'CTRL_Root')
    HToolsLib.setKeyAble(childController, 0, 0, 1)
    lastSpineName = childController

    childController = 'CTRL_hip_C'
    cmds.parent(childController, lastSpineName)
    HToolsLib.setKeyAble(childController, 0, 0, 1)
    lastSpineName = childController

    childController = 'CTRL_spine01_C'
    cmds.parent(childController, lastSpineName)
    HToolsLib.setKeyAble(childController, 0, 0, 1)
    #lastSpineName = 'CTRL_spine01_C'
    lastSpineName = childController

    childController = 'CTRL_spine02_C'
    cmds.parent(childController, lastSpineName)
    HToolsLib.setKeyAble(childController, 0, 0, 1)
    #lastSpineName = 'CTRL_spine02_C'
    lastSpineName = childController

    childController = 'CTRL_head_C'
    cmds.parent(childController, lastSpineName)
    HToolsLib.setKeyAble(childController, 0, 0, 1)
    lastSpineName = childController

    ##parent FK controlelrs.
    posList = ('_L', '_R')
    allLimbs = (('shoulder', 'arm', 'hand'), ('thigh', 'leg', 'foot'))

    for pos in posList:
        for limbs in allLimbs:
            if (limbs == allLimbs[0]):
                lastSpineName = 'CTRL_spine02_C'
            else:
                lastSpineName = 'CTRL_hip_C'
            #print(lastSpineName)
            for limb in limbs:
                #jointName = pos + limb
                if pos == posList[0]:
                    ofstName  = 'OFST_FK_' + limb + '_L'
                    ctrlName  = 'CTRL_FK_' + limb + '_L'
                else:
                    ofstName  = 'OFST_FK_' + limb + '_R'
                    ctrlName  = 'CTRL_FK_' + limb + '_R'

                childController = ofstName

                cmds.parent(childController, lastSpineName)
                HToolsLib.setKeyAble(ctrlName, 0, 0, 1)
                lastSpineName = ctrlName
        
        #IK使用時に非表示なるので、spineの子にする
        ofstName  = 'OFST_FK_weapon' + pos
        ctrlName  = 'CTRL_FK_weapon' + pos
        
        cmds.parent(ofstName, 'CTRL_spine02_C')
        HToolsLib.setKeyAble(ctrlName, 0, 0, 1)
        
    ##parenting FK and IK joints.
    armsGroup = cmds.group(w=True, em=True, n='armsFKIK_JNT_GRP')
    legsGroup = cmds.group(w=True, em=True, n='legsFKIK_JNT_GRP')
    for pos in posList:
        for limbs in allLimbs:
            if (limbs == allLimbs[0]):
                parentName = armsGroup
            else:
                parentName = legsGroup

            childName = 'FK_' + limbs[0] + pos
            cmds.parent(childName, parentName)

            childName = 'IK_' + limbs[0] + pos
            cmds.parent(childName, parentName)
    
    cmds.parent(armsGroup, 'CTRL_spine02_C')
    cmds.parent(legsGroup, 'CTRL_hip_C')

    ##parenting IK contollers.
    armsGroup = cmds.group(w=True, em=True, n='armsFKIK_CTRL_GRP')
    legsGroup = cmds.group(w=True, em=True, n='legsFKIK_CTRL_GRP')
    parentName = 'CTRL_tr_C'
    IKControllers = (('CTRL_PV_IK_arm_L', 'OFST_IK_hand_L', 'CTRL_PV_IK_arm_R', 'OFST_IK_hand_R'),
                     ('CTRL_PV_IK_leg_L', 'OFST_IK_foot_L', 'CTRL_PV_IK_leg_R', 'OFST_IK_foot_R'))

    for controllers in IKControllers:
        for childName in controllers:
            if controllers == IKControllers[0]:
                parentName = armsGroup
            else:
                parentName = legsGroup
            cmds.parent(childName, parentName)
    
    cmds.parent(armsGroup, 'CTRL_tr_C')
    cmds.parent(legsGroup, 'CTRL_tr_C')
            
    cmds.parent('FKIK_SWITCH_GRP', 'CTRL_tr_C')

def parentSode(LR):
    #IK使用時に非表示なるので、spineの子にする
    ofstName  = 'OFST_sode' + LR
    ctrlName  = 'CTRL_sode' + LR
        
    cmds.parent(ofstName, 'CTRL_spine02_C')
    HToolsLib.setKeyAble(ctrlName, 0, 0, 1)

def contollerConst(nameSpace = None):
    constList = ['Root', 'hip_C']
    for const in constList:
        driver = 'CTRL_' + const
        if nameSpace:
            driven = 'MODEL:' + const
        else:
            driven = const
        cmds.parentConstraint(driver, driven, mo=True)

    constList = ['spine01_C', 'spine02_C', 'head_C']

    for const in constList:
        driver = 'CTRL_' + const
        if nameSpace:
            driven = 'MODEL:' + const
        else:
            driven = const
        cmds.orientConstraint(driver, driven, mo=True)

    constList = ['weapon_L', 'weapon_R']
    
    for const in constList:
        driver = 'CTRL_FK_' + const
        if nameSpace:
            driven = 'MODEL:' + const
        else:
            driven = const
        cmds.parentConstraint(driver, driven, mo=True)        

    cmds.parentConstraint('MODEL:hand_L', 'OFST_FK_weapon_L', mo=True)        
    cmds.parentConstraint('MODEL:hand_R', 'OFST_FK_weapon_R', mo=True)        

    ##FKコントローラーとFK用ジョイントのコンストレイント
    #weaponジョイントは大本で操作したいのでここでは外す
    posList = ('_L', '_R')
    allLimbs = (('shoulder', 'arm', 'hand'), ('thigh', 'leg', 'foot'))

    for pos in posList:
        for limbs in allLimbs:
            for limb in limbs:
                if pos == posList[0]:
                    driver = 'CTRL_FK_' + limb + pos
                else:
                    driver = 'CTRL_FK_' + limb  + pos
                driven = 'FK_' + limb + pos

                cmds.parentConstraint(driver, driven, mo=True)

class ConstSode():
    #ちゃんと書けばweponジョイントにも使えるのでは？
    def __init__(self, primJointName, LR):
        #self.nameSpace = ''
        self.LR = LR
        self.jointName = primJointName + LR
        self.driver = 'CTRL_' + primJointName + LR
        self.driven = ''

    def constSode(self):
        nameSpaceName = ''
        if cmds.objExists('MODEL:Root'):
            nameSpaceName = 'MODEL:'
        else:
            print('It has no NameSpace.')

        #primJointName = 'sode'
        #jointName     = primJointName + LR
        #driver = 'CTRL_' + jointName
        if nameSpaceName:
            self.driven = 'MODEL:' + self.jointName
        else:
            self.driven = self.jointName
        cmds.parentConstraint(self.driver, self.driven, mo=True) 
        
        parentJointName = 'MODEL:arm' + self.LR
        childController = 'OFST_sode' + self.LR

        cmds.parentConstraint(parentJointName, childController, mo=True)        
        cmds.parentConstraint('MODEL:hand_R', 'OFST_FK_weapon_R', mo=True)    

def createIK():
    posList = ('_L', '_R')
    allLimbs = (('shoulder', 'arm', 'hand', 'weapon'), ('thigh', 'leg', 'foot'))

    for pos in posList:
        if pos == posList[0]:
            LR = '_L'
        else:
            LR = '_R'

        for limbs in allLimbs:
            ctrlName = 'CTRL_IK_' + limbs[2] + LR
            pvName   = 'CTRL_PV_IK_'  + limbs[1] + LR
            ikName   = 'IKIK_' + limbs[2] + LR
            pVector  = ikName + '.poleVector'
            PVOffset = ikName + '_poleVectorConstraint1.offset'
            sJoint   = 'IK_' + limbs[0] + LR
            eEfector = 'IK_' + limbs[2] + LR

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

def setLimbsFKSwitch():
    ##ネームスペースの処理してない
    posList = ('_L', '_R')
    allLimbs = (('shoulder', 'arm', 'hand'), ('thigh', 'leg', 'foot'))

    for pos in posList:
        if pos == posList[0]:
            LR = '_L'
        else:
            LR = '_R'
        for limbs in allLimbs:
            if limbs == allLimbs[0]:
                switchName = 'handCtrl_SWTC' + LR
            else:
                switchName = 'footCtrl_SWTC' + LR
            reverseName = 'rev' + limbs[2] + 'FK' + LR

            tempNodeName = cmds.shadingNode('reverse', asUtility=True)
            cmds.rename(tempNodeName, reverseName)		
            cmds.connectAttr(switchName + '.translateZ', reverseName + '.inputZ', f=True)

            i=0#めんどうだからこれはなんとかしたい
            for limb in limbs:
                if limbs == allLimbs[1]:
                    if i==3:
                        ##Legというジョイントはないので抜けたい
                        continue
                    else:
                        pass
                else:
                    pass

                #ベイクジョイントとFK操作ジョイントのコンストレイント
                srcJoint = 'FK_' + limb + pos
                dstJoint = 'MODEL:' + limb + pos
                dstJointconst = limb + pos + '_parentConstraint1.'
                cmds.parentConstraint(srcJoint, dstJoint, mo=True)

                #reverseノードのアウトプットをウェイトとvisibilityに繋げる
                constWeight    = dstJointconst + srcJoint + 'W0'
                ctrlVisibility = 'CTRL_FK_' + limb + pos + '.visibility'

                cmds.connectAttr(reverseName + '.outputZ', constWeight, f=True)
                cmds.connectAttr(reverseName + '.outputZ', ctrlVisibility, f=True)

                i+=1

def setLegIKSwitch():
    ##ネームスペースの処理してない
    posList = ('_L', '_R')
    allLimbs = (('shoulder', 'arm', 'hand'), ('thigh', 'leg', 'foot'))

    for pos in posList:
        if pos == posList[0]:
            LR = '_L'
        else:
            LR = '_R'
        for limbs in allLimbs:
            if limbs == allLimbs[0]:
                switchName = 'handCtrl_SWTC' + LR
            else:
                switchName = 'footCtrl_SWTC' + LR
            i=0#めんどうだからこれはなんとかしたい
            for limb in limbs:
                if limbs == allLimbs[1]:
                    if i==3:
                        ##Legというジョイントはないので抜けたい
                        continue
                    else:
                        pass
                else:
                    pass
 
                #ベイクジョイントとFK操作ジョイントのコンストレイント
                srcJoint = 'IK_' + limb + pos
                dstJoint = 'MODEL:' + limb + pos
                dstJointconst = limb + pos + '_parentConstraint1.'
                cmds.parentConstraint(srcJoint, dstJoint, mo=True)

                #reverseノードのアウトプットをウェイトとvisibilityに繋げる
                constWeight    = dstJointconst + srcJoint + 'W1'
                cmds.connectAttr(switchName + '.translateZ', constWeight, f=True)

                i+=1

            ctrlVisibility = 'CTRL_IK_' + limbs[2] + pos + '.visibility'
            cmds.connectAttr(switchName + '.translateZ', ctrlVisibility, f=True)

            ctrlVisibility = 'CTRL_PV_IK_' + limbs[1] + pos + '.visibility'
            cmds.connectAttr(switchName + '.translateZ', ctrlVisibility, f=True)

def createIKGroup():
    LRList = ('_L', '_R')
    IKs = ('hand', 'foot')
    IKGroup = cmds.group(w=True, em=True, n='IK_GRP')
    for LR in LRList:
        for IK in IKs:
            IKName = 'IKIK_' + IK + LR #IKIK_hand_L
            cmds.parent(IKName, IKGroup)
    cmds.parent(IKGroup, 'CTRL_Root')

#HToolsの方に移したい
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


