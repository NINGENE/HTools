# __*__ coding: utf-8 __*__
from maya import OpenMayaUI, cmds, mel
from PySide2 import QtCore, QtGui, QtWidgets
import shiboken2
from NEOTool.rigging import NeoRigCreator
from NEOTool.rigging import NeoRigAttach
from NEOTool.rigging import NeoRigParent
reload(NeoRigCreator)
reload(NeoRigAttach)
reload(NeoRigParent)


'''
NEOTools
create 18/12/25

各コントローラーのサイズを記憶させる何かがあった方が楽だろうか・・・
あとは各モンスターってより足があるなし、羽があるなし、とかのオプションつけ足して
どのコントローラー生成するかを決めた方がいいかも
単純にFKだけで足りそうなやつ（earとかconeとか？）はextention関数に入れて
足の有無とかをオプションにする（蜂はあし要らない、狼と熊で足の構造違うとかを分ける）
'''

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setWindowTitle('Rig Generator')
		self.resize(250, 90)
		
		widget = applyButton()
		self.setCentralWidget(widget)

class OptionWidget(QtWidgets.QWidget):
	def __init__(self, *args, **kwargs):
		super(OptionWidget, self).__init__(*args, **kwargs)

		optionLayout = QtWidgets.QFormLayout(self)

		#ドッグレッグリグのオンオフ確認
		self.checkWidgetDL = QtWidgets.QCheckBox('Is Dog Leg')
		optionLayout.addRow('', self.checkWidgetDL)

		#アーム作成の可否
		self.checkWidgetLeg = QtWidgets.QCheckBox('Make Leg')
		optionLayout.addRow('', self.checkWidgetLeg)		

		#アーム作成の可否
		self.checkWidgetArm = QtWidgets.QCheckBox('Make Arm')
		optionLayout.addRow('', self.checkWidgetArm)

		#翼作成の可否
		self.checkWidgetWing = QtWidgets.QCheckBox('Make Wing')
		optionLayout.addRow('', self.checkWidgetWing)

		#size of controller
		self.inputSize = QtWidgets.QSpinBox()
		self.inputSize.setRange(0, 1000)
		self.inputSize.setValue(5)
		optionLayout.addRow('Size', self.inputSize)

class applyButton(QtWidgets.QWidget):
	def __init__(self, *args, **kwargs):
		super(applyButton, self).__init__(*args, **kwargs)
		self.testText = 'None'	#テスト用なので最終的に要らない
		self.HierarchyList = ()	#testParentForCutterで作成したジョイントの親子関係を格納するところ
		
		layout = QtWidgets.QVBoxLayout()
		self.setLayout(layout)
		
		self.test = OptionWidget()
		layout.addWidget(self.test)

		button = QtWidgets.QPushButton('spam!!')
		button.clicked.connect(Callback(self.debugCommand))
		layout.addWidget(button)

		button = QtWidgets.QPushButton('Genarate Controller')
		button.clicked.connect(Callback(self.generateRig))
		layout.addWidget(button)

		button = QtWidgets.QPushButton('Parent Controller')
		button.clicked.connect(Callback(self.parentController))
		layout.addWidget(button)

		button = QtWidgets.QPushButton('Attach Controller')
		button.clicked.connect(Callback(self.attachController))
		layout.addWidget(button)

	def debugCommand(self):
		number = 0
		text = 'spam!!'
		print(text)
		return number
	
	def generateRig(self):
		isDogLeg = self.test.checkWidgetDL.isChecked()
		useLeg   = self.test.checkWidgetLeg.isChecked()
		useArm   = self.test.checkWidgetArm.isChecked()
		useWing  = self.test.checkWidgetWing.isChecked()
		size     = self.test.inputSize.value()
		NeoRigCreator.controllerGenerator(isDogLeg, useLeg, useArm, useWing, size)

	def parentController(self):
		isDogLeg = self.test.checkWidgetDL.isChecked()
		useLeg   = self.test.checkWidgetLeg.isChecked()
		useArm   = self.test.checkWidgetArm.isChecked()
		useWing  = self.test.checkWidgetWing.isChecked()
		NeoRigParent.main(isDogLeg, useLeg, useArm, useWing)
		
	def attachController(self):
		isDogLeg = self.test.checkWidgetDL.isChecked()
		useLeg   = self.test.checkWidgetLeg.isChecked()
		useArm   = self.test.checkWidgetArm.isChecked()
		useWing  = self.test.checkWidgetWing.isChecked()		
		NeoRigAttach.main(isDogLeg, useLeg, useArm, useWing)

class testButton(QtWidgets.QWidget):
	def __init__(self, *args, **kwargs):
		super(testButton, self).__init__(*args, **kwargs)

		self.HierarchyList = ()	#testParentForCutterで作成したジョイントの親子関係を格納するところ
		
		layout = QtWidgets.QVBoxLayout()
		self.setLayout(layout)

		button = QtWidgets.QPushButton('Test Parent Ctrlr for Cutter')
		button.clicked.connect(Callback(self.testParentForCutter))
		layout.addWidget(button)

		button = QtWidgets.QPushButton('Test attach Ctrlr for Cutter')
		button.clicked.connect(Callback(self.testAttachForCutter))
		layout.addWidget(button)

	def testParentForCutter(self):
		#monsterType = self.numberCheck()
		self.HierarchyList = NeoRigParent.testAutoParentForCutter()

	def testAttachForCutter(self):
		if not self.HierarchyList:
			cmds.error('needs attach joint list')
		else:
			attachJointList = self.HierarchyList[1]
			NeoRigAttach.testAttachForCutter(attachJointList)


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
	toolWindow = MainWindow(getMayaWindow())
	toolWindow.show()

def getMayaWindow():
	ptr = OpenMayaUI.MQtUtil.mainWindow()
	widget = shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)
	return widget