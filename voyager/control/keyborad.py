import pyautogui
import win32api
from pyautogui._pyautogui_win import keyboardMapping


def press(key):
    pyautogui.press(key)


def keyUp(key):
    pyautogui.keyUp(key)


def keyDown(key):
    pyautogui.keyDown(key)


def hold(key):
    pyautogui.hold(key)


def hotkey(key1, key2):
    pyautogui.hotkey(key1, key2)


def typeWrite(message):
    pyautogui.typewrite(message)


def onKeyPressed(key):
    """
    按键监听，全局有效
    :param key: 按键字符，例如：f8
    """
    if win32api.GetAsyncKeyState(keyboardMapping[key]):
        return True
    return False
