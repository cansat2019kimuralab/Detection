import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BME280')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/IM920')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Melting')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/TSL2561')
import time
import serial
import pigpio
import BME280
import BMX055
import IM920
import GPS
import Melting
import Motor
import TSL2561
luxdata=[]
lcount=0
luxmax=200
deltAmax=0.3
presjudge=0
luxjudge=0

def luxjudge():
	luxdata=TSL2561.readLux()
	global lcount
	if luxdata[0]>luxmax or luxdata[1]>luxmax:
		lcount+=1
	elif luxdata[0]<luxmax and luxdata[1]<luxmax:
		lcount=0
	if lcount>4:
		luxjudge=1
		print("luxreleasejudge")
	else:
		luxjudge=0
	print(str(luxdata[0])+":"+str(luxdata[1]))
	return luxjudge

def pressjudge():
	bme280Data=BME280.bme280_read()#?
	PRESS=bme280Data[1]
	deltA=PRESS
	bme280Data=BME280.bme280_read()	#更新
	PRESS=bme280Data[1]
	deltA=PRESS-deltA
	if deltA>deltAmax:
		acount+=1
	elif deltA<deltAmax:
		acount=0
	if acount>2:
		pressjudge=1
		print("presjudge")
	else:
		pressjudge=0
	return pressjudge
