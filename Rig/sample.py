# __*__ coding: utf-8 __*__
from HTools.rig import HRigSys
reload(HRigSys)

'''
開始日 2021/5/10
新しいリグ生成システムの試験をかねて制作開始
専用コントローラー（髪の毛、とか、チェーン、とか都度色々違うやつ）は
頭とかベースの部分のところとは記述箇所を変えるか
'''

#colors = {'red':13, 'yellow':22, 'blue':15}

shapeDict = {'linerCircle':1, 'ototsuCircle':2, 'cross':3,
             'arrowCross':4, 'box':5, 'pyramid':6, 
             'gear':7, 'sphere':8, 'candyLike':9}

nameSpaceName = ''

POS_LIST = ('_L', '_R')

#ARM_LIMBS = ('clavicle', 'shoulder', 'arm', 'hand', 'weapon')
#ARM_LIMBS = ('clavicle', 'shoulder', 'arm', 'hand')
ARM_LIMBS = ['shoulder', 'arm', 'hand']
#ARM_LIMBS = ('shoulder', 'arm', 'hand', 'weapon')
#ARM_LIMBS = ('shoulder', 'arm', 'hand')
#LEG_LIMBS = ('hip', 'thigh', 'leg', 'foot')
LEG_LIMBS = ('thigh', 'leg', 'foot')
#LEG_LIMBS = ('thigh', 'leg', 'foot', 'toe')

IK_ARM_CTRLS = ('PV_IK_arm', 'IK_hand') #'CTRL_PV_IK_arm_L'
IK_LEG_CTRLS = ('PV_IK_leg', 'IK_foot')

IKGRP = 'IK_GRP'

