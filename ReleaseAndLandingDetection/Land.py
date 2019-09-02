import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BME280')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/IM920')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/TSL2561')
import time
import serial
import pigpio
import BME280
import BMX055
import IM920
import GPS
import math
import traceback
import Capture
import cv2

Pcount=0
GAcount=0
Mcount=0
plcount=0
bme280Data=[0.0,0.0,0.0,0.0]
gpsData=[0.0,0.0,0.0,0.0,0.0,0.0]
bmxData=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
presslandjudge=0
photolandjudge=0
photopath = 		"/home/pi/photo/photo"
photoName =			""

def pressdetect(presslandThd):
	try:
		global Pcount
		global bme280Data
		presslandjudge=0
		secondlatestPRESS=bme280Data[1]
		bme280Data=BME280.bme280_read()	#更新
		latestPRESS=bme280Data[1]
		deltP=abs(latestPRESS-secondlatestPRESS)
		if bme280Data==[0.0,0.0,0.0,0.0]:
			print("BMEerror!")
			presslandjudge=2
		elif 0.0 in bme280Data:
			print("BMEerror!")
			presslandjudge=2
		elif deltP<presslandThd:
			Pcount+=1
			if Pcount>4:
				presslandjudge=1
				#print("preslandjudge")
		else:
			Pcount=0
			presslandjudge=0
		#print(str(latestPRESS)+"	:	"+"delt	"+str(deltP))
		#print("Pcount	"+str(Pcount))
	except:
		print(traceback.format_exc())
		Pcount = 0
		presslandjudge = 2
	finally:
		return presslandjudge,Pcount

def gpsdetect():  #使わない
	global GAcount
	global gpsData
	gpsjudge = 0
	secondlatestGheight=gpsData[3]
	gpsData=GPS.readGPS()
	latestGheight=gpsData[3]
	deltH=abs(float(latestGheight)-float(secondlatestGheight))
	#print(latestGheight)
	#3秒ごとに判定
	if deltH<deltHmax:
		GAcount+=1
		if GAcount>4:
			gpsjudge=1
			#print("GPSlandjudge")
	elif deltH>deltHmax :
		GAcount=0

	else:
		gpsjudge=0
	#print("GAcount"+str(GAcount))
	return gpsjudge,GAcount

def bmxdetect(gyrolandThd):
	global Mcount
	global bmxData
	gyrolandjudge = 0
	try:
		bmxData=BMX055.bmx055_read()
		gyrox=math.fabs(bmxData[3]) #using gyro
		gyroy=math.fabs(bmxData[4])
		gyroz=math.fabs(bmxData[5])
		#print(bmxData)

		if gyrox < gyrolandThd and gyroy < gyrolandThd and gyroz < gyrolandThd: 
			Mcount+=1
			if Mcount > 4:
				gyrolandjudge=1
		else:
			Mcount=0
			gyrolandjudge=0
	except:
		print(traceback.format_exc())
		Mcount = 0
		gyrolandjudge = 2
	finally:
		return gyrolandjudge,Mcount

def photolanddetect(photolandThd):  
	global plcount
	#global photoName
	photo = ""
	photopath = "/home/pi/photo/photo"
	try:
		img_1=cv2.imread(photoName)
		photo = Capture.Capture(photopath)
		img_2=cv2.imread(photo)
		hist_g_1 = cv2.calcHist([img_1],[0],None,[256],[0,256])
		hist_g_2 = cv2.calcHist([img_2],[0],None,[256],[0,256])
		comp_hist = cv2.compareHist(hist_g_1, hist_g_2, cv2.HISTCMP_CORREL)
		print(str(comp_hist))
		photoName=photo
		if comp_hist > photolandThd:
			plcount += 1
			if plcount > 4:
				photolandjudge=1
			else:
				photolandjudge=0
		else:
			plcount=0
			photolandjudge=0
	except:
		print(traceback.format_exc())
		plcount = 0
		photolandjudge = 0
	
	return photolandjudge,plcount


		

if __name__ == "__main__":
	photopath = "/home/pi/photo/photo"
	photoName = ""
	photolandThd=0.3
	try:
		while photolandjudge==0:
			photolandjudge,plcount = photolanddetect(photolandThd)
			print("plcount "+str(plcount))
			print("judge   "+str(photolandjudge))
			time.sleep(1)
	except:
		print(traceback.format_exc())
