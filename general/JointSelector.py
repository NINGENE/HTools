# __*__ coding: utf-8 __*__
from maya import OpenMayaUI, cmds, mel
from PySide2 import QtCore, QtWidgets
import shiboken2

'''
create 2018/6/22
update 2020/3/9

概要
最終的にはアニメーションのエクスポートまでサポートしたいけど
今はジョイントとかカーブだけ選択出来る内容

'''
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Selector Tool')
        self.resize(250, 90)

        widget = applyButton()
        self.setCentralWidget(widget)

class applyButton(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(applyButton, self).__init__(*args, **kwargs)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        #↓追々コンボボックス実装したい
        #combo = QtWidgets.QComboBox(layout)
        #comb.addItem('joint')

        self.radio1 = QtWidgets.QRadioButton('joint')
        layout.addWidget(self.radio1)

        self.radio2 = QtWidgets.QRadioButton('nurbus')
        layout.addWidget(self.radio2)

        button = QtWidgets.QPushButton('apply')
        button.clicked.connect(Callback(self.selectNode))
        layout.addWidget(button)

        lineWidget = QtWidgets.QFrame()
        lineWidget.setFrameShape(QtWidgets.QFrame.HLine)
        lineWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(lineWidget)

        button = QtWidgets.QPushButton('Make check Cam')
        button.clicked.connect(Callback(self.makeCheckCam))
        layout.addWidget(button)
        
        lineWidget2 = QtWidgets.QFrame()
        lineWidget2.setFrameShape(QtWidgets.QFrame.HLine)
        lineWidget2.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(lineWidget2)

        #Locator option
        labelWidget1 = QtWidgets.QLabel('Locator Size')
        layout.addWidget(labelWidget1)

        self.inputWidget1 = QtWidgets.QSpinBox()
        self.inputWidget1.setRange(0, 1000)
        self.inputWidget1.setValue(50)
        layout.addWidget(self.inputWidget1)

        #Namespace option
        labelWidget2 = QtWidgets.QLabel('Namespace Name')
        layout.addWidget(labelWidget2)

        self.inputWidget2 = QtWidgets.QLineEdit('RIG_Ref:')
        layout.addWidget(self.inputWidget2)

        #button
        button = QtWidgets.QPushButton('Create Locator')
        button.clicked.connect(Callback(self.makeLocatorForMirror))
        layout.addWidget(button)

        lineWidget3 = QtWidgets.QFrame()
        lineWidget3.setFrameShape(QtWidgets.QFrame.HLine)
        lineWidget3.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(lineWidget3)

        #part of createGround()
        #size opition
        sizeWidgetX = QtWidgets.QLabel('Scale X')
        layout.addWidget(sizeWidgetX)

        self.sizeWidgetX = QtWidgets.QSpinBox()
        self.sizeWidgetX.setRange(0, 10000)
        self.sizeWidgetX.setValue(100)
        layout.addWidget(self.sizeWidgetX)

        sizeWidgetY = QtWidgets.QLabel('Scale Y')
        layout.addWidget(sizeWidgetY)

        self.sizeWidgetY = QtWidgets.QSpinBox()
        self.sizeWidgetY.setRange(0, 10000)
        self.sizeWidgetY.setValue(10)
        layout.addWidget(self.sizeWidgetY)

        sizeWidgetZ = QtWidgets.QLabel('Scale Z')
        layout.addWidget(sizeWidgetZ)

        self.sizeWidgetZ = QtWidgets.QSpinBox()
        self.sizeWidgetZ.setRange(0, 10000)
        self.sizeWidgetZ.setValue(100)
        layout.addWidget(self.sizeWidgetZ)

        button = QtWidgets.QPushButton('Create Ground')
        button.clicked.connect(Callback(self.createGround))
        layout.addWidget(button)

    class GroundCube():
        cubeName = 'test'

        def __init__(self, scaleX, scaleY, scaleZ):
            self.SX = scaleX
            self.SY = scaleY
            self.SZ = scaleZ

        def createCube(self):
            tempCube = cmds.polyCube(name='Ground')
            self.cubeName = tempCube[0]

            cmds.setAttr(self.cubeName + '.scaleX', self.SX)
            cmds.setAttr(self.cubeName + '.scaleY', self.SY)
            cmds.setAttr(self.cubeName + '.scaleZ', self.SZ)
            cmds.delete(self.cubeName + '.f[3]')

            numOfVrt = cmds.polyEvaluate(self.cubeName, v=True)
            i = 0
            while i < numOfVrt:
                vtxName = self.cubeName + '.vtx[' + str(i) + ']'
                cmds.move(0, -(self.SY / 2), 0, vtxName, r=True)

                i+=1
            
            cmds.select(self.cubeName)
            mel.eval('DeleteHistory')
            cmds.select(cl=True)

            

        def createLambert(self):
            print(self.cubeName)
            tempLamSH = cmds.shadingNode('lambert', asShader = True)
            tempLamSG = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name = tempLamSH + 'SG')
            cmds.connectAttr(tempLamSH + '.outColor',  tempLamSG + '.surfaceShader', f=True)
            #shadingNode -asShader lambert;
            #// lambert2 //
            #sets -renderable true -noSurfaceShader true -empty -name lambert2SG;
            #// lambert2SG //
            #connectAttr -f lambert2.outColor lambert2SG.surfaceShader;
            #// lambert2.outColor を lambert2SG.surfaceShader に接続しました。 //

            cmds.setAttr(tempLamSH + '.ambientColor', 0, 1, 1, type='double3')
            cmds.setAttr(tempLamSH + '.transparency', 0.5, 0.5, 0.5, type='double3')
            cmds.sets(self.cubeName, fe=tempLamSG, e=True)
            #select -r lambert2 ;
            #showEditor lambert2;
            #setAttr "lambert2.ambientColor" -type double3 0 1 1 ;
            #setAttr "lambert2.transparency" -type double3 0.55285 0.55285 0.55285 ;
            #select -r pCube1 ;
            #sets -e -forceElement lambert2SG;
            #// lambert2SG //
            #select -cl  ;

    def numberCheck(self):
        checkType = 0
        if self.radio1.isChecked():
            checkType = 1
        elif self.radio2.isChecked():
            checkType = 2
        else:
            pass
    
        return checkType

    def selectNode(self):
        checkType = self.numberCheck()
        print(checkType)

        bakeTopNode = cmds.ls(sl=True)
        if bakeTopNode:
            cmds.select(bakeTopNode, hi=True)
            tempNodes = cmds.ls(sl=True)
        else:
            cmds.error("need select any node")

        if checkType == 1:
            self.pickJoint(tempNodes)
    
        elif checkType == 2:
            self.pickNurbs(tempNodes)
    
        else:
            pass

    def pickJoint(self, tempSrcCtrls):  #ノードチェッカーとしてライブラリにまとめたいかも
        print(tempSrcCtrls)
        cmds.select(cl=True)
        for tempCtrl in tempSrcCtrls:
            #if '_JNT_' in tempCtrl:
            if cmds.nodeType(tempCtrl) == 'joint':
                cmds.select(tempCtrl, add=True)
            else:
                print(tempCtrl + "_end")

    def pickNurbs(self, tempSrcCtrls):
        print(tempSrcCtrls)
        cmds.select(cl=True)
        for tempCtrl in tempSrcCtrls:
            checkNurbus = cmds.listRelatives(tempCtrl,s=True, pa=True, type= 'nurbsCurve')
            if checkNurbus:
                cmds.select(tempCtrl, add=True)

            else:
                pass

    def makeCheckCam(self):
        cam = cmds.camera()
        grp = cmds.group(w=True, em=True,)
        cmds.parent(cam[0], grp)

        cmds.setAttr(cam[0] + '.translate', 0, 0, 3000)
        cmds.setAttr(grp + '.translate', -150, 0, -150)
        cmds.setAttr(grp + '.rotate', -40, 45, 0)
        cmds.setAttr(cam[0] + '.focalLength',  28.000)
        cmds.setAttr(cam[0] + '.horizontalFilmAperture', 1.672)

    def makeLocatorForMirror(self):
        topNode = cmds.ls(sl=True)

        locSize = self.inputWidget1.value()
        nameSpace = self.inputWidget2.text()
        
        if topNode:
            cmds.select(topNode, hi=True)
            tempNodes = cmds.ls(sl=True)
            cmds.select(cl=True)
            isNeed = False

            checkList = ('root_CTRL_C', 'curve_FK', 'curve_IK', 
                        'handCtrl_SWTC_L', 'handCtrl_SWTC_R', 'legCtrl_SWTC_L', 'legCtrl_SWTC_R')

            for node in tempNodes:
                checkNurbus = cmds.listRelatives(node,s=True, pa=True, type= 'nurbsCurve')
                if checkNurbus:
                    if not cmds.objExists('mirror_GRP'):
                        cmds.group(n='mirror_GRP', em=True)

                    isNeed = True
                    for check in checkList:
                        srcName = nameSpace + check
                        if not (node == srcName or node == check):
                            pass

                        else:
                            isNeed = False
                            break


                    if isNeed:
                        locName = 'LOC_' + node
                        cmds.spaceLocator(name = locName)

                        cmds.setAttr(locName + 'Shape.localScaleX', locSize)
                        cmds.setAttr(locName + 'Shape.localScaleY', locSize)
                        cmds.setAttr(locName + 'Shape.localScaleZ', locSize)
                        
                        cmds.pointConstraint(node, locName, mo=False)
                        cmds.orientConstraint(node, locName, mo=True)

                        cmds.parent(locName, 'mirror_GRP')

        else:
            print 'need select a node you want to create locators\n',

    def createGround(self):
        cubeSizeX = self.sizeWidgetX.value()    #default is 100
        cubeSizeY = self.sizeWidgetY.value()    #default is 10
        cubeSizeZ = self.sizeWidgetZ.value()    #default is 100
        
        tempCube = self.GroundCube(cubeSizeX, cubeSizeY, cubeSizeZ)
        tempCube.createCube()
        tempCube.createLambert()

class Callback(object):
    def __init__(self, func, *args, **kwargs):
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

    def __call__(self):
        cmds.undoInfo(openChunk=True)
        try:
            return self.__func(*self.__args, **self.__kwargs)

        except:
            raise
    
        finally:
            cmds.undoInfo(closeChunk=True)

def main():
    window = MainWindow(getMayaWindow())
    window.show()


def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    widget = shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)
    return widget