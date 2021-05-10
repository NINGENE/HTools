# __*__ coding: utf-8 __*__

import copy
from maya import cmds, mel
from HTools.lib import HToolsLib, CreateShapes
reload(HToolsLib)
reload(CreateShapes)

'''
開始日 2021/1/20
あとで纏めるやつまとめ
'''
#ベースとなるクラスを作り直そう
#外から変えたいやつを構造体的に纏めたクラスを作るか
#└引数が増えるのが嫌なのでクラスに纏める的発想
#最終的にCUIの方ではこのクラスを書き換えるのをメインとする感じで

#↓これをまるっと引数で渡せばいいようにしたい
#継承とか上手くいかなかったのでいったん下のBaseControllerに機能を譲る(21/5/10現在)
class HTransfrom(object):
    def __init__(self):
        self.name = 'test_joint_name'
        #Transform
        self.tx = 0
        self.ty = 0
        self.tz = 0
        #Rotate
        self.rx = 180
        self.ry = 0
        self.rz = 90
        #Scale
        self.sx = 1
        self.sy = 1
        self.sz = 1
    
    def testFunc(self, place = ''):
        if place:
            print('test called from ' + place)
        else:
            print('test in HRig_test')

class BaseController():
    def __init__(self, ownNameSpaceName, primJointName, pos='_C', nodeType=''):
        self.primJntName   = primJointName
        self.pos           = pos
        self.NType         = nodeType
        self.ctrlName      = 'CTRL_' + self.primJntName + self.pos
        self.ofstName      = 'OFST_' + self.primJntName + self.pos
        self.NS            = ownNameSpaceName
        self.jointName     = self.NS + self.NType + self.primJntName + self.pos

        #Transform
        self.tx = 0
        self.ty = 0
        self.tz = 0
        #Rotate
        self.rx = 180
        self.ry = 0
        self.rz = 90
        #Scale
        self.sx = 1
        self.sy = 1
        self.sz = 1

        #Key able
        self.keyT = 1 
        self.keyR = 0
        self.keyS = 1

        self.shapeNumber = 2

    def resetJointName(self, newJointName):
        self.primJntName   = newJointName
        self.ctrlName      = 'CTRL_' + self.primJntName + self.pos
        self.ofstName      = 'OFST_' + self.primJntName + self.pos
        self.jointName     = self.NS + self.NType + self.primJntName + self.pos        

    def setRotate(self):
        cmds.select(self.ctrlName, r=True)
        cmds.rotate(self.rx, self.ry, self.rz)
        HToolsLib.freezeAndDeletehistory()
        cmds.select(cl=True)

    def setScale(self):
        cmds.select(self.ctrlName, r=True)
        cmds.scale(self.sx, self.sy, self.sz)
        HToolsLib.freezeAndDeletehistory()
        cmds.select(cl=True)

class ControllerCreator(BaseController):
    
    def createControllers(self, tempName, color='yellow'):

        HToolsLib.renameAndColorV2(tempName, self.ctrlName, color)
        HToolsLib.creatOffset(self.ofstName, self.ctrlName, self.jointName)

        dstName = self.ofstName

        if cmds.objExists(self.jointName):
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

def createSimpleController(controllerInfo):
    CInfo = controllerInfo

    tempName = CreateShapes.callShape(CInfo.shapeNumber)
    CInfo.createControllers(tempName)
    CInfo.setRotate()
    CInfo.setScale()
    HToolsLib.setKeyAble(CInfo.ctrlName, CInfo.keyT, CInfo.keyR, CInfo.keyS)

#基本的な関数
def simpleFKChain(joints, controllerInfo):
    CInfo = controllerInfo
    primJointNames = []
    if type(joints) == list:
        #腕、足のように名前が決まっているけど、連番じゃないタイプの名前
        #リストがすでにあるのでとりあえずそのまま使用
        primJointNames = joints
    else:
        #tail_01のように数がまちまちだけど連番の場合
        #リストを作る
        i = 1
        while True:
            baseJointName = 'JNT_' + joints + '%02d' %i + '_C'
            if cmds.objExists(baseJointName):
                #パターン1
                #primJointNames.append(baseJointName)

                #パターン2（今までの方法を踏襲する場合こちらの方が良いかも
                primJointNames.append('JNT_' + joints + '%02d' %i)
                i += 1
            else:
                break

    uFKChains = []
    #nameSpaceName = ''  #仮
    for joint in primJointNames:
        CInfo.resetJointName(joint)
        uFKChain = copy.deepcopy(CInfo)
        createSimpleController(uFKChain)
        
        uFKChains.append(uFKChain)
    

    for i in range(1, len(uFKChains)):
        uFKChains[i].parentController(uFKChains[i-1].ctrlName)

    for fk in uFKChains:
        fk.constraintController()

    #if parentObject:
    #    uFKChains[0].parentController(parentObject)


