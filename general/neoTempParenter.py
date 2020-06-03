# __*__ coding: utf-8 __*__
from maya import cmds, mel

'''
create 2018/6/21

description:
RIG移行のためのスクリプト
新コントローラーを旧コントローラーにペアレントする
各モンスター専用設計かつ、
特定の条件出ないと動かないため自由は利かない（なんども利用する予定もない）
'''
def verRhino():
	cmds.select(cl=True)
	#自分よ、左のノードに右をコンストレインだぞ
	cmds.parentConstraint('root_CTRL_C', 'RIG:root_CTRL_C', mo=True)
	cmds.parentConstraint('tr_CTRL_C', 'RIG:tr_CTRL_C', mo=True)
	cmds.parentConstraint('spine_01_CTRL_C', 'RIG:spine_01_CTRL_C', mo=True)

	i = 2
	while cmds.objExists('RIG:spine_0' + str(i) + '_CTRL_C'):
		cmds.orientConstraint('spine_0' + str(i) + '_CTRL_C', 'RIG:spine_0' + str(i) + '_CTRL_C', mo=True)
		i+=1

	cmds.orientConstraint('neck_CTRL_C', 'RIG:neck_CTRL_C', mo=True)
	cmds.orientConstraint('head_CTRL_C', 'RIG:head_CTRL_C', mo=True)

	#cmds.orientConstraint('pelvis_CTRL_C', 'MODEL:pelvis_JNT_C', mo=True)
	
	cmds.orientConstraint('clavicle_CTRL_L', 'RIG:clavicle_CTRL_L', mo=True)
	cmds.orientConstraint('clavicle_CTRL_R', 'RIG:clavicle_CTRL_R', mo=True)
	
	cmds.orientConstraint('thigh_CTRL_L', 'RIG:thigh_CTRL_L', mo=True)
	cmds.orientConstraint('thigh_CTRL_R', 'RIG:thigh_CTRL_R', mo=True)
	#FKコントローラーはoldには無いのでコンストレインしないので書かない

	cmds.parentConstraint('hand_CTRL_L', 'RIG:hand_CTRL_L', mo=True)
	cmds.parentConstraint('hand_CTRL_R', 'RIG:hand_CTRL_R', mo=True)
	cmds.parentConstraint('foot_CTRL_L', 'RIG:foot_CTRL_L', mo=True)
	cmds.parentConstraint('foot_CTRL_R', 'RIG:foot_CTRL_R', mo=True)

	cmds.orientConstraint('armfinger_CTRL_L', 'RIG:armfinger_CTRL_L', mo=True)
	cmds.orientConstraint('armfinger_CTRL_R', 'RIG:armfinger_CTRL_R', mo=True)
	cmds.orientConstraint('footfinger_CTRL_L', 'RIG:footfinger_CTRL_L', mo=True)
	cmds.orientConstraint('footfinger_CTRL_R', 'RIG:footfinger_CTRL_R', mo=True)

	cmds.pointConstraint('arm_PV_CTRL_L', 'RIG:arm_PV_CTRL_L', mo=True)
	cmds.pointConstraint('arm_PV_CTRL_R', 'RIG:arm_PV_CTRL_R', mo=True)
	cmds.pointConstraint('leg_PV_CTRL_L', 'RIG:leg_PV_CTRL_L', mo=True)
	cmds.pointConstraint('leg_PV_CTRL_R', 'RIG:leg_PV_CTRL_R', mo=True)

	#↓↓ユニークコントローラー
	#jawあるやつ
	#if cmds.objExists('MODEL:jaw_JNT_C'):
	#	cmds.orientConstraint('jaw_CTRL_C', 'MODEL:jaw_JNT_C', mo=True)

	#noseあるやつ
	if cmds.objExists('RIG:nose_CTRL_C'):
		cmds.orientConstraint('nose_CTRL_C', 'RIG:nose_CTRL_C', mo=True)
	
	#if cmds.objExists('MODEL:brow_JNT_C'):
	#	cmds.orientConstraint('brow_CTRL_C', 'MODEL:brow_JNT_C', mo=True)


	#尻尾あるやつtail作成
	i = 1
	while cmds.objExists('RIG:tail_0' + str(i) + '_CTRL_C'):
		srcCTRL = 'tail_0' + str(i) + '_CTRL_C'
		dstJNT = 'RIG:tail_0' + str(i) + '_CTRL_C'
		cmds.orientConstraint(srcCTRL, dstJNT, mo=True)
		i += 1

	#coneあるやつ（オオカミのみ）
	#i = 1
	#while cmds.objExists('MODEL:cone_0'+str(i)+'_JNT_C'):
	#	srcCTRL = 'cone_0' + str(i) + '_CTRL_C'
	#	dstJNT = 'MODEL:cone_0' + str(i) + '_JNT_C'
	#	cmds.parentConstraint(srcCTRL, dstJNT, mo=True)
	#	i += 1
	LRList = ['_L', '_R']
	#耳のあるやつ
	for LR in LRList:
		srcCTRL = 'ear_CTRL' +LR
		dstJNT = 'RIG:ear_01_CTRL' + LR
		cmds.orientConstraint(srcCTRL, dstJNT, mo=True)

	#Cannon作成（サイだけ）
	for LR in LRList:
		cmds.parentConstraint('Cannon_CTRL'+LR, 'RIG:Cannon_CTRL'+LR, mo=True)


