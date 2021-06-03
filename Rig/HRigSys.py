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

        #self.shapeNumber = 'ototsuCircle'
        self.shapeName   = primJointName   #今のところスフィア作るときに必要な名前
        self.shapeNumber = 2
        self.color       = 'yellow' #colors = {'red':13, 'yellow':22, 'blue':15}

        self.rootParent = ''

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
    
    def createControllers(self, tempName):

        HToolsLib.renameAndColorV2(tempName, self.ctrlName, self.color)
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
        
    def constraintController(self, driver=''):
        #primJoint = 'head_C'
        if not driver:
            driver = self.ctrlName
            driven = self.jointName
        else:
            driven = self.ofstName
        cmds.parentConstraint(driver, driven, mo=True)

#基本的な関数

#単純なFKの作りのものはこれで対応できる気がするので、後で整頓する
#鳴神などの複数しっぽあるタイプはそのままは利用出来ない（鳴神は単純にこれを回数やるだけでいいかも）
def createSimpleController(controllerInfo, isConstraint = False):
    CInfo = controllerInfo

    tempName = CreateShapes.callShape(CInfo.shapeNumber, CInfo.shapeName, CInfo.color) 
    #tempName = CreateShapes.callShape(CreateShapes.shapeDict[CInfo.shapeNumber])
    CInfo.createControllers(tempName)
    CInfo.setRotate()
    CInfo.setScale()
    HToolsLib.setKeyAble(CInfo.ctrlName, CInfo.keyT, CInfo.keyR, CInfo.keyS)

    if isConstraint:
        CInfo.constraintController()

def createFKChain(controllerInfoList):
    CInfoList = controllerInfoList

    for CInfo in CInfoList:
        createSimpleController(CInfo)

    for i in range(1, len(CInfoList)):
        CInfoList[i].parentController(CInfoList[i-1].ctrlName)

    for fk in CInfoList:
        fk.constraintController()

#simpleFKChainはちとこのままだと汎用性が低いっぽいので、一旦上のcreateFKChainを使う
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
            #baseJointName = 'JNT_' + joints + '%02d' %i + '_C'
            baseJointName = joints + '%02d' %i + '_C'
            if cmds.objExists(baseJointName):
                #パターン1
                #primJointNames.append(baseJointName)

                #パターン2（今までの方法を踏襲する場合こちらの方が良いかも
                #primJointNames.append('JNT_' + joints + '%02d' %i)
                primJointNames.append(joints + '%02d' %i)
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

def generateRootController(rootInfo, trInfo):

    rootInfo.ctrlName = 'CTRL_Root'
    rootInfo.ofstName = 'OFST_Root'
    createSimpleController(rootInfo)
    createSimpleController(trInfo)
    trInfo.parentController(rootInfo.ctrlName)

def deleteUnneceJoint(unnecessaryJoint):
    delJoint = unnecessaryJoint
    cmds.delete(delJoint)

    print('Delete ' + delJoint + '.')
    return delJoint

def generateFKLimbs(controllerInfoList):
    #FK用ジョイントの複製とFKコントローラーの生成、FKジョイントとFKコントローラーとのコンストレイントまで一括でやる
    CInfoList = controllerInfoList
    dupList = HToolsLib.dupulicateJoint(CInfoList[0].jointName, 'FK', CInfoList[0].NS)
    
    i = 0
    for i in range(len(CInfoList)):
        CInfoList[i].jointName = dupList[i]
    createFKChain(CInfoList)

def generateIKLimbs(controllerInfoList):
    #IKジョイントの複製
    CInfoList = controllerInfoList
    dupList = HToolsLib.dupulicateJoint(CInfoList[0].jointName, 'IK', CInfoList[0].NS)
    #IK通すためにCInfoリストのジョイントネームを書き換えておく
    CInfoList[0].jointName = dupList[0]

    #コントローラーの生成
    #creating IK Pole vector controller. 
    CInfoList[1].jointName = dupList[1]
    CInfoList[1].ofstName  = 'OFST_PV_' + dupList[1]
    CInfoList[1].ctrlName  = 'CTRL_PV_' + dupList[1]

    createSimpleController(CInfoList[1])

    cmds.select(CInfoList[1].ofstName)
    cmds.move(CInfoList[1].tx, CInfoList[1].ty, CInfoList[1].tz, r=True, wd=True)

    #creating IK controller.
    CInfoList[2].jointName = dupList[2]
    CInfoList[2].ofstName  = 'OFST_' + dupList[2]
    CInfoList[2].ctrlName  = 'CTRL_' + dupList[2]

    createSimpleController(CInfoList[2])

    #コントローラーとIKジョイントのコンストレイント
    ctrlName = CInfoList[2].ctrlName #'CTRL_IK_' + limbs[2] + LR
    pvName   = CInfoList[1].ctrlName #'CTRL_PV_IK_'  + limbs[1] + LR
    ikName   = 'IK' + CInfoList[2].jointName
    pVector  = ikName + '.poleVector'
    PVOffset = ikName + '_poleVectorConstraint1.offset'
    sJoint   = CInfoList[0].jointName
    eEfector = CInfoList[2].jointName

    cmds.ikHandle(n=ikName, sol='ikRPsolver', sj=sJoint, ee=eEfector)

    prePVValuX = cmds.getAttr(pVector + 'X')
    prePVValuY = cmds.getAttr(pVector + 'Y')
    prePVValuZ = cmds.getAttr(pVector + 'Z')
    #IKとボックスコントローラーをコンスト
    cmds.pointConstraint(ctrlName, ikName, mo=True)

    #ポールベクターのコンスト
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
    
    #ボックスコントローラーの回転のコンスト
    srcCTRL = ctrlName
    dstJNT = eEfector
    cmds.orientConstraint(srcCTRL, dstJNT, mo=True)

 
 #どうまとめるか考えるけどとりあえずここで機能確認