#いずれはライブラリに入れたい
def checkNamespace():
    if cmds.objExists('MODEL:root') or cmds.objExists('MODEL:Root'):
        nameSpaceName = 'MODEL:'
        print('NameSpace is ' + str(nameSpaceName))
    else:
        print('It has no NameSpace.')

    return nameSpaceName

#単純なFKの作りのものはこれで対応できる気がするので、後で整頓する
#鳴神などの複数しっぽあるタイプはそのままは利用出来ない（鳴神は単純にこれを回数やるだけでいいかも）
#simpleFKControllerとかにするか
#サイズの変更も出来るようにする
#コントローラーの形状も（これはもっと親のクラスが良いかも
def main():
    joints = ['shoulder', 'arm', 'hand']
    #joints = 'tail'
    simpleFKChain(joints)

def tailUnitCreate(primJointName, parentObject=''):
    uTails = []

    i = 1
    while True:
        uTail = ControllerCreator(nameSpaceName, primJointName + '%02d' %i)
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

    if parentObject:
        uTails[0].parentController(parentObject)

    #return uTails[0]
    #neckの場合、最後が欲しい場合もある
    return uTails





# ↓↓↓ここからは要精査（単純に削除していないだけ)
class LimbUnitBase():
    def __init__(self, limbs, pos):
        self.limbs = limbs
        self.pos   = pos

        self.hasClavicle  = False
        #self.hasSecondary = False

        self.rotValue = [0, 0, 90]
        self.sclValue = [1, 1, 1]

        self.dupList = ''

        self.NS = '' #dup joint doesn't need the Name Space.
        self.nullPos = '' #dup joint doesn't need the pos in CreateFK().
    
    def sortOutDups(self, FKIK):
        baseDupJoint = nameSpaceName + self.limbs[0] + self.pos
        self.dupList = HToolsLib.dupulicateJoint(baseDupJoint, FKIK, nameSpaceName)

        #weponを含むセカンダリジョイントをデュプリケイトジョイントから削除
        removeJoints = []
        for dJoint in self.dupList:
            checkName = dJoint.split('_')
            if not checkName[1] in self.limbs:
                removeJoints.append(dJoint)
                if cmds.objExists(dJoint):
                    cmds.delete(dJoint)
        for rJoint in removeJoints:
            self.dupList.remove(rJoint)

class LimbUnitFK(LimbUnitBase):
    
    def CreateFK(self, size=(1, 1, 1)):
        FKLimbs = []

        #weponを含むセカンダリジョイントをデュプリケイトジョイントから削除
        self.sortOutDups(FKIK='FK')

        #残ったジョイントのコントローラーを作成
        for dJoint in self.dupList:
            uFK = ControllerCreator(self.NS, dJoint, self.nullPos)
        
            if dJoint == ('FK_clavicle' + self.pos):
                tempName = CreateShapes.candyLike()
                uFK.createControllers(tempName, 'yellow')
                
                if self.pos == '_L':
                    uFK.setRotate((0, 90, 90))
                else:
                    uFK.setRotate((0, -90, 90))
                
                self.hasClavicle = True

            else:
                tempName = CreateShapes.linerCircle()
                uFK.createControllers(tempName, 'blue')
                if dJoint == ('FK_toe' + self.pos):
                    uFK.setRotate((90, 0, 0))
                else:
                    uFK.setRotate((0, 0, 90))
            
            uFK.setScale(size)
            HToolsLib.setKeyAble(uFK.ctrlName, 1, 0, 1)
            FKLimbs.append(uFK)

        lastChild = ''
        i = 0
        #print(lastSpineName)
        for limb in FKLimbs:
            if i == 0:
                pass    
            else:
                parent  = lastChild
                child   = limb.ofstName
            
                cmds.parent(child, parent)
            
            driver = limb.ctrlName
            driven = limb.jointName
            cmds.parentConstraint(driver, driven, mo=True)
            
            lastChild = limb.ctrlName

            i+=1
    
    def createWeponController(self, size=(1, 1, 1)):
        #IK使用時に非表示なるので、spineの子にする（墨兵はヒップ
        uWeapon = ControllerCreator(nameSpaceName, 'weapon', self.pos)
        parentNode = 'CTRL_spine02_C'

        if cmds.objExists(uWeapon.jointName):
            tempName = CreateShapes.sphere(uWeapon.ctrlName, 13)
            uWeapon.createControllers(tempName, 'red')
            uWeapon.setRotate((0, 0, 90))
            uWeapon.setScale(size)

            uWeapon.parentController(parentNode)

            uWeapon.constraintController()

            HToolsLib.setKeyAble(uWeapon.ctrlName, 0, 0, 1)
            #weponの親をhandジョイントにする
            cmds.parentConstraint('MODEL:hand' + self.pos, uWeapon.ofstName, mo=True)

    def createSecondaryController(self, size=(1,1,1)):
        #IK使用時に非表示なるので、spineの子にする（墨兵はヒップ
        uSecond = ControllerCreator(nameSpaceName, 'chain', self.pos)
        parentNode = 'CTRL_spine02_C'

        if cmds.objExists(uSecond.jointName):        
            tempName = CreateShapes.candyLike()
            uSecond.createControllers(tempName, 'blue')
            if self.pos == '_L':
                uSecond.setRotate((0, 0, 180))
            else:
                uSecond.setRotate((0, 0, 180))

            uSecond.parentController(parentNode)

            uSecond.constraintController()

            HToolsLib.setKeyAble(uSecond.ctrlName, 0, 0, 1)
            #weponの親をhandジョイントにする
            cmds.parentConstraint('MODEL:arm' + self.pos, uSecond.ofstName, mo=True)

