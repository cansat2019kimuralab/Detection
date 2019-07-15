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

t = 1	#待機時間
x = 61	#放出判定の時間
y = 60	#着地判定の時間
z = 120	#走行の時間


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
	with open('log/releaseLog.txt', 'a') as f:
		pass
	with open('log/landingLog.txt', 'a') as f2:
		pass
	with open('log/runningLog.txt', 'a') as f3:
		pass

def close():
	GPS.closeGPS()

if __name__ == "__main__":
	print("Program Start  {0}".format(time.time()))

	try:
		setup()
		time.sleep(t)
		bme280Data=BME280.bme280_read()
		lcount=0
		acount=0
		Pcount=0
		GAcount=0
		luxmax=300
		deltAmax=0.3
		deltPmax=0.05
		deltHmax=5

		tx1 = time.time()
		tx2 = tx1

		#溶断まで
		print("Releasing Judgement Program Start  {0}".format(time.time()))

		with open('log/releaseLog.txt', 'a') as f:
			f.write("\n")
			#ループx
			while(1):

				#tx2を更新
				tx2=time.time()
				#放出判定(照度センサ)
				luxdata=TSL2561.readLux()
				#f.write(str(luxdata[0])+":"+str(luxdata[1]))
				print("lux1: "+str(luxdata[0])+" "+"lux2: "+str(luxdata[1]))
				f.write(str(luxdata[0])+"	"+str(luxdata[1])+"		")

				print(lcount)
				print(acount)

				if luxdata[0]>luxmax or luxdata[1]>luxmax:
					lcount+=1
				elif luxdata[0]<luxmax and luxdata[1]<luxmax:
					lcount=0
				if lcount>4:
					luxreleasejudge=True
					print("luxreleasejudge")
				else:
					luxreleasejudge=False
				#放出判定（気圧センサ）
					PRESS=bme280Data[1]
					deltA=PRESS
					bme280Data=BME280.bme280_read()	#更新
					PRESS=bme280Data[1]
					deltA=PRESS-deltA
					#f.write("P0:P1"+str(P0)+":"+str(P1))
					print(str(PRESS))
					print(str(deltA))
					time.sleep(2)
					#3秒前の値と比較
					#高度差が式一以上でacout+=1
					if deltA>deltAmax:
						acount+=1
					elif deltA<deltAmax:
						acount=0
					if acount>2:
						presreleasejudge=True
						print("presjudge")

					else:
						presreleasejudge=False
				f.write(str(deltA)+"   "+str(PRESS)+"\t")
				f.write("\n")

				if luxreleasejudge or presreleasejudge:
					ty1=time.time()
					ty2=ty1
					print("RELEASE!")
					f.write("release")
					pi.write(22,0)
					bme280Data=BME280.bme280_read()
					gpsData = GPS.readGPS()
					#ループyのタイムアウト判定
					with open('log/landingLog.txt', 'a') as f2:
						f.write("\n")
						while(ty2-ty1<=y):
							ty2=time.time()
							#気圧判定
							PRESS=bme280Data[1]
							deltP=PRESS
							bme280Data=BME280.bme280_read()	#更新
							PRESS=bme280Data[1]
							deltP=deltP-PRESS
							f2.write(str(deltP))#+":"+str(PRESS)+ "\t")
							f2.write("\n")
							print(deltP)
							print("Pcount:"+str(Pcount))
							if abs(deltP)<deltPmax:
								Pcount+=1
							elif abs(deltP)>deltPmax:
								Pcount=0
							if Pcount>4:
								preslandjudge=True
								print("preslandjudge")
							else:
								preslandjudge=False

							#GPS高度判定
							Gheight=gpsData[4]
							deltH=Gheight
							gpsData=GPS.readGPS()
							Gheight=gpsData[4]
							deltH=deltH-Gheight
							print(Gheight)
							#3秒ごとに判定
							time.sleep(3)
							if abs(deltH)<deltHmax:
								GAcount+=1
							elif abs(deltH)>deltHmax :
								GAcount=0
							if GAcount>4:
								GPSlandjudge=True
								print("GPSlandjudge")
							else:
								GPSlandjudge=False


							#気圧と高度が変化していたら撮影
							if not preslandjudge and not GPSlandjudge:
								print("satueinow")
								#撮影
							#両方に変化なければ着地、ループyを抜ける
							elif preslandjudge and  GPSlandjudge:
								break
							else:
								print("Landingjudgement now")
					#ループy中でbreakが起きなければ続行、起きたら全体も抜ける
						else:
							print("THE ROVER HAS LANDED.  {0}".format(time.time()))
							f2.write("land")
							break
						print("THE ROVER HAS LANDED.  {0}".format(time.time()))
						f2.write("land")
						break
				#放出されず、かつループxでタイムアウト
				elif tx2-tx1>=x:
					tz1=time.time()
					tz2=tz1
					print("X timeout")
					#ループzのタイムアウト判定
					while(tz2-tz1<=z):
						tz2=time.time()
						PRESS=bme280Data[1]
						deltP=PRESS
						bme280Data=BME280.bme280_read()	#更新
						PRESS=bme280Data[1]
						deltP=deltP-PRESS
						print(PRESS)
						#3秒ごとに判定.
						time.sleep(3)
						if abs(deltP)<deltPmax:
							Pcount+=1
						elif abs(deltP)>deltPmax:
							Pcount=0
						if Pcount>5:
							preslandjudge=True
							print("preslandjudge")
						else:
							preslandjudge=False
						#気圧が変化しなければループzを抜ける
						if  preslandjudge:
							break
					#ループz中でbreakが起きなければ続行、起きたら全体も抜ける
					else:
						break
					break
#溶断へ
		print("outcasing")
		close()
	except KeyboardInterrupt:
		close()
		print("\r\nKeyboard Intruppted")
	except Exception as e:
		close()
		IM920.Send("Error Occured")
		IM920.Send("Program Stopped")
		print(e.message) 