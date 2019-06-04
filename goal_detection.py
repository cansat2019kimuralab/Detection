#! coding: Shift_JIS

import cv2
import numpy as np
import sys

#入力画像の取得
img = cv2.imread('target18.jpg')
img = cv2.resize(img,(640,480))
Height, Width =img.shape[:2]
s1 = (Height,Width)
cv2.imshow('元画像',img)

#入力画像のコピー(フィルタ用)
img_gauss=img.copy()

#フィルタ処理(ぼかし)
img_gauss = cv2.GaussianBlur(img_gauss, (9, 9), 3)

#BGR->HSV
img_HSV = cv2.cvtColor(img_gauss,cv2.COLOR_BGR2HSV)

#H,Sの範囲設定
lower_red = np.array([0,80,0])
upper_red = np.array([10,255,255])

#HSVのH,Sからマスク画像生成
mask1 = cv2.inRange(img_HSV, lower_red, upper_red)
cv2.imshow('色相彩度、論理積後画像', mask1)

#輪郭処理
contours, hierarchy = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#最大面積
max_area = 0
max_area_contour = -1
for j in range(0,len(contours)):
	area = cv2.contourArea(contours[j])
	if max_area < area:
		max_area = area
		max_area_contour = j

cnt = contours[max_area_contour]
#重心計算
M = cv2.moments(cnt)
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
print("重心は(",cx,",",cy,")")

#最大面積の抽出
print('最大面積は',max_area)		

#goal検出不可
if max_area <= 100:
	print( "コーンが検出されませんでした。" )
	cv2.waitKey()
	cv2.destroyAllWindows()
	sys.exit()
#goal判定
if max_area >= 80000:
	print( "ゴール!!!!!!!!" )
	cv2.waitKey()
	cv2.destroyAllWindows()
	sys.exit()
		
#傾いた矩形
rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
img = cv2.drawContours(img,[box],0,(0,0,255),2)

#rotated_center = rect.center()
img = cv2.circle(img,(cx,cy), 5, (255,0,0), -1, cv2.LINE_AA)						#中心描画


#垂直な矩形
x,y,w,h = cv2.boundingRect(cnt)
im = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

#print("画像の中心のx座標は", s1.width/2, "\n")								#画像の中心座標の表
#print("傾いたターゲットのx座標は", rect.center.x ,"\n")				#ターゲットの中心座標の表示

cv2.imshow("ターゲット", img);														#マスク表示
cv2.waitKey()	
cv2.destroyAllWindows()
