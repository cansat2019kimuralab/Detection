# GoalDetection
## goal_detection.py
ライブラリ用プログラム
- GoalDetection(imgpath, H_min, H_max, S_thd):ゴール検出用関数  
  ### 引数　 
  - imgpath：画像のpath  
  - H_min: 色相の最小値  
  - H_max: 色相の最大値  
  - S_thd: 彩度の閾値
  ### 戻り値：[max_area, GAP, imgname]
   - GAP:画像の中心とゴールの中心の差（ピクセル）  
   - max_area:ゴールの面積  
   - imgname:処理した画像の名前
---
