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
import TSL2561
import math
import traceback
deltPmax=0.1
deltHmax=5
gyromax=20
Pcount=0
GAcount=0
Mcount=0
bme280Data=[0.0,0.0,0.0,0.0]
gpsData=[0.0,0.0,0.0,0.0,0.0,0.0]
bmxData=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
presslandjudge=0

def pressdetect():
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
	elif deltP<deltPmax:
		Pcount+=1
		if Pcount>4:
			preslandjudge=1
			#print("preslandjudge")
	else:
		Pcount=0
		presslandjudge=0
	#print(str(latestPRESS)+"	:	"+"delt	"+str(deltP))
	#print("Pcount	"+str(Pcount))
	return presslandjudge,Pcount

def gpsdetect():
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

def bmxjudetect():
	global Mcount
	global bmxData
	magnetlandjudge = 0
	bmxData=BMX055.bmx055_read()
	gyrox=math.fabs(bmxData[3]) #using gyro
	gyroy=math.fabs(bmxData[4])
	gyroz=math.fabs(bmxData[5])
	print(bmxData)


	if gyrox < gyromax and gyroy < gyromax and gyroz < gyromax: 
		Mcount+=1
		if Mcount > 9:
			magnetlandjudge=1
	else:
		Mcount=0
		magnetlandjudge=0
	return magnetlandjudge,Mcount

if __name__ == "__main__":
	try:
		Mcount,magnetlandjudge = bmxjudge()
		while magnetlandjudge==0:
			Mcount,magnetlandjudge = bmxjudge()
			print("Mcount "+str(Mcount))
			time.sleep (1)
	except:
		print(traceback.format_exc())
