
##PyAutoGUIのモジュール
import pyautogui

##プロセスを制御するためにOS周りのモジュール
import re
import os
import subprocess
import sys
import time
import array

##Win32のUI情報と制御用モジュール
from win32 import win32api
from win32 import win32gui

from PIL import ImageGrab
import cv2
import glob
import numpy as np


def main():
	#実行前の待機(秒)
    time.sleep(1)
    #画面サイズの取得
    screen_x,screen_y = pyautogui.size()
    print(screen_x, screen_y)

    #マウスを(1,1)に移動しておく
    pyautogui.moveTo(1, 1, duration=1)

    #win32guiを使ってウインドウタイトルを探す
    #Windowのハンドル取得('クラス名','タイトルの一部')で検索クラスがわからなかったらNoneにする
    #有名どころで('#32770',"名前を付けて保存")かな
    parent_handle = win32gui.FindWindow(None, "Mine2000")

    #ハンドルIDが取れなかったら、電卓を起動する
    if parent_handle == 0:
        cmd = 'C:\Program Files (x86)\mine2000 project\mine2000 ver2.2.1\mine2000.exe'
        subprocess.Popen(cmd, shell=True)
        time.sleep(3)
        parent_handle = win32gui.FindWindow(None, "Mine2000")

    if parent_handle == 0 :
        print(u"アプリの起動に失敗したみたい、中断します")
        sys.exit()

    #ハンドルが取れたら、ウインドウの左上と右下の座標と画面のアクティブ化
    if parent_handle > 0 :
        w0, h0, w1, h1 = win32gui.GetWindowRect(parent_handle)
        print(u"アプリの座標:"+str(w0)+"/"+str(h0))
        apw_x = w1 - w0
        apw_y = h1 - h0
        print(u"アプリの画面サイズ:"+str(apw_x)+"/"+str(apw_y))

        # ウィンドウをアクティブに持ってくる
        win32gui.SetForegroundWindow(parent_handle)
        time.sleep(0.5)

        # ウィンドウを画面中央に持ってくる
        x_pos = int((screen_x - apw_x) / 2)
        y_pos = int((screen_y - apw_y) / 2)
        win32gui.MoveWindow(parent_handle, x_pos, y_pos, apw_x, apw_y, True)

        #ウインドウの完全な情報を取ってくる、FindWindowで部分一致だったりした場合の補完用
        titlebar = win32gui.GetWindowText(parent_handle)
        classname = win32gui.GetClassName(parent_handle)

        img = ImageGrab.grab(bbox=(w0 + 4, h0 + 79, w1 - 4, h1))
        img.save('screenshot.png')

    while True:
        print(pyautogui.position())
        time.sleep(0.1)


#以下、メインルーチン
if __name__ == "__main__":
    files = glob.glob('./images/*.png')
    image = cv2.imread('screenshot.png')
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    arr = np.full((48,64), None)

    for fname in files:    
        #検索したい画像を読み込む
        template = cv2.imread(fname, 0)
        base, ext = os.path.splitext(os.path.basename(fname))

        #検索対象画像内で画像が一致するかを検索
        result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

        # 一致部分を□で囲む
        th, tw = template.shape[:2]
        threshold = 0.85
        loc = np.where(result >= threshold)
        print(base)
        for pt in zip(*loc[::-1]):
            arr[pt[1]//16][pt[0]//16] = 9 if base in ['gray', 'flag'] else int(base)
            print(pt[0]//16, pt[0]%16, pt[1]//16, pt[1]%16)
            cv2.rectangle(image, pt, (pt[0] + tw, pt[1] + th), (255,0,255), 2)

    for i in arr:
        for j in i:
            print(j if j != None else '%', end=' ')
        print()

    cv2.imwrite("test.png", image)

    # main()