# PyAutoGUIのモジュール
import pyautogui

# プロセスを制御するためにOS周りのモジュール
import os
import subprocess
import sys
import time

# Win32のUI情報と制御用モジュール
from win32 import win32api
from win32 import win32gui

from PIL import ImageGrab
import cv2
import glob
import numpy as np
import mouse
from enum import IntEnum, auto

from minesweeper_solver.square import Square
from minesweeper_solver.square import State
from minesweeper_solver.square import Color
from minesweeper_solver.square import Pos
from minesweeper_solver.field import Field


class GrayState(IntEnum):
    NUMBER = auto()
    MINE = auto()


class MineSweeper():
    def __init__(self):
        self.window_handle = None
        self.rows = 48
        self.cols = 64
        self.window_box = self.__init_window()
        self.field = Field(self.cols, self.rows)
        self.files = []
        for fname in glob.glob('./images/*.png'):
            # 画像を読み込む
            template = self.adjust(cv2.imread(fname), 2, 0)
            base, _ = os.path.splitext(os.path.basename(fname))
            self.files.append((template, base))

    def __init_window(self):
        # 画面サイズの取得
        screen_x, screen_y = pyautogui.size()

        # win32guiを使ってウインドウタイトルを探す
        # Windowのハンドル取得('クラス名','タイトルの一部')で検索クラスがわからなかったらNoneにする
        parent_handle = win32gui.FindWindow(None, "Mine2000")

        # ハンドルIDが取れなかったら、mine2000を起動する
        if parent_handle == 0:
            cmd = 'C:\Program Files (x86)\mine2000 project\mine2000 ver2.2.1\mine2000.exe'
            subprocess.Popen(cmd, shell=True)
            time.sleep(1)
            parent_handle = win32gui.FindWindow(None, "Mine2000")

        if parent_handle == 0:
            sys.exit()

        # ハンドルが取れたら、ウインドウの左上と右下の座標取得と画面のアクティブ化
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

            # スクリーンショット用に座標を調整する
            return (w0 + 4, h0 + 79, w1 - 4, h1)

        raise Exception

    def screenshot(self):
        img = ImageGrab.grab(bbox=(self.window_box))
        img.save('screenshot.png')

    def adjust(self, img, alpha=1.0, beta=0.0):
        # 積和演算を行う。
        dst = alpha * img + beta
        # [0, 255] でクリップし、uint8 型にする。
        return np.clip(dst, 0, 255).astype(np.uint8)

    def update(self):
        time.sleep(0.4)
        self.screenshot()
        time.sleep(0.4)

        # スクリーンショットを読み込んでコントラスト補正する
        image_name = 'screenshot.png'
        # image_name = 'test_screenshot.png'

        image = cv2.imread(image_name)
        img_2 = self.adjust(image, 2, 0)

        for template, base in self.files:
            # 検索対象画像内で画像が一致するかを検索
            result = cv2.matchTemplate(img_2, template, cv2.TM_CCOEFF_NORMED)

            # 一致部分を□で囲む
            th, tw = template.shape[:2]
            threshold = 0.99
            loc = np.where(result >= threshold)
            # print(base)
            for pt in zip(*loc[::-1]):
                self.field[pt[1] // 16][pt[0] // 16].number = 9 if base in ['flag', 'mine'] else None if base == 'gray' else int(base)
                self.field[pt[1] // 16][pt[0] // 16].update_state()
                # print(pt[0]//16, pt[1]//16, self.field[pt[1]//16][pt[0]//16].number, self.field[pt[1]//16][pt[0]//16].state)
                cv2.rectangle(image, pt, (pt[0] + tw, pt[1] + th), (255, 0, 255), 2)

        cv2.imwrite("test.png", image)

    def select_square_pos(self):
        for line in self.field:
            for square in line:
                if square.state == State.NUMBER and square.color == Color.GRAY:
                    around = self.field.get_around(square.pos)
                    gray = around.gray_count
                    mine = around.mine_count

                    # 残りの?マスと数字が同じ
                    if square.number == gray + mine and square.number != 0 and gray != 0:
                        for l in around:
                            for s in l:
                                if s.state == State.GRAY:
                                    return True, GrayState.MINE, s.pos

                    # 数字と同じだけ周りにmineがあるとき
                    if square.number == mine and square.number != 0:
                        for l in around:
                            for s in l:
                                if s.state == State.GRAY:
                                    return True, GrayState.NUMBER, s.pos

        return False, None, None



def on_click(ms):
    # ms.update()
    print(ms.field)
    around = ms.field.get_around(Pos(0, 1))
    print(around)
    print(ms.field.get_square(Pos(0 ,1)))

if __name__ == "__main__":
    minesweeper = MineSweeper()

    minesweeper.update()
    # on_click(minesweeper)
    # exit()
    while True:
        ok, gray_state, pos = minesweeper.select_square_pos()
        if not ok:
            print('None')
        else:
            print(pos, gray_state)
            print(minesweeper.field.get_around(pos))

        minesweeper.update()
        time.sleep(1)
