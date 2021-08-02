# __*__ coding: utf-8 __*__
from maya import cmds, mel

def main(isLock = True):
    lockJoint = cmds.ls(sl=True)

    if cmds.nodeType(lockJoint) == 'joint':

        cmds.select(cl=True)
        cmds.select(lockJoint, hi=True)
        lock_Joints = cmds.ls(sl=True)

        for joint in lock_Joints:
            if cmds.nodeType(lockJoint) == 'joint':
                cmds.setAttr(joint + '.liw', isLock)
                #print(lock_Joints)
    
    else:
        cmds.error('Please select joint.')
