from maya import cmds, mel
from ..lib import CreateShapes, HToolsLib

posList = ['Left', 'Right']
jointPrifix = 'MODEL:Character1_'
corePrimJntNameList = ['Hips', 'Spine', 'Spine1', 'Spine2', 'Neck', 'Head']

def main():
    createControllers()

    primJntNameList = ['ForeArm', 'Hand']
    createIKContoroller(primJntNameList, -1)

    primJntNameList = ['Leg', 'Foot']
    createIKContoroller(primJntNameList)

    parentContorollers()

    attachFKControllers()

    primJntNameList = ['ForeArm', 'Hand']
    limbs = ['Arm', 'ForeArm', 'Hand']
    createIK(primJntNameList, limbs)

    primJntNameList = ['Leg', 'Foot']
    limbs = ['UpLeg', 'Leg', 'Foot']
    createIK(primJntNameList, limbs)

def createControllers():
    primJntName = 'Hips'
    jointName = jointPrifix + primJntName
    ctrlName = 'CTRL_' + primJntName + '_C'

    tempName = CreateShapes.cross()
    HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')

    cmds.pointConstraint(jointName, ctrlName)
    cmds.select(ctrlName, r=True)
    cmds.delete(cn=True)

    cmds.select(ctrlName, r=True)
    cmds.rotate(0, 0, 0)
    cmds.scale(25, 25, 25)
    HToolsLib.freezeAndDeletehistory()

    primJoints = ('Spine', 'Spine1', 'Spine2')
    for primJntName in primJoints:
        jointName = jointPrifix + primJntName
        ofstName  = 'OFST_' + primJntName + '_C'
        ctrlName  = 'CTRL_' + primJntName + '_C'

        tempName = CreateShapes.ototsuCircle()

        HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')
        HToolsLib.creatOffset(ofstName, ctrlName, jointName)
        cmds.parentConstraint(jointName, ctrlName)
        cmds.select(ctrlName, r=True)
        cmds.delete(cn=True)

        cmds.select(ctrlName, r=True)
        cmds.rotate(0, 180, 90)
        cmds.scale(20, 20, 20)

        HToolsLib.freezeAndDeletehistory()

    primJoints = ('Neck','Head')
    for primJntName in primJoints:
        jointName = jointPrifix + primJntName
        ofstName  = 'OFST_' + primJntName + '_C'
        ctrlName  = 'CTRL_' + primJntName + '_C'

        tempName = CreateShapes.ototsuCircle()

        HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')
        HToolsLib.creatOffset(ofstName, ctrlName, jointName)
        cmds.parentConstraint(jointName, ctrlName)
        cmds.select(ctrlName, r=True)
        cmds.delete(cn=True)

        cmds.select(ctrlName, r=True)
        cmds.rotate(0, 180, 90)
        cmds.scale(10, 10, 10)

        HToolsLib.freezeAndDeletehistory()

    primJoints = ('LeftEye','RightEye')
    for primJntName in primJoints:
        jointName = jointPrifix + primJntName
        #ofstName  = 'OFST_' + primJntName
        ctrlName  = 'CTRL_' + primJntName

        tempName = CreateShapes.linerCircle()

        HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')
        #HToolsLib.creatOffset(ofstName, ctrlName, jointName)
        cmds.parentConstraint(jointName, ctrlName)
        cmds.select(ctrlName, r=True)
        cmds.delete(cn=True)

        cmds.select(ctrlName, r=True)
        cmds.move(0, 0, 10, r=True, wd=True)
        cmds.rotate(90, 0, 0)
        cmds.scale(1, 1, 1)

        HToolsLib.freezeAndDeletehistory()

    ctrlName  = 'CTRL_eyes'

    tempName = CreateShapes.linerCircle()

    HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')
    cmds.parentConstraint(jointName, ctrlName)
    cmds.select(ctrlName, r=True)
    cmds.delete(cn=True)

    cmds.select(ctrlName, r=True)
    cmds.move(0, x=True, a=True, wd=True)
    cmds.move(0, 0, 10, r=True, wd=True)
    cmds.rotate(90, 0, 0)
    cmds.scale(6, 2, 1)

    HToolsLib.freezeAndDeletehistory()
    
    for pos in posList:
        #shoulder
        shoulderRot = 90
        if pos == 'Right':
            shoulderRot *= -1
        primJntName = pos + 'Shoulder'
        jointName = jointPrifix + primJntName
        ofstName  = 'OFST_' + primJntName
        ctrlName  = 'CTRL_' + primJntName

        tempName = CreateShapes.candyLike()

        HToolsLib.renameAndColorV2(tempName, ctrlName, 'blue')
        HToolsLib.creatOffset(ofstName, ctrlName, jointName)

        cmds.parentConstraint(jointName, ctrlName)
        cmds.select(ctrlName, r=True)
        cmds.delete(cn=True)

        cmds.select(ctrlName, r=True)
        cmds.move(0, 0, 0, r=True, wd=True)
        cmds.rotate(0, shoulderRot, 90)
        cmds.scale(5, 5, 5)

        HToolsLib.freezeAndDeletehistory()


