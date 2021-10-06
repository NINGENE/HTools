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



shapeDict = {'linerCircle':1, 'ototsuCircle':2, 'cross':3,
             'arrowCross':4, 'box':5, 'pyramid':6, 
             'gear':7, 'sphere':8, 'candyLike':9}

class Shapes():
    def __init__(self):
        self.liner_circle  = shapeDict['linerCircle']
        self.ototsu_circle = shapeDict['ototsuCircle']
        self.cross         = shapeDict['cross']
        self.arrow_cross   = shapeDict['arrowCross']
        self.box           = shapeDict['box']
        self.pyramid       = shapeDict['pyramid']
        self.gear          = shapeDict['gear']
        self.sphere        = shapeDict['sphere']
        self.candylike     = shapeDict['candyLike']

class Colors():
    def __init__(self):
        self.red    = 'red'
        self.yellow = 'yellow'
        self.blue   = 'blue'
#↓これをまるっと引数で渡せばいいようにしたい
#継承とか上手くいかなかったのでいったん下のBaseControllerに機能を譲る(21/5/10現在)
#上の話はなんか違う気がしてきた

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

    tempName = CreateShapes.callShape(CInfo.shapeNumber, CInfo.shapeName, CInfo.color, CInfo.pos) 
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

    #複製したIKジョイントからローカル回転用のハンドジョイントの複製
    prim_local_rot_joint_name = 'IK_' + CInfoList[2].primJntName + '_local'
    local_rot_joint = cmds.duplicate(dupList[2])  #順当に行けば2番はHandだと思うけどちょっと怖い
    #ウェポンジョイント等は邪魔なので子をリストアップして削除
    del_joints = cmds.listRelatives(local_rot_joint[0], fullPath=True)
    if del_joints:
        for joint in del_joints:
            cmds.delete(joint)
            print('Deleted ' + str(del_joints))
        
    local_rot_joint = cmds.rename(local_rot_joint[0], prim_local_rot_joint_name + CInfoList[2].pos)

    #コントローラーの生成
    #creating IK Pole vector controller. 
    CInfoList[1].jointName = dupList[1]
    CInfoList[1].ofstName  = 'OFST_PV_' + dupList[1]
    CInfoList[1].ctrlName  = 'CTRL_PV_' + dupList[1]

    createSimpleController(CInfoList[1])

    #なんかここクラス使ってるのに移動のさせ方何とかならんのか？
    cmds.select(CInfoList[1].ofstName)
    cmds.move(CInfoList[1].tx, CInfoList[1].ty, CInfoList[1].tz, r=True, wd=True)

    #creating IK controller.
    CInfoList[2].jointName = dupList[2]
    CInfoList[2].ofstName  = 'OFST_' + dupList[2]
    CInfoList[2].ctrlName  = 'CTRL_' + dupList[2]

    createSimpleController(CInfoList[2])

    #creating IK local rotation controller.
    ctrl_local_controller = ControllerCreator(CInfoList[2].NS, prim_local_rot_joint_name, CInfoList[2].pos)

    ctrl_local_controller.sx = CInfoList[2].sx * 1.25
    ctrl_local_controller.sy = CInfoList[2].sy * 1.25
    ctrl_local_controller.sz = CInfoList[2].sz * 1.25
    ctrl_local_controller.shapeNumber = shapeDict['linerCircle']

    ctrl_local_controller.jointName = prim_local_rot_joint_name + CInfoList[2].pos
    createSimpleController(ctrl_local_controller)
    ctrl_local_controller.parentController(CInfoList[1].jointName)

    #コントローラーとIKジョイントのコンストレイント
    ctrlName = CInfoList[2].ctrlName #'CTRL_IK_' + limbs[2] + LR
    pvName   = CInfoList[1].ctrlName #'CTRL_PV_IK_'  + limbs[1] + LR
    local_Ctrl_Name = ctrl_local_controller.ctrlName
    ikName   = 'IK' + CInfoList[2].jointName
    pVector  = ikName + '.poleVector'
    PVOffset = ikName + '_poleVectorConstraint1.offset'
    sJoint   = CInfoList[0].jointName
    eEfector = CInfoList[2].jointName

    #コントローラーにフォローハンド用のアトリビュートを追加
    cmds.addAttr(ctrlName, keyable = True, shortName='pw', longName='LocalSpace', defaultValue=1.0, minValue=0.0, maxValue=1.0 )

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

    #ローカルコントローラーの回転のコンスト
    srcCTRL = local_Ctrl_Name
    dstJNT  = local_rot_joint
    cmds.orientConstraint(srcCTRL, dstJNT, mo=True)

 
 #どうまとめるか考えるけどとりあえずここで機能確認