def main():
    global nameSpaceName
    nameSpaceName = HRigSys.checkNamespace()

    #ルートと移動回転のコントローラー作成
    #ルートコントローラーのパラメーター
    cRoot = HRigSys.ControllerCreator(nameSpaceName, 'Root')
    param=0
    while param == 0:
        cRoot.rx = 0
        cRoot.ry = 0
        cRoot.rz = 0
        cRoot.keyT = 0 
        cRoot.keyR = 0
        cRoot.keyS = 0
        cRoot.shapeNumber = shapeDict['linerCircle']
        cRoot.color = 'red'
        #cRoot.shapeNumber = 'linierCircle'

        param=1

    #移動回転コントローラーのパラメーター
    cTRCtrl = HRigSys.ControllerCreator(nameSpaceName, 'tr')
    param=0
    while param==0:
        cTRCtrl.rx = 0
        cTRCtrl.ry = 0
        cTRCtrl.rz = 0
        cTRCtrl.keyT = 0 
        cTRCtrl.keyR = 0
        cTRCtrl.keyS = 0
        cTRCtrl.shapeNumber = shapeDict['arrowCross']
        cTRCtrl.color = 'red'
        #cTRCtrl.shapeNumber = 'arrowCross'

        param=1

    #コントローラーの生成
    HRigSys.generateRootController(cRoot, cTRCtrl)
    #-----------------------------------------ルートと移動回転のコントローラー作成終了----------------------------

    #スパインコントローラーの生成
    check = True
    if check:
        cHip = HRigSys.ControllerCreator(nameSpaceName, 'hip')
        param=0
        while param==0:
            cHip.shapeNumber = shapeDict['cross']
            cHip.keyT=0
            param=1
        HRigSys.createSimpleController(cHip, isConstraint=True)
        cHip.parentController(cTRCtrl.ctrlName)
    
    check = True
    lastSpine = ''
    if check:
        rootController = cHip.ctrlName #ここは変わる可能性があるからもうちょい見やすくしたい
        spineInfos = []
        spineNum = 2
        i=1
        while i < (spineNum + 1):
            cSpineInfo = HRigSys.ControllerCreator(nameSpaceName, 'spine' + '%02d' %i)
            spineInfos.append(cSpineInfo)
            i+=1
        HRigSys.createFKChain(spineInfos)
        spineInfos[0].parentController(rootController)

        lastSpine = spineInfos[-1]

        
    #--------------------------------------------spineコントローラー終了---------------------------------------

    #ヘッド周りのコントローラー
    headCheck = True
    if headCheck:
        parentController = lastSpine
        cHead = HRigSys.ControllerCreator(nameSpaceName, 'head')
        HRigSys.createSimpleController(cHead, isConstraint=True)
        
        cHead.parentController(parentController.ctrlName)
    #---------------------------------------------head関連終了------------------------------------------------

    #左右があるやつはいまのとろこ全体的に左右のサイズが違う場合に対応していない

    #手のFKコントローラーの作成
    check_handFK = True
    check_hand_L = True
    check_hand_R = True
    FKHandSizeX  = 0.5
    FKHandSizeY  = 0.5
    FKHandSizeZ  = 0.5
    if check_handFK:
        parentController = lastSpine
        cArmFKLimbsListL = []
        cArmFKLimbsListR = []
        limbList = ARM_LIMBS
        positionList = checkLR(check_hand_L, check_hand_R)

        for pos in positionList:
            FKLimbList = []
            for limb in limbList:
                cLimb = HRigSys.ControllerCreator(nameSpaceName, limb, pos)
                
                cLimb.sx = FKHandSizeX #0.5
                cLimb.sy = FKHandSizeY #0.5
                cLimb.sz = FKHandSizeZ #0.5
                cLimb.shapeNumber = shapeDict['linerCircle']
                cLimb.color = 'blue'
                
                FKLimbList.append(cLimb)
            
            if pos == '_L':
                cArmFKLimbsListL = FKLimbList
                HRigSys.generateFKLimbs(cArmFKLimbsListL)
            else:
                cArmFKLimbsListR = FKLimbList
                HRigSys.generateFKLimbs(cArmFKLimbsListR)
        
        if check_hand_L:
            cArmFKLimbsListL[0].parentController(parentController.ctrlName)
        if check_hand_R:
            cArmFKLimbsListR[0].parentController(parentController.ctrlName)
    
    #足のFKコントローラーの作成
    #こちらも片足の場合があるので左右でチェック出来るように
    check_legFK = True
    check_leg_L = True
    check_leg_R = True
    FKLegSizeX  = 0.5
    FKLegSizeY  = 0.5
    FKLegSizeZ  = 0.5
    if check_legFK:
        parentController = cHip.ctrlName
        cLegFKLimbsListL = []
        cLegFKLimbsListR = []
        limbList = LEG_LIMBS
        positionList = checkLR(check_leg_L, check_leg_R)

        for pos in positionList:
            FKLimbList = []
            for limb in limbList:
                cLimb = HRigSys.ControllerCreator(nameSpaceName, limb, pos)
                
                cLimb.sx = FKLegSizeX
                cLimb.sy = FKLegSizeY
                cLimb.sz = FKLegSizeZ
                cLimb.shapeNumber = shapeDict['linerCircle']
                cLimb.color = 'blue'
                
                FKLimbList.append(cLimb)
            
            if pos == '_L':
                cLegFKLimbsListL = FKLimbList
                HRigSys.generateFKLimbs(cLegFKLimbsListL)
            else:
                cLegFKLimbsListR = FKLimbList
                HRigSys.generateFKLimbs(cLegFKLimbsListR)

        if check_leg_L:
            cLegFKLimbsListL[0].parentController(parentController)
        if check_leg_R:
            cLegFKLimbsListR[0].parentController(parentController)
    #-----------------------------------------FKコントローラー作成終了-----------------------------------------

    #手のIKコントローラーの作成
    #これも左右で別々にチェック
    check_armIK = True
    if check_armIK:
        cArmIKLimbsListL = []
        cArmIKLimbsListR = []
        limbList = ARM_LIMBS
        positionList = checkLR(check_hand_L, check_hand_R)

        for pos in positionList:
            IKLimbList = []
            rotX = 90
            if not pos == '_L':
                rotX = -90
            #shoulder
            cIKLimb = HRigSys.ControllerCreator(nameSpaceName, limbList[0], pos)
            IKLimbList.append(cIKLimb)

            #arm
            cIKLimb = HRigSys.ControllerCreator(nameSpaceName, limbList[1], pos)

            cIKLimb.tx = 0
            cIKLimb.ty = 0
            cIKLimb.tz = -2
            cIKLimb.rx = rotX
            cIKLimb.ry = 0
            cIKLimb.rz = 0
            cIKLimb.sx = 0.25
            cIKLimb.sy = 0.25
            cIKLimb.sz = 0.25
            cIKLimb.keyT = 0
            cIKLimb.keyR = 1
            cIKLimb.shapeNumber = shapeDict['pyramid']

            IKLimbList.append(cIKLimb)
            #hand
            cIKLimb = HRigSys.ControllerCreator(nameSpaceName, limbList[2], pos)

            cIKLimb.rx = 0
            cIKLimb.ry = 0
            cIKLimb.rz = 0
            cIKLimb.sx = 1
            cIKLimb.sy = 1
            cIKLimb.sz = 1
            cIKLimb.keyT = 0
            cIKLimb.shapeNumber = shapeDict['box']

            IKLimbList.append(cIKLimb)

            if pos == '_L':
                cArmIKLimbsListL = IKLimbList
                HRigSys.generateIKLimbs(cArmIKLimbsListL)
            else:
                cArmIKLimbsListR = IKLimbList
                HRigSys.generateIKLimbs(cArmIKLimbsListR)

    #足のIKコントローラーの作成
    #ここも左右チェック
    check_legIK = True
    if check_legIK:
        cLegIKLimbsListL = []
        cLegIKLimbsListR = []
        limbList = LEG_LIMBS
        positionList = checkLR(check_leg_L, check_leg_R)

        for pos in positionList:
            IKLimbList = []
            rotX = 90
            if not pos == '_L':
                rotX = -90
            #shoulder
            cIKLimb = HRigSys.ControllerCreator(nameSpaceName, limbList[0], pos)
            IKLimbList.append(cIKLimb)

            #arm
            cIKLimb = HRigSys.ControllerCreator(nameSpaceName, limbList[1], pos)

            cIKLimb.tx = 0
            cIKLimb.ty = 0
            cIKLimb.tz = 1
            cIKLimb.rx = rotX
            cIKLimb.ry = 0
            cIKLimb.rz = 0
            cIKLimb.sx = 0.15
            cIKLimb.sy = 0.15
            cIKLimb.sz = 0.15
            cIKLimb.keyT = 0
            cIKLimb.keyR = 1
            cIKLimb.shapeNumber = shapeDict['pyramid']

            IKLimbList.append(cIKLimb)
            #hand
            cIKLimb = HRigSys.ControllerCreator(nameSpaceName, limbList[2], pos)

            cIKLimb.rx = 0
            cIKLimb.ry = 0
            cIKLimb.rz = 0
            cIKLimb.sx = 0.25
            cIKLimb.sy = 0.25
            cIKLimb.sz = 0.25
            cIKLimb.keyT = 0
            cIKLimb.shapeNumber = shapeDict['box']

            IKLimbList.append(cIKLimb)

            if pos == '_L':
                cLegIKLimbsListL = IKLimbList
                HRigSys.generateIKLimbs(cLegIKLimbsListL)
            else:
                cLegIKLimbsListR = IKLimbList
                HRigSys.generateIKLimbs(cLegIKLimbsListR)
    #-------------------------------------IKコントローラー作成終了--------------------

    HRigSys.generateSwitch(pos = [4, 6, 0])

    if check_hand_L:
        HRigSys.setLimbsFKSwitch(cArmFKLimbsListL, 'handCtrl_SWTC')
        HRigSys.setLimbsIKSwitch(cArmIKLimbsListL, 'handCtrl_SWTC')

    if check_hand_R:
        HRigSys.setLimbsFKSwitch(cArmFKLimbsListR, 'handCtrl_SWTC')
        HRigSys.setLimbsIKSwitch(cArmIKLimbsListR, 'handCtrl_SWTC')

    if check_leg_L:
        HRigSys.setLimbsFKSwitch(cLegFKLimbsListL, 'footCtrl_SWTC')
        HRigSys.setLimbsIKSwitch(cLegIKLimbsListL, 'footCtrl_SWTC')
    
    if check_leg_R:
        HRigSys.setLimbsFKSwitch(cLegFKLimbsListR, 'footCtrl_SWTC')
        HRigSys.setLimbsIKSwitch(cLegIKLimbsListR, 'footCtrl_SWTC')

    #--------------------FKIKのコンストレイント終了----------------------------

    #-----------------------FKIKジョイントの整理-------------------------------
    if check_handFK:
        HRigSys.createFKIKJointGroupArm(parentController=lastSpine.ctrlName)
        if check_hand_L:
            HRigSys.parentFKIKJoint(cArmFKLimbsListL[0], 'armsFKIK_JNT_GRP')
            HRigSys.parentFKIKJoint(cArmIKLimbsListL[0], 'armsFKIK_JNT_GRP')

        if check_hand_R:
            HRigSys.parentFKIKJoint(cArmFKLimbsListR[0], 'armsFKIK_JNT_GRP')
            HRigSys.parentFKIKJoint(cArmIKLimbsListR[0], 'armsFKIK_JNT_GRP')

    if check_legFK:
        HRigSys.createFKIKJointGroupLeg(parentController=cHip.ctrlName)
        if check_leg_L:
            HRigSys.parentFKIKJoint(cLegFKLimbsListL[0], 'legsFKIK_JNT_GRP')
            HRigSys.parentFKIKJoint(cLegIKLimbsListL[0], 'legsFKIK_JNT_GRP')
        
        if check_leg_R:
            HRigSys.parentFKIKJoint(cLegFKLimbsListR[0], 'legsFKIK_JNT_GRP')
            HRigSys.parentFKIKJoint(cLegIKLimbsListR[0], 'legsFKIK_JNT_GRP')

    #-------------------------IKコントローラーの整理----------------------------
    HRigSys.createFKIKControllerGroup('armsFKIK_CTRL_GRP', 'legsFKIK_CTRL_GRP')
    if check_hand_L:
        HRigSys.parentIKController(cArmIKLimbsListL[1], 'armsFKIK_CTRL_GRP')
        HRigSys.parentIKController(cArmIKLimbsListL[2], 'armsFKIK_CTRL_GRP')
    
    if check_hand_R:
        HRigSys.parentIKController(cArmIKLimbsListR[1], 'armsFKIK_CTRL_GRP')
        HRigSys.parentIKController(cArmIKLimbsListR[2], 'armsFKIK_CTRL_GRP')

    if check_leg_L:
        HRigSys.parentIKController(cLegIKLimbsListL[1], 'legsFKIK_CTRL_GRP')
        HRigSys.parentIKController(cLegIKLimbsListL[2], 'legsFKIK_CTRL_GRP')

    if check_leg_R:
        HRigSys.parentIKController(cLegIKLimbsListR[1], 'legsFKIK_CTRL_GRP')
        HRigSys.parentIKController(cLegIKLimbsListR[2], 'legsFKIK_CTRL_GRP')

    HRigSys.createIKGroup()

    #-----------------createOptionalController-------------------
    #関数に仕様と思ったけど親コントローラー取得が面倒だったのでmainの中に作る
    #Only Kodama
    treeCheck = False
    lastSpine = ''
    if treeCheck:
        rootController = 'CTRL_tr_C'
        #jointList = ['tree', 'tentacle']
        jointList = []
        cTree = HRigSys.ControllerCreator(nameSpaceName, 'tree')
        param=0
        while param == 0:
            cTree.rx = 90
            #cTree.ry = -180
            #cTree.rz = -90
            cTree.keyT = 0 
            cTree.keyR = 0
            #cTree.keyS = 0
            cTree.shapeNumber = shapeDict['cross']
            cTree.color = 'blue'

            param=1
        
        jointList.append(cTree)

        cTentacle = HRigSys.ControllerCreator(nameSpaceName, 'tentacle')
        param=0
        while param == 0:
            #cRoot.rx = 0
            #cRoot.ry = 0
            #cRoot.rz = 0
            cTentacle.sx = 0.75
            cTentacle.sy = 0.75
            cTentacle.sz = 0.75
            #cRoot.keyT = 0 
            cTentacle.keyR = 0
            #cRoot.keyS = 0
            cTentacle.shapeNumber = shapeDict['linerCircle']
            cTentacle.color = 'blue'

            param=1

        jointList.append(cTentacle)
        HRigSys.createFKChain(jointList)
        jointList[0].parentController(rootController)


def checkLR(check_L, check_R):
    positionList = []
    if check_L:
        if check_R:
            positionList = ['_L', '_R']
        else:
            positionList = ['_L']
    elif check_R:
        positionList = ['_R']
    
    return positionList


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