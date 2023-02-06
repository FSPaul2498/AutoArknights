import autoguitool as auto
import logging
import time


# 主循环
def main_proc_loop():
    loop_cnt = 0
    while loop_cnt < 14:
        loop_cnt += 1
        logging.warning("========================================================")
        logging.warning(f"Combat Loop No {loop_cnt} Processing")
        try:
            NormalCombat()
        except RecoverSanity as e:
            logging.warning("=====================================")
            logging.warning("   Recover Sanity    ")
            logging.warning(f"   {e.value}")
            logging.warning("=====================================")
        except LackSanity as e:
            logging.critical("=====================================")
            logging.critical("   Lack Sanity    ")
            logging.critical(f"   {e.value}")
            logging.critical("=====================================")
            raise


# NormalCombat (CE-6 1-7)
def NormalCombat():
    # 选择关卡
    while not auto.try_loc("Combat/Sanity.png"):
        auto.try_click("Combat/1-7.png")
    # 打开代理
    auto.fl_toggle("Combat/Auto_Off.png", "Combat/Auto_On.png")
    # 开始行动
    auto.fl_click("Combat/Ops_Start_1.png")
    time.sleep(2)
    if auto.try_click("Combat/Ops_Start_2.png"):
        pass
    elif auto.try_loc("Combat/Recover_Drug.png"):
        if auto.try_loc("Combat/Drug_Yellow.png"):
            auto.try_click("Combat/Recover_Yes.png")
            raise RecoverSanity("Recover with Drugs: Yes (Yellow Drug)")
        else:
            raise LackSanity("Recover with Drugs: False")
    elif auto.try_loc("Combat/Recover_Originium.png"):
        raise LackSanity("Recover with Originium: False")
    else:
        raise UnknownError("Unknown Error")
    time.sleep(70)
    # 行动结束
    while not auto.try_loc("Combat/LV_120.png"):
        pass
    time.sleep(3)
    auto.fl_click("Combat/LV_120.png")


# 补充理智异常
class RecoverSanity(Exception):
    def __init__(self, value):
        self.value = value


# 缺少理智异常
class LackSanity(Exception):
    def __init__(self, value):
        self.value = value


# 未知情况异常
class UnknownError(Exception):
    def __init__(self, value):
        self.value = value


# 主函数
if __name__ == "__main__":
    # 设定日志模式 基本操作间隔
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)-8s : %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    auto.pyautogui.PAUSE = 1
    time.sleep(1)
    # 倒计时执行
    countDown = list(range(3))[::-1]
    logging.warning("=====================================")
    logging.warning("Move your mouse pointer to (0,0) for Emergency EXIT !")
    for i in countDown:
        logging.warning(f"AutoCombat will start in {i + 1} sec(s)...")
        time.sleep(1)
    logging.warning("=====================================")
    # 开始执行
    try:
        main_proc_loop()
    except auto.pyautogui.FailSafeException:
        logging.critical("=====================================")
        logging.critical("   PyAutoGUI fail-safe triggered   ")
        logging.critical("=====================================")
    except auto.LocateError as e:
        logging.critical("=====================================")
        logging.critical("   Can't locate target picture:   ")
        logging.critical(f"   {e.value}")
        logging.critical("=====================================")
    except UnknownError as e:
        logging.critical("=====================================")
        logging.critical("   Can't handle unknown error:    ")
        logging.critical(f"   {e.value}")
        logging.critical("=====================================")
    except KeyboardInterrupt:
        logging.critical("=====================================")
        logging.critical("   KeyboardInterrupt by PyCharm   ")
        logging.critical("=====================================")
    else:
        logging.warning("=====================================")
        logging.warning("     All Done     ")
        logging.warning("=====================================")
    finally:
        logging.critical("===== PROGRAM HAS STOPPED =====")