class DogLegIK():
    def __init__(self, name_space, prim_dup_joints):
        self.name_space_name = name_space
        self.prim_limbs = prim_dup_joints
        self.prim_joint = prim_dup_joints[0]    #コピーするジョイントのルートジョイント　基本hipが入っている
    
    def make_dog_leg_rig(self,
        hip_ctrl_size=[1.5, 1, 1],
        prim_joint_name = 'hip',
        ik_box_size = [1, 1, 1],
        pv_size = [0.2, 0.2, 0.2],
        pv_pos = 2,
        position_list = ['_L', '_R']):

        print(self.prim_joint)
        for pos in position_list:
            name_space_name = self.name_space_name
            base_dup_joint  = name_space_name + self.prim_joint + pos
            kinema          = 'IK'

            #1. アッタチするための階層が綺麗なジョイントの作成（ベースジョイント）
            dupList = HToolsLib.dupulicateJoint(base_dup_joint, kinema, name_space_name)
            #コピーしたジョイントをリネーム
            IKBaseJoints = []
            for tempJoint in dupList:
                cmds.rename(tempJoint, 'Base_' + tempJoint)
                IKBaseJoints.append('Base_' + tempJoint)

            #2. 4本をまとめて動かすジョイントの作成（名前考え中）
            dupList = HToolsLib.dupulicateJoint(base_dup_joint, kinema, name_space_name)
            #コピーしたジョイントをリネーム
            topHieralkyJoints = []
            for tempJoint in dupList:
                cmds.rename(tempJoint, 'Top_' + tempJoint)
                topHieralkyJoints.append('Top_' + tempJoint)

            #3. 上の奴（名前考え中）にIK通す
            topIK = cmds.ikHandle(n='top_IK_foot' + pos, sol='ikRPsolver', sj=topHieralkyJoints[0], ee=topHieralkyJoints[3])	#example of IK name 'aim_front_IK_L'
            cmds.setAttr(topIK[0] + '.visibility', 0)

            #4. 太もも調整用のジョイントを作成（上下でセパレートしたやつ）
            #4-1. 上側
            dupList = HToolsLib.dupulicateJoint(base_dup_joint, kinema, name_space_name)
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

            #4-2. 下側
            dupList = HToolsLib.dupulicateJoint(base_dup_joint, kinema, name_space_name)
            downJoints = []
            for tempJoint in dupList:
                cmds.rename(tempJoint, 'Down_' + tempJoint)
                downJoints.append('Down_' + tempJoint)
            
            cmds.parent(downJoints[1], w=True)
            cmds.delete(downJoints[0])
            
            #5. 上下でセパレートしたやつジョイントにIKを通す
            downIK = cmds.ikHandle(n='down_IK_foot' + pos, sol='ikRPsolver', sj=downJoints[1], ee=downJoints[3])	#example of IK name 'aim_front_IK_L'
            cmds.setAttr(downIK[0] + '.visibility', 0)

            #6. upとdownをコンストレイント
            cmds.pointConstraint(upJoints[1], downJoints[1])
            
            #7. 名前考え中と上下でセパレートしやつをコネクト（子になるのは上下でセパレートしたやつ）
            #太もも用のコントローラーの作成
            ###ここはあとで外に出す？CUIに記載されている部分を一先ず動かすためにここに書いている
            c_hip = ControllerCreator(name_space_name, prim_joint_name, pos)
            #c_hip = HRigSys.ControllerCreator(nameSpaceName, prim_joint_name, pos)
            c_hip.ctrlName = 'CTRL_IK_' + prim_joint_name + pos
            c_hip.ofstName = 'OFST_IK_' + prim_joint_name + pos
            c_hip.sx = hip_ctrl_size[0]
            c_hip.sy = hip_ctrl_size[1]
            c_hip.sz = hip_ctrl_size[2]
            c_hip.shapeNumber = 5   #shapeDict['box']

            ###ここまでがCUIで書いている部分、こっちにそのまま残してもいいかも

            createSimpleController(c_hip)

            cmds.parentConstraint(topHieralkyJoints[0], c_hip.ofstName)
            cmds.parentConstraint(c_hip.ctrlName, upJoints[0])

            #8. ベースジョイントを上下セパの子にする
            cmds.parentConstraint(upJoints[0], IKBaseJoints[0])
            numOfJoint = len(IKBaseJoints)
            i = 1
            while i < numOfJoint:
                cmds.parentConstraint(downJoints[i], IKBaseJoints[i])
                i+=1

            #9. footのIKコントローラー作成（IK自体は仕込まない）
            #普通のlegと一緒にしたいなぁ
            ###ここはCUI部分
            #c_foot = HRigSys.ControllerCreator(nameSpaceName, 'IK_foot', pos)
            c_foot = ControllerCreator(name_space_name, 'IK_foot', pos)
            c_foot.jointName = 'Base_IK_foot' + pos
            c_foot.sx = ik_box_size[0]
            c_foot.sy = ik_box_size[1]
            c_foot.sz = ik_box_size[2]
            c_foot.keyT = 0
            c_foot.shapeNumber = 5   #shapeDict['box']
            ###CUI部分ここまで
            createSimpleController(c_foot)

            #10. ポールベクター作成
            vecZPos = pv_pos
            if pos == '_L':
                vecXRot = 90
            else:
                vecXRot = -90    
            ###ここが必要か良く分からない
            isPositive = True
            if isPositive:
                pass
            else:
                vecZPos *= -1
                vecXRot *= -1
            ###ここまで
            
            ##creating IK Pole vector controller. 
            c_pv = ControllerCreator(name_space_name, IKBaseJoints[1], pos)
            c_pv.jointName = IKBaseJoints[1]
            c_pv.ctrlName = 'CTRL_leg_TW' + pos
            c_pv.ofstName = 'OFST_leg_TW' + pos
            c_pv.tx = 0
            c_pv.ty = 0
            c_pv.tz = vecZPos
            c_pv.rx = vecXRot
            c_pv.ry = 0
            c_pv.rz = 0
            c_pv.sx = pv_size[0]
            c_pv.sy = pv_size[1]
            c_pv.sz = pv_size[2]
            c_pv.keyT = 0
            c_pv.keyR = 1
            c_pv.shapeNumber = 6 #shapeDict['pyramid']
            
            createSimpleController(c_pv)
            #ここもなんかここクラス使ってるのに移動のさせ方何とかならんのか？
            cmds.select(c_pv.ofstName)
            cmds.move(c_pv.tx, c_pv.ty, c_pv.tz, r=True, wd=True)


            self.parentDogLeg(pos)

            self.constDogLegIK(pos)


    def parentDogLeg(self, pos):
        ikCtrlName = 'footIK_CTRL_GRP'
        if not cmds.objExists(ikCtrlName):
            cmds.group(w=True, em=True, n=ikCtrlName)

        cmds.parent('OFST_IK_foot' + pos, ikCtrlName)
        cmds.parent('OFST_leg_TW' + pos, ikCtrlName)

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


    def constDogLegIK(self, pos):
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
        cmds.setAttr(tweakTwist + '.input2X', 25)#もともと0.25だけど単位がメーターなので100倍している


    def setDogLegIKSwitch(self, pos):
        switchName = 'footCtrl_SWTC' + pos

        for joint in self.prim_limbs:
            #ベイクジョイントとIK操作ジョイントのコンストレイント
            srcJoint = 'Base_IK_' + joint + pos
            dstJoint = 'MODEL:' + joint + pos
            cmds.parentConstraint(srcJoint, dstJoint, mo=True)

            #スウィッチの数値をウェイトと繋げる
            constWeight = joint + pos + '_parentConstraint1.' + 'Base_IK_' + joint + pos + 'W1'

            cmds.connectAttr(switchName + '.translateZ', constWeight, f=True)

        #スイッチの数値とコントローラーの表示に繋げる
        ctrlVisibilities = ('CTRL_IK_hip' + pos, 'CTRL_IK_foot' + pos, 'CTRL_leg_TW' + pos)
        for vis in ctrlVisibilities:
            cmds.connectAttr(switchName + '.translateZ', vis + '.visibility', f=True)
        
    
    def array_nodes(self):
        legsGroup = 'footIK_CTRL_GRP'
        cmds.parent(legsGroup, 'CTRL_tr_C')

        cmds.parent('legsFKIK_JNT_GRP', 'CTRL_hip_C')
        
        cmds.parent('DogLegIK_GRP', 'CTRL_tr_C')

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
    #switchName = switch + CInfoList[2].pos  #左右が取れればいいのでどこでもいいし何でもいい
    switchName = switch #猫又のFL問題が在ったので、ここでLR取るんじゃなくて外でスイッチ名指定しちゃう
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
    #switchName = switch + CInfoList[2].pos  #左右が取れればいいのでどこでもいいし何でもいい
    switchName = switch #猫又のFL問題が在ったので、ここでLR取るんじゃなくて外でスイッチ名指定しちゃう
    condition_name = 'isFollow' + CInfoList[2].primJntName + 'FK' + CInfoList[2].pos

    #フォローハンドのオンオフ
    temp_node_name = cmds.shadingNode('condition', asUtility=True)
    cmds.rename(temp_node_name, condition_name)
    cmds.connectAttr(switchName + '.translateZ', condition_name + '.colorIfFalse.colorIfFalseR', f=True)
    cmds.connectAttr(switchName + '.translateZ', condition_name + '.secondTerm', f=True)
    cmds.setAttr(condition_name + '.firstTerm', 1)

    for limb in CInfoList:
        #ベイクジョイントとIK操作ジョイントのコンストレイント
        srcJoint = limb.jointName #'IK_' + limb + pos
        dstJoint = limb.NS + limb.primJntName + limb.pos #'MODEL:' + limb + pos
        dstJointconst = limb.primJntName + limb.pos + '_parentConstraint1.'
        cmds.parentConstraint(srcJoint, dstJoint, mo=True)

        #reverseノードのアウトプットをウェイトとvisibilityに繋げる
        constWeight    = dstJointconst + srcJoint + 'W1'
        cmds.connectAttr(switchName + '.translateZ', constWeight, f=True)
    
    #handoだけもう一回ローカルジョイントとつなげる
    limb = CInfoList[2]
    srcJoint = 'IK_' +  limb.primJntName + '_local' + limb.pos #IK_hand_local_R
    dstJoint = limb.NS + limb.primJntName + limb.pos #'MODEL:' + limb + pos 
    dstJointconst = limb.primJntName + limb.pos + '_parentConstraint1.'
    cmds.parentConstraint(srcJoint, dstJoint, mo=True)

    #hand用のrevを作る
    follow_hand_reverse = 'fh_rev' + CInfoList[2].primJntName + CInfoList[2].pos

    tempNodeName = cmds.shadingNode('reverse', asUtility=True)
    cmds.rename(tempNodeName, follow_hand_reverse)

    #handのウェイトを切り替えるやつを繋ぎなおす
    cmds.connectAttr(CInfoList[2].ctrlName + '.LocalSpace', condition_name + '.colorIfTrueR', f=True)

    constWeight = dstJointconst + srcJoint + 'W2'   #ローカルハンド側のウェイト
    cmds.connectAttr(condition_name + '.outColorR', constWeight, f=True)

    constWeight = dstJointconst + 'IK_' + limb.primJntName + limb.pos + 'W1'   #IKコントローラー側のウェイト
    cmds.connectAttr(condition_name + '.outColorR', follow_hand_reverse + '.inputX', f=True)
    cmds.connectAttr(follow_hand_reverse + '.outputX', constWeight, f=True)
    #ローカルハンドのコンストレイントのつなぎここまで

    ctrlVisibility = CInfoList[2].ctrlName + '.visibility'
    cmds.connectAttr(switchName + '.translateZ', ctrlVisibility, f=True)

    ctrlVisibility = CInfoList[1].ctrlName + '.visibility'
    cmds.connectAttr(switchName + '.translateZ', ctrlVisibility, f=True)

    #ローカルハンドの表示の設定
    #FKIKスイッチ判定用のコンディションを作る
    condition_name = 'localHandVis' + CInfoList[2].primJntName + CInfoList[2].pos
    temp_node_name = cmds.shadingNode('condition', asUtility=True)
    cmds.rename(temp_node_name, condition_name)

    #コンディションへの接続
    cmds.connectAttr(CInfoList[2].ctrlName + '.LocalSpace', condition_name + '.colorIfFalseR', f=True)
    cmds.connectAttr(switchName + '.translateZ', condition_name + '.colorIfTrueR', f=True)
    cmds.connectAttr(switchName + '.translateZ', condition_name + '.firstTerm', f=True)
    
    cmds.connectAttr(condition_name + '.outColorR', 'CTRL_' + srcJoint + '.visibility', f=True)
    #ローカルハンドの表示設定ここまで

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
    #猫又のFL、FR系がこれだと反応しないのでおいおい考える
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