def generateSwitch(pos = [4, 4, 0]): 
    test = True
    if test:
        CreateShapes.createFKIKSwitch(0.025)
        cmds.select('FKIK_SWITCH_GRP')
        cmds.move(pos[0], pos[1], pos[2])
        cmds.rotate(90, 0, 0)
        cmds.parent('FKIK_SWITCH_GRP', 'CTRL_tr_C')
        cmds.select(cl=True)

def setLimbsFKSwitch(controllerInfoList, switch):
    CInfoList = controllerInfoList
    switchName = switch + CInfoList[2].pos  #左右が取れればいいのでどこでもいいし何でもいい
    reverseName = 'rev' + CInfoList[2].primJntName + 'FK' + CInfoList[2].pos

    tempNodeName = cmds.shadingNode('reverse', asUtility=True)
    cmds.rename(tempNodeName, reverseName)		
    cmds.connectAttr(switchName + '.translateZ', reverseName + '.inputZ', f=True)

    for limb in CInfoList:
        #ベイクジョイントとFK操作ジョイントのコンストレイント
        srcJoint = limb.jointName #'FK_' + limb + pos
        dstJoint = limb.NS + limb.primJntName + limb.pos #'MODEL:' + limb + pos
        dstJointconst = limb.primJntName + limb.pos + '_parentConstraint1.'
        cmds.parentConstraint(srcJoint, dstJoint, mo=True)

        #reverseノードのアウトプットをウェイトとvisibilityに繋げる
        constWeight    = dstJointconst + srcJoint + 'W0'
        ctrlVisibility = limb.ctrlName + '.visibility'

        cmds.connectAttr(reverseName + '.outputZ', constWeight, f=True)
        cmds.connectAttr(reverseName + '.outputZ', ctrlVisibility, f=True)

def setLimbsIKSwitch(controllerInfoList, switch):
    CInfoList = controllerInfoList
    switchName = switch + CInfoList[2].pos  #左右が取れればいいのでどこでもいいし何でもいい
    for limb in CInfoList:
        #ベイクジョイントとIK操作ジョイントのコンストレイント
        srcJoint = limb.jointName #'IK_' + limb + pos
        dstJoint = limb.NS + limb.primJntName + limb.pos #'MODEL:' + limb + pos
        dstJointconst = limb.primJntName + limb.pos + '_parentConstraint1.'
        cmds.parentConstraint(srcJoint, dstJoint, mo=True)

        #reverseノードのアウトプットをウェイトとvisibilityに繋げる
        constWeight    = dstJointconst + srcJoint + 'W1'
        cmds.connectAttr(switchName + '.translateZ', constWeight, f=True)

    ctrlVisibility = CInfoList[2].ctrlName + '.visibility'
    cmds.connectAttr(switchName + '.translateZ', ctrlVisibility, f=True)

    ctrlVisibility = CInfoList[1].ctrlName + '.visibility'
    cmds.connectAttr(switchName + '.translateZ', ctrlVisibility, f=True)

#↓手と足で分けたいけど、分けるなら関数にするほどでもなくない？って感じなのでどうするかちょっと考える
#とりあえずCUIにはmayaコマンドがインポートされていないので、こっちでバラバラにした
def createFKIKJointGroup(armGrouupName, legGroupName):
    armsGroup = cmds.group(w=True, em=True, n=armGrouupName)
    legsGroup = cmds.group(w=True, em=True, n=legGroupName)
    #↓ここリテラルは最悪
    cmds.parent(armsGroup, 'CTRL_spine02_C')
    cmds.parent(legsGroup, 'CTRL_hip_C')

def createFKIKJointGroupArm(parentController, armGrouupName = 'armsFKIK_JNT_GRP'):
    armsGroup = cmds.group(w=True, em=True, n=armGrouupName)
    cmds.parent(armsGroup, parentController)

def createFKIKJointGroupLeg(parentController, legGroupName = 'legsFKIK_JNT_GRP'):
    legsGroup = cmds.group(w=True, em=True, n=legGroupName)
    cmds.parent(legsGroup, parentController)

def parentFKIKJoint(controllerInfo, groupName):
    parentName = groupName    
    childName = controllerInfo.jointName

    cmds.parent(childName, parentName)
    
def createFKIKControllerGroup(armGrouupName, legGroupName):
    armsGroup = cmds.group(w=True, em=True, n=armGrouupName)
    legsGroup = cmds.group(w=True, em=True, n=legGroupName)
    cmds.parent(armsGroup, 'CTRL_tr_C')
    cmds.parent(legsGroup, 'CTRL_tr_C')

def parentIKController(controllerInfo, groupName):
    parentName = groupName    
    childName = controllerInfo.ofstName

    cmds.parent(childName, parentName)

def createIKGroup():
    #IKの名前も保存出来るようにしたいねぇ
    #腕や足が無かった場合引っかかるのでとりあえずobjExist入れた
    LRList = ('_L', '_R')
    IKs = ('hand', 'foot')
    IKGroup = cmds.group(w=True, em=True, n='IK_GRP')
    for LR in LRList:
        for IK in IKs:
            IKName = 'IKIK_' + IK + LR #IKIK_hand_L
            if cmds.objExists(IKName):
                cmds.parent(IKName, IKGroup)
    cmds.parent(IKGroup, 'CTRL_Root')


def main():
    joints = ['shoulder', 'arm', 'hand']
    #joints = 'tail'
    simpleFKChain(joints)


if __name__ == '__main__':
    main()