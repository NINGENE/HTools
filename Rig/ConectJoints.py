# __*__ coding: utf-8 __*__
from maya import cmds, mel

def main():
    #これは完全にHumanoid構成で書かれているので応用が効かない
    forRigJoints = ['hip_C', 'spine01_C', 'spine02_C', 'neck_C', 'head_C',
                    'clavicle_L', 'shoulder_L', 'arm_L',
                    'clavicle_R', 'shoulder_R', 'arm_R',
                    'thigh_L', 'thigh_R']
    
    HUMANOID_JOINTS = ['Hips', 'spine', 'chest', 'neck', 'head',
                      'shoulder_L', 'upperArm_L', 'lowerArm_L',
                      'shoulder_R', 'upperArm_R', 'lowerArm_R',
                      'upLeg_L', 'upLeg_R']
    
    copyJoints = cmds.ls(sl=True)
    if not len(copyJoints) == 2:
        print('Please choose 2 root Joints')
        #print(copyJoints)
    
    #ジョイント以外を選択した時のことを考えてない
    else:
        if copyJoints[0] == 'MODEL:Hips':
            cmds.select(cl=True)
            cmds.select(copyJoints[0], hi=True)
            dstJoints = cmds.ls(sl=True)

            cmds.select(cl=True)
            cmds.select(copyJoints[1], hi=True)
            srcJoints = cmds.ls(sl=True)
        elif copyJoints[1] == 'MODEL:Hips':
            cmds.select(cl=True)
            cmds.select(copyJoints[1], hi=True)
            dstJoints = cmds.ls(sl=True)
        
            cmds.select(cl=True)
            cmds.select(copyJoints[0], hi=True)
            srcJoints = cmds.ls(sl=True)

        for i in range(len(dstJoints)):
            cmds.parentConstraint(srcJoints[i], dstJoints[i])

        for i in range(len(HUMANOID_JOINTS)):
            cmds.rename(HUMANOID_JOINTS[i], forRigJoints[i])

        cmds.select(d=True)
        rootJoint = cmds.joint(name = 'Root', p=(0,0,0))
        cmds.parent(forRigJoints[0], rootJoint)
        cmds.select(d=True)
    

