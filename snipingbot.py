import numpy as np
import win32api, win32con
import time
import random
import pyautogui
import keyboard

#inc bid = 1885,603
#dec bid = 1124,603
#inc buy = 1885,912
#dec sell = 1124,912
#search = 1728,986
#setbuy = 1514,912

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def resetprice():
    setbuy = (1514,912)
    click(1514,912)
    win32api.keybd_event(0x08, 0,0,0)
    click(1456,759) # black space to clear

time.sleep(2)
def sniping():
    while keyboard.is_pressed('q') == False:
        time.sleep(0.1)
        click(970, 686) # inc bid
        time.sleep(0.1)
        click(1398,925) # search
        time.sleep(0.5) # should realistically make a function to check if there is a player available
        click(1549, 864) # buy now
        time.sleep(0.25)
        click(959, 604) # ok
        click(155,199) # back
        time.sleep(0.5) 
        click(1763,394)
        pyautogui.dragTo(1763,576, 0.5, button='left')
        click(393,686)
        time.sleep(0.1)
        click(1398,925) # search
        time.sleep(0.5) # should realistically make a function to check if there is a player available
        click(1549, 864) # buy now
        time.sleep(0.25)
        click(959, 604) # ok
        click(155,199) # back
        time.sleep(0.5) 
        click(1763,394)
        pyautogui.dragTo(1763,576, 0.5, button='left')
    
    return

sniping()