def verWolf():
	cmds.select(cl=True)
	#自分よ、左のノードに右をコンストレインだぞ
	cmds.parentConstraint('root_CTRL_C', 'RIG:root_CTRL_C', mo=True)
	cmds.parentConstraint('tr_CTRL_C', 'RIG:tr_CTRL_C', mo=True)
	cmds.parentConstraint('spine_01_CTRL_C', 'RIG:spine_01_CTRL_C', mo=True)

	i = 2
	while cmds.objExists('RIG:spine_0' + str(i) + '_CTRL_C'):
		cmds.orientConstraint('spine_0' + str(i) + '_CTRL_C', 'RIG:spine_0' + str(i) + '_CTRL_C', mo=True)
		i+=1

	cmds.orientConstraint('neck_CTRL_C', 'RIG:neck_CTRL_C', mo=True)
	cmds.orientConstraint('head_CTRL_C', 'RIG:head_CTRL_C', mo=True)

	cmds.orientConstraint('pelvis_CTRL_C', 'RIG:pelvis_CTRL_C', mo=True)
	
	cmds.orientConstraint('clavicle_CTRL_L', 'RIG:clavicle_CTRL_L', mo=True)
	cmds.orientConstraint('clavicle_CTRL_R', 'RIG:clavicle_CTRL_R', mo=True)
	
	cmds.orientConstraint('thigh_CTRL_L', 'RIG:thigh_CTRL_L', mo=True)
	cmds.orientConstraint('thigh_CTRL_R', 'RIG:thigh_CTRL_R', mo=True)
	#FKコントローラーはoldには無いのでコンストレインしないので書かない

	cmds.parentConstraint('hand_CTRL_L', 'RIG:hand_CTRL_L', mo=True)
	cmds.parentConstraint('hand_CTRL_R', 'RIG:hand_CTRL_R', mo=True)
	cmds.parentConstraint('foot_CTRL_L', 'RIG:foot_CTRL_L', mo=True)
	cmds.parentConstraint('foot_CTRL_R', 'RIG:foot_CTRL_R', mo=True)

	cmds.orientConstraint('armfinger_CTRL_L', 'RIG:armfinger_CTRL_L', mo=True)
	cmds.orientConstraint('armfinger_CTRL_R', 'RIG:armfinger_CTRL_R', mo=True)
	cmds.orientConstraint('footfinger_CTRL_L', 'RIG:footfinger_CTRL_L', mo=True)
	cmds.orientConstraint('footfinger_CTRL_R', 'RIG:footfinger_CTRL_R', mo=True)

	cmds.pointConstraint('arm_PV_CTRL_L', 'RIG:arm_PV_CTRL_L', mo=True)
	cmds.pointConstraint('arm_PV_CTRL_R', 'RIG:arm_PV_CTRL_R', mo=True)
	cmds.pointConstraint('leg_PV_CTRL_L', 'RIG:leg_PV_CTRL_L', mo=True)
	cmds.pointConstraint('leg_PV_CTRL_R', 'RIG:leg_PV_CTRL_R', mo=True)

	#↓↓ユニークコントローラー
	#jawあるやつ
	cmds.orientConstraint('jaw_CTRL_C', 'RIG:jaw_CTRL_C', mo=True)

	#noseあるやつ
	#if cmds.objExists('RIG:nose_CTRL_C'):
	#	cmds.orientConstraint('nose_CTRL_C', 'RIG:nose_CTRL_C', mo=True)
	
	#if cmds.objExists('MODEL:brow_JNT_C'):
	#	cmds.orientConstraint('brow_CTRL_C', 'MODEL:brow_JNT_C', mo=True)


	#尻尾あるやつtail作成
	i = 1
	while cmds.objExists('RIG:tail_0' + str(i) + '_CTRL_C'):
		srcCTRL = 'tail_0' + str(i) + '_CTRL_C'
		dstJNT = 'RIG:tail_0' + str(i) + '_CTRL_C'
		cmds.orientConstraint(srcCTRL, dstJNT, mo=True)
		i += 1

	#coneあるやつ（オオカミのみ）
	i = 1
	while cmds.objExists('MODEL:cone_0'+str(i)+'_JNT_C'):
		srcCTRL = 'cone_0' + str(i) + '_CTRL_C'
		dstJNT = 'MODEL:cone_0' + str(i) + '_JNT_C'
		cmds.parentConstraint(srcCTRL, dstJNT, mo=True)
		i += 1

#↓ここからテスト機能
def testAttachForCutter(attachJointList):
	for joint in attachJointList:
		#print(joint)
		if joint == 'root':
			cmds.parentConstraint('root_CTRL_C', 'MODEL:root', mo=True)

		elif cmds.objExists(joint + '_CTRL_C'):
			cmds.parentConstraint(joint + '_CTRL_C', 'MODEL:' + joint + '_JNT_C', mo=True)

		#この条件判定だと_Rしかない場合はさばけない
		#受け取るリストはLR表記がなく重複したものは削除済みのものである
		elif cmds.objExists(joint + '_CTRL_L'):
			cmds.parentConstraint(joint + '_CTRL_L', 'MODEL:' + joint + '_JNT_L', mo=True)
			if cmds.objExists(joint + '_CTRL_R'):
				cmds.parentConstraint(joint + '_CTRL_R', 'MODEL:' + joint + '_JNT_R', mo=True)
		
		#elif cmds.objExists(joint + '_CTRL_R'):念のため残しとく
		#	cmds.parentConstraint(joint + '_CTRL_R', 'MODEL:' + joint + '_JNT_R', mo=True)
		
		else:
			pass

