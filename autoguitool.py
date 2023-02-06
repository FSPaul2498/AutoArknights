import logging
import os
import pyautogui
import time


# 相对转绝对坐标
def rel_to_abs(x, y, region):
    return region[0] + x, region[1] + y


# 移动鼠标
def move_to(x, y, duration=0):
    logging.debug(f"Move to {x}, {y}")
    pyautogui.moveTo(x, y, duration)


# 移动鼠标
def move_rel(dx, dy, duration=0):
    logging.debug(f"Move rel {dx}, {dy}")
    pyautogui.moveRel(dx, dy, duration)


# 移动鼠标
def move_to_loc(path, region=(), recheck=3, duration=0):
    logging.debug(f"Move to {os.path.basename(path)}")
    location = force_loop_locate(path, region=region, recheck=recheck)
    x, y = pyautogui.center(location)
    pyautogui.moveTo(x, y, duration)


# 拖动鼠标
def drag_from_to(x, y, tx, ty, duration=1):
    logging.debug(f"Drag from {x}, {y} to {tx}, {ty}")
    pyautogui.moveTo(x, y)
    pyautogui.dragTo(tx, ty, duration=duration)


# 拖动鼠标
def drag_rel(dx, dy, duration=1):
    logging.debug(f"Drag rel {dx}, {dy}")
    pyautogui.dragRel(dx, dy, duration=duration)


# 点击鼠标
def click(x=-1, y=-1, region=()):
    if x == -1 or y == -1:
        logging.debug("Click in place")
        pyautogui.click()
    elif len(region) > 1:
        logging.debug(f"Click rel at {x}, {y}")
        pyautogui.click(region[0] + x, region[1] + y)
    else:
        logging.debug(f"Click at {x}, {y}")
        pyautogui.click(x, y)


# 尝试点击
def try_click(path, region=(), recheck=0):
    logging.debug(f"Try Click {os.path.basename(path)}")
    try:
        fl_click(path, region=region, recheck=recheck)
    except LocateError:
        return False
    else:
        return True


# 强制点击
def fl_click(path, region=(), recheck=3):
    logging.debug(f"FL Click {os.path.basename(path)}")
    location = force_loop_locate(path, region=region, recheck=recheck)
    x, y = pyautogui.center(location)
    pyautogui.click(x, y)


# 尝试定位
def try_loc(path, region=(), recheck=0):
    logging.debug(f"Try Locate {os.path.basename(path)}")
    try:
        fl_loc(path, region=region, recheck=recheck)
    except LocateError:
        return False
    else:
        return True


# 强制定位
def fl_loc(path, region=(), recheck=3):
    logging.debug(f"FL Locate {os.path.basename(path)}")
    return force_loop_locate(path, region=region, recheck=recheck)


# 强制切换
def fl_toggle(path_0, path_1):
    logging.debug(f"Toggle to {os.path.basename(path_1)}")
    while not try_loc(path_1):
        fl_click(path_0)


# 强制定位实现
def force_loop_locate(path, region=(), recheck=3):
    location = pyautogui.locateOnScreen(path, confidence=0.95, region=region)
    fail_cnt = 0
    while location is None and fail_cnt < recheck:
        time.sleep(1)
        fail_cnt += 1
        logging.debug(f"Locate {os.path.basename(path)} retry for {fail_cnt}")
        location = pyautogui.locateOnScreen(path, confidence=0.9, region=region)
    if location is None:
        raise LocateError(os.path.basename(path))
    else:
        return location


# 无法定位异常
class LocateError(Exception):
    def __init__(self, value):
        self.value = value
