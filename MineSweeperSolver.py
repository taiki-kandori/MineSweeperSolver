
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
import mouse


class Field():
    def __init__(self):
        self.window_handle = None
        self.window_box = (None, None, None, None)
        self.arr = np.full((48, 64), None)
        self.files = glob.glob('./images/*.png')

    def set_window_box(self, x0, y0, x1, y1):
        # スクリーンショット用に座標を調整する
        self.window_box = (x0 + 4, y0 + 79, x1 - 4, y1)

    def screenshot(self):
        img = ImageGrab.grab(bbox=(self.window_box))
        img.save('screenshot.png')

    def update_field(self):
        self.screenshot()

        image = cv2.imread('screenshot.png')
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        for fname in self.files:
            #検索したい画像を読み込む
            template = cv2.imread(fname, 0)
            base, ext = os.path.splitext(os.path.basename(fname))

            #検索対象画像内で画像が一致するかを検索
            result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

            # 一致部分を□で囲む
            th, tw = template.shape[:2]
            threshold = 0.85
            loc = np.where(result >= threshold)
            for pt in zip(*loc[::-1]):
                self.arr[pt[1]//16][pt[0]//16] = 9 if base in ['gray', 'flag'] else int(base)
                # print(pt[0]//16, pt[0]%16, pt[1]//16, pt[1]%16)
                cv2.rectangle(image, pt, (pt[0] + tw, pt[1] + th), (255,0,255), 2)

        cv2.imwrite("test.png", image)

    def print_field(self):
        print(np.array2string(self.arr, max_line_width=100, edgeitems=100))


def init_window():
    #画面サイズの取得
    screen_x,screen_y = pyautogui.size()

    #win32guiを使ってウインドウタイトルを探す
    #Windowのハンドル取得('クラス名','タイトルの一部')で検索クラスがわからなかったらNoneにする
    parent_handle = win32gui.FindWindow(None, "Mine2000")

    #ハンドルIDが取れなかったら、mine2000を起動する
    if parent_handle == 0:
        cmd = 'C:\Program Files (x86)\mine2000 project\mine2000 ver2.2.1\mine2000.exe'
        subprocess.Popen(cmd, shell=True)
        time.sleep(1)
        parent_handle = win32gui.FindWindow(None, "Mine2000")

    if parent_handle == 0:
        sys.exit()

    #ハンドルが取れたら、ウインドウの左上と右下の座標取得と画面のアクティブ化
    if parent_handle > 0:
        w0, h0, w1, h1 = win32gui.GetWindowRect(parent_handle)
        apw_x = w1 - w0
        apw_y = h1 - h0

        # ウィンドウをアクティブに持ってくる
        win32gui.SetForegroundWindow(parent_handle)
        time.sleep(0.5)

        # ウィンドウを画面中央に持ってくる
        x_pos = int((screen_x - apw_x) / 2)
        y_pos = int((screen_y - apw_y) / 2)
        win32gui.MoveWindow(parent_handle, x_pos, y_pos, apw_x, apw_y, True)

        return w0, h0, w1, h1

    raise Exception


def on_click(field):
    time.sleep(0.3)
    field.update_field()

    # field.print_field()

#以下、メインルーチン
if __name__ == "__main__":
    field = Field()
    field.set_window_box(*init_window())

    while True:
        if mouse.is_pressed(button=mouse.LEFT):
            while not mouse.is_pressed:
                pass
            on_click(field)
        # time.sleep(0.1)
