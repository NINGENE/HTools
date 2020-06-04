from maya import cmds, mel
from HTools.lib import HToolsLib, CreateShapes
reload(HToolsLib)
reload(CreateShapes)

def createGeneCtrl():
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