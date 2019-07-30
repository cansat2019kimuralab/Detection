# ParaDetection.py
---
## ParaDetection(imgpath, H_min, H_max, S_thd)
### 引数：  
 - imgpath: 画像のpath  
 - H_min: 色相の最小値  
 - H_max: 色相の最大値  
 - S_thd: 彩度の閾値
### 戻り値：  
 - flug:(0:パラシュートなし、1:パラシュートあり)  
 - area:パラシュートの面積[pixcel]  
 - imgname:処理した画像の名前   
--- 
## ParaJudge(LxThd)
### 引数：  
 - LuxThd: 照度センサの閾値  
### 戻り値：  
 - flug:(0:被パラシュート、1:パラシュートなし)   
---
