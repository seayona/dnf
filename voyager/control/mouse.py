import pyautogui

pyautogui.FAILSAFE = False


def moveTo(x, y):
    if x == 0 and y == 0:
        return
    pyautogui.moveTo(x, y, 0.2)


def click(x, y):
    pyautogui.click(x, y)


if __name__ == '__main__':
    moveTo(0, 0)
    click(0, 0)