class LimbUnitIK(LimbUnitBase):

    def createIK(self, isPositive=False, size=(1,1,1)):
        #def createIKLimbs(self, isPositive):
        vecZPos = 4
        vecXRot = 90
        if isPositive:
            pass
        else:
            vecZPos *= -1
            vecXRot *= -1

        #IKLimbs = []

        self.sortOutDups(FKIK='IK')

        ##creating IK Pole vector controller. 
        jointName = self.dupList[1]
        ctrlName  = 'CTRL_PV_' + self.dupList[1]
        
        tempName = CreateShapes.pyramid()

        HToolsLib.renameAndColorV2(tempName, ctrlName, 'blue')

        cmds.parentConstraint(jointName, ctrlName)
        cmds.select(ctrlName, r=True)
        cmds.delete(cn=True)

        cmds.select(ctrlName, r=True)
        cmds.move(0, 0, vecZPos, r=True, wd=True)
        cmds.rotate(vecXRot, 0, 0)
        cmds.scale(size[0], size[1], size[2])

        HToolsLib.freezeAndDeletehistory()

        ##creating IK controller.
        jointName = self.dupList[2]
        ctrlName  = 'CTRL_' + self.dupList[2]
        ofstName  = 'OFST_' + self.dupList[2]

        tempName = CreateShapes.box()

        HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')
        HToolsLib.creatOffset(ofstName, ctrlName, jointName)

        dstName = ofstName
        cmds.parentConstraint(jointName, dstName)
        cmds.select(dstName, r=True)
        cmds.delete(cn=True)

        cmds.select(ctrlName, r=True)
        cmds.rotate(0, 0, 0)
        cmds.scale(size[0], size[1], size[2])

        HToolsLib.freezeAndDeletehistory()

        prefferdAngle = self.dupList[1] + '.preferredAngleY'
        angle = cmds.getAttr(prefferdAngle)
        #print(angle)
        if (angle <= 45):
            print('angle is OK')
        else:
            cmds.setAttr(prefferdAngle, 45)

        #def createIK(self):
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

        HToolsLib.setKeyAble('CTRL_PV_' + self.dupList[1], 0, 1, 1)
        HToolsLib.setKeyAble('CTRL_' + self.dupList[2], 0, 0, 1)

    def createReverseFoot(self):
        ikName   = 'IK_Toe' + self.pos
        sJoint   = 'IK_' + self.limbs[2] + self.pos
        eEfector = 'IK_' + self.limbs[3] + self.pos

        cmds.ikHandle(n=ikName, sol='ikSCsolver', sj=sJoint, ee=eEfector)

        uToe = ControllerCreator(self.NS, 'IK_toe', self.pos)
        tempName = CreateShapes.linerCircle()
        uToe.createControllers(tempName, 'red')

        child  = ikName
        parent = uToe.ctrlName
        cmds.parent(child, parent)

        #box作る
        uIKFootForRev = ControllerCreator(self.NS, 'IK_foot', self.pos)
        tempName = CreateShapes.box()
        #IKfootコントローラーをリネーム
        revOffset = 'OFST_IK_footForRev'+self.pos
        revController = 'CTRL_IK_footForRev'+self.pos
        cmds.rename('OFST_IK_foot'+self.pos, revOffset)
        cmds.rename('CTRL_IK_foot'+self.pos, revController)

        cmds.setAttr(revController + '.visibility', 0)

        #boxをIKfootコントローラーとして作成
        uIKFootForRev.createControllers(tempName, 'yellow')


        uToeRot = ControllerCreator(self.NS, 'IK_toe', self.pos)
        uToeRot.ctrlName = 'CTRL_ToeRot'+ self.pos
        uToeRot.ofstName = 'OFST_ToeRot'+ self.pos
        tempName = CreateShapes.box()
        uToeRot.createControllers(tempName, 'yellow')
        driver = uToeRot.ctrlName
        driven = uToeRot.jointName
        cmds.orientConstraint(driver, driven, mo=True)

        #toe,toeRotコントローラーとIKfootコントローラーを子にする
        child  = uToe.ofstName
        parent = uIKFootForRev.ctrlName
        cmds.parent(child, parent)

        child  = revOffset
        parent = uToe.ctrlName
        cmds.parent(child, parent)

        child  = uToeRot.ofstName
        parent = uIKFootForRev.ctrlName
        cmds.parent(child, parent)

        cmds.connectAttr(uToeRot.ctrlName + '.rotateX', uToe.ctrlName + '.rotateX', f=True)
        cmds.connectAttr(uToeRot.ctrlName + '.rotateZ', uToe.ctrlName + '.rotateZ', f=True)

        HToolsLib.setKeyAbleR(uToe.ctrlName, 1, 0, 1)

        HToolsLib.setKeyAble(uIKFootForRev.ctrlName, 0, 0, 1)
        HToolsLib.setKeyAble(uToe.ctrlName, 1, 0, 1)
        HToolsLib.setKeyAble(uToeRot.ctrlName, 1, 0, 1)
        
