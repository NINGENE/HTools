# __*__ coding: utf-8 __*__
from maya import cmds, mel

def copyBlendShape():
    #リテラルはダサい
    srcBS  = 'BS_head_old2'
    srcGeo = 'GEO_head_old2'
    dstGeo = 'GEO_head'

    bsName = 'BS_head'
    cmds.blendShape(dstGeo, name = bsName)

    bsList = cmds.listAttr(srcBS + '.w', m = True)
    for i in range(len(bsList)):
        cmds.setAttr(srcBS + '.' + bsList[i], 1)
        tempHead = cmds.duplicate(srcGeo)
        
        cmds.blendShape(bsName, edit=True, t=(dstGeo, i, tempHead[0], 1.0) )
        cmds.aliasAttr(bsList[i], bsName + '.w' + '[' + str(i) + ']')
        cmds.setAttr(srcBS + '.' + bsList[i], 0)

        cmds.delete(tempHead[0])
