# __*__ coding: utf-8 __*__
from maya import cmds, mel

URIKO_STREET_CONBS = ('GEO_jeans_summer_close', 'GEO_shoes', 'GEO_hoodie_body')

def comvine_street_cloth():
    cmds.setAttr('street_cloth_changer.over_ON', 0)
    combine_geo(URIKO_STREET_CONBS, 'GEO_StreetCloth_all')

    bs_name = 'BS_StreetCloth_all'
    dst_geo = 'GEO_StreetCloth_all'
    cmds.blendShape(dst_geo, name = bs_name)

    cmds.setAttr('street_cloth_changer.over_ON', 1)

    res1 = combine_geo(URIKO_STREET_CONBS)

    i=0    
    cmds.blendShape(bs_name, edit=True, t=(dst_geo, i, res1[0], 1.0) )
    cmds.aliasAttr('over_on', bs_name + '.w' + '[' + str(i) + ']')
    cmds.delete(res1[0])

def comvine_street_cloth_old():
    cmds.setAttr('locator1.over_ON', 0)
    cmds.setAttr('locator1.hood_ON', 0)
    combine_geo(URIKO_STREET_CONBS, 'GEO_StreetCloth_all')

    bs_name = 'BS_StreetCloth_all'
    dst_geo = 'GEO_StreetCloth_all'
    cmds.blendShape(dst_geo, name = bs_name)

    cmds.setAttr('locator1.over_ON', 0)
    cmds.setAttr('locator1.hood_ON', 1)
    res1 = combine_geo(URIKO_STREET_CONBS)

    i=0    
    
    cmds.blendShape(bs_name, edit=True, t=(dst_geo, i, res1[0], 1.0) )
    cmds.aliasAttr('hood_on', bs_name + '.w' + '[' + str(i) + ']')
    cmds.delete(res1[0])
    i+=1

    cmds.setAttr('locator1.over_ON', 1)
    cmds.setAttr('locator1.hood_ON', 0)
    res2 = combine_geo(URIKO_STREET_CONBS)

    cmds.blendShape(bs_name, edit=True, t=(dst_geo, i, res2[0], 1.0) )
    cmds.aliasAttr('over_on', bs_name + '.w' + '[' + str(i) + ']')
    cmds.delete(res1[0])
    i+=1

    cmds.setAttr('locator1.over_ON', 1)
    cmds.setAttr('locator1.hood_ON', 1)
    res3 = combine_geo(URIKO_STREET_CONBS)

    cmds.blendShape(bs_name, edit=True, t=(dst_geo, i, res3[0], 1.0) )
    cmds.aliasAttr('hood_over_on', bs_name + '.w' + '[' + str(i) + ']')
    cmds.delete(res1[0])
    i+=1

def combine_geo(source_geos, result_name=''):
    #source_geos = cmds.ls(sl=True)
    #source_geos = URIKO_STREET_CONBS
    conb_geos = []
    for geo in source_geos:
        temp_duped_geo = cmds.duplicate(geo)
        cmds.parent(temp_duped_geo, w=True)
        conb_geos.append(temp_duped_geo)

    result = cmds.polyUnite(*conb_geos, n = result_name)
    cmds.select(cl=True)
    cmds.select(result)
    mel.eval('DeleteHistory')
    cmds.select(cl=True)
    
    for geo in conb_geos:
        cmds.delete(geo)
    
    return result

def create_BlendShape():
    bs_name = 'BS_StreetCloth_all'
    dst_geo = 'GEO_StreetCloth_all'
    cmds.blendShape(dst_geo, name = bs_name)

#単品のスクリプトからとりあえずコピーしてきた
def copy_blend_shape():
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