class FKIKUnit():#名前が良くない
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

        for i in range(len(self.limbs)):#clavicleをコンストするやつをどこかで作る
            #ベイクジョイントとFK操作ジョイントのコンストレイント
            primName = self.limbs[i] + self.pos
            srcJoint = 'FK_' + primName
            dstJoint = nameSpaceName + primName
            dstJointconst = primName + '_parentConstraint1.'
            cmds.parentConstraint(srcJoint, dstJoint, mo=True)

            #reverseノードのアウトプットをウェイトとvisibilityに繋げる
            constWeight    = dstJointconst + srcJoint + 'W0'
            if not dstJoint == ('MODEL:clavicle' + self.pos):#これも要らない
                ctrlVisibility = 'CTRL_' + srcJoint + '.visibility'
                cmds.connectAttr(reverseName + '.outputZ', ctrlVisibility, f=True)             

            cmds.connectAttr(reverseName + '.outputZ', constWeight, f=True)



    def setLimbsIKSwitch(self):
        #clavicleがあった場合、リストを1つ後ろにずらす
        listShiftNum = 0
        rangeNum = 3
        if self.isUp:
            if cmds.objExists(('MODEL:clavicle'+self.pos)):
                listShiftNum = 1
        if not self.isUp:
            rangeNum = len(self.limbs)

                
        for i in range(rangeNum): #weponジョイントは操作したくない←weponジョイントは無くしたのでアップデートが必要
            #ベイクジョイントとIK操作ジョイントのコンストレイント
            primName = self.limbs[i+listShiftNum] + self.pos
            srcJoint = 'IK_' + primName
            dstJoint = nameSpaceName + primName
            dstJointconst = primName + '_parentConstraint1.'
            if cmds.objExists(srcJoint):
                cmds.parentConstraint(srcJoint, dstJoint, mo=True)
                #reverseノードのアウトプットをウェイトとvisibilityに繋げる
                constWeight = dstJointconst + srcJoint + 'W1'
                cmds.connectAttr(self.switchName + '.translateZ', constWeight, f=True)



        ctrlVisibility = 'CTRL_IK_' + self.limbs[2+listShiftNum] + self.pos + '.visibility'
        cmds.connectAttr(self.switchName + '.translateZ', ctrlVisibility, f=True)

        ctrlVisibility = 'CTRL_PV_IK_' + self.limbs[1+listShiftNum] + self.pos + '.visibility'
        cmds.connectAttr(self.switchName + '.translateZ', ctrlVisibility, f=True)

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
    dupList = HToolsLib.dupulicateJoint(baseDupJoint, 'IK', nameSpaceName)
    #コピーしたジョイントをリネーム
    IKBaseJoints = []
    for tempJoint in dupList:
        #print(tempJoint)
        cmds.rename(tempJoint, 'Base_' + tempJoint)
        IKBaseJoints.append('Base_' + tempJoint)
    print(IKBaseJoints)

    #4本をまとめて動かすジョイントの作成（名前考え中）
    dupList = HToolsLib.dupulicateJoint(baseDupJoint, 'IK', nameSpaceName)
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
    dupList = HToolsLib.dupulicateJoint(baseDupJoint, 'IK', nameSpaceName)
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
    dupList = HToolsLib.dupulicateJoint(baseDupJoint, 'IK', nameSpaceName)
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
    


if __name__ == '__main__':
    main()