def createIKContoroller(primJntNameList, frontBack = 1):
    for pos in posList:
        #twist
        primJntName = pos + primJntNameList[0]
        jointName = jointPrifix + primJntName
        ctrlName = 'CTRL_IK_' + primJntName + 'TW'

        tempName = CreateShapes.pyramid()
        HToolsLib.renameAndColorV2(tempName, ctrlName, 'blue')

        cmds.parentConstraint(jointName, ctrlName)
        cmds.select(ctrlName, r=True)
        cmds.delete(cn=True)

        cmds.select(ctrlName, r=True)
        cmds.move(0, 0, (frontBack * 30), r=True, wd=True)
        cmds.rotate((frontBack * 90), 0, 0)
        cmds.scale(5, 5, 5)

        HToolsLib.freezeAndDeletehistory()

        #creating IK controller.
        primJntName = pos + primJntNameList[1]
        jointName = jointPrifix + primJntName
        ctrlName = 'CTRL_IK_' + primJntName

        tempName = CreateShapes.box()

        HToolsLib.renameAndColorV2(tempName, ctrlName, 'yellow')

        cmds.parentConstraint(jointName, ctrlName)
        cmds.select(ctrlName, r=True)
        cmds.delete(cn=True)

        cmds.select(ctrlName, r=True)
        cmds.rotate(0, 0, 0)
        cmds.scale(10, 10, 10)

        HToolsLib.freezeAndDeletehistory()


def parentContorollers():
    for i in range(0, (len(corePrimJntNameList)-1)):
        src = 'CTRL_' + corePrimJntNameList[i] + '_C'
        dst = 'OFST_' + corePrimJntNameList[i+1] + '_C'
        cmds.parent(dst, src)

    src = 'CTRL_Spine2_C'
    dst = 'OFST_LeftShoulder'
    cmds.parent(dst, src)
    dst = 'OFST_RightShoulder'
    cmds.parent(dst, src)

    src = 'CTRL_eyes'
    dst = 'CTRL_LeftEye'
    cmds.parent(dst, src)
    dst = 'CTRL_RightEye'
    cmds.parent(dst, src)

    src = 'CTRL_Head_C'
    dst = 'CTRL_eyes'
    cmds.parent(dst, src)

    rootGroupName = 'rig_system'
    cmds.group(w=True, em=True, n='rig_system')
    cmds.parent('CTRL_Hips_C', rootGroupName)

    IKS = ['ForeArmTW', 'Hand', 'LegTW', 'Foot']
    for pos in posList:
        for IK in IKS:
            dst = 'CTRL_IK_' + pos + IK
            cmds.parent(dst, rootGroupName)

def attachFKControllers():
    for primJntName in corePrimJntNameList:
        src = 'CTRL_' + primJntName + '_C' 
        dst = jointPrifix + primJntName
        cmds.parentConstraint(src, dst, mo=True)
    
    src = 'CTRL_LeftShoulder'
    dst = 'MODEL:Character1_LeftShoulder'
    cmds.parentConstraint(src, dst, mo=True)
    src = 'CTRL_RightShoulder'
    dst = 'MODEL:Character1_RightShoulder'
    cmds.parentConstraint(src, dst, mo=True)

    #It's not FK but in here now.
    src = 'CTRL_LeftEye'
    dst = 'MODEL:Character1_LeftEye'
    cmds.aimConstraint(src, dst, mo=True)
    src = 'CTRL_RightEye'
    dst = 'MODEL:Character1_RightEye'
    cmds.aimConstraint(src, dst, mo=True)


def createIK(primJntNameList, limbs):
    for pos in posList:
        ctrlName = 'CTRL_IK_' + pos + primJntNameList[1]
        pvName   = 'CTRL_IK_' + pos + primJntNameList[0] + 'TW'
        ikName   = 'IK_' + pos + primJntNameList[1]
        pVector  = ikName + '.poleVector'
        PVOffset = ikName + '_poleVectorConstraint1.offset'
        sJoint   = jointPrifix + pos + limbs[0]
        eEfector = jointPrifix + pos + limbs[2]

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
        
        srcCTRL = ctrlName
        dstJNT = jointPrifix + pos + limbs[2]
        cmds.orientConstraint(srcCTRL, dstJNT, mo=True)