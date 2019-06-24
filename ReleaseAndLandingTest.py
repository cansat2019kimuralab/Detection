# -*- coding: utf-8 -*-

import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/IM920')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BME280')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/TSL2561')
import time
import difflib
import pigpio
import serial
import binascii
import IM920
import GPS
import BMX055
import BME280
import Capture
import TSL2561

luxstr = ["lux1", "lux2"]
bme280str = ["temp", "pres", "hum", "alt"]
bmx055str = ["accx", "accy", "accz", "gyrx", "gyry", "gyrz", "dirx", "diry", "dirz"]
gpsstr = ["utctime", "lat", "lon", "sHeight", "gHeight"]

t = 10	#待機時間
x = 10	#放出判定の時間
y = 10	#着地判定の時間
z = 10	#走行の時間

pi=pigpio.pi()

def gpsSend(gpsData):
	IM920.Send('g'+str(gpsData[0]) + ',' + str(gpsData[1]) + ',' + str(gpsData[2]) + ',' + str(gpsData[3]) + ',' + str(gpsData[4]) + ',' + str(gpsData[5]))

def setup():
	pi.set_mode(22,pigpio.OUTPUT)
	pi.write(22,0)
	pi.write(17,0)
	time.sleep(1)
	BME280.bme280_setup()
	BME280.bme280_calib_param()
	BMX055.bmx055_setup()
	GPS.openGPS()
	with open('/log/releaseLog.txt', 'w'):
		pass
	with open('/log/runningLog.txt', 'w'):
		pass
	with open('/log/landingLog.txt', 'w'):
		pass

def close():
	GPS.closeGPS()

if __name__ == "__main__":
	print("Program Start  {0}".format(time.time()))
	try:
		setup()
		time.sleep(t)

        tx1 = time.time()
		tx2 = tx1

        #溶断まで
        #ループx
        while(1):
            #放出判定
            if 光判定 or 気圧判定:
                ty1=time.time()
                ty2=ty1
                #ループyのタイムアウト判定
                while(ty2-ty1<=y):
                    #気圧と高度が変化していたら撮影
                    if 気圧変化 and 高度変化:
                        撮影
                    #片方に変化なければ着地、ループyを抜ける
                    else:
                        break
                #ループy中でbreakが起きなければ続行、起きたら全体も抜ける
                else:
                    continue
                break
            #放出されず、かつループxでタイムアウト
            else if tx2-tx1>=x:
                tz1=time.time()
                tz2=tz1
                #ループzのタイムアウト判定
                while(tz2-tz1<=z):
                    #気圧が変化しなければループzを抜ける
                    if not 気圧変化:
                        break
                #ループz中でbreakが起きなければ続行、起きたら全体も抜ける
                else:
                    continue
                break

        #溶断へ


	except KeyboardInterrupt:
		close()
		print("\r\nKeyboard Intruppted")
	except Exception as e:
		close()
		IM920.Send("Error Occured")
		IM920.Send("Program Stopped")
		print(e.message)