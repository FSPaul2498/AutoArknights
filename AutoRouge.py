import autoguitool as auto
import logging
import os
import sys
import time

# Size format: list(left, top, width, height)
# Default Compatible Resolution: 1280 x 720
global full_size, right_half


# 主循环
def main_proc_loop(loop_lmt=1):
    # 调试模式 - 注释关闭
    # debug_mode()
    # 剧场宣传板 检测分辨率
    rouge_home_check()
    # 开始循环游戏
    loop_cnt = 0
    global full_size, right_half
    while loop_cnt < loop_lmt:
        loop_cnt += 1
        logging.warning("========================================================")
        logging.warning(f"Rouge Loop No {loop_cnt} Processing")
        try:
            explore_start()
            map_analyze(full_size)
            while True:
                map_analyze(right_half)
        except UnknownMap:
            explore_leave()
        except SignalLost:
            reverberation()


# 调试模式
def debug_mode():
    logging.warning("==== DEBUG MODE ====")
    global full_size, right_half
    full_size = [320, 151, 1280, 720]
    right_half = list(full_size)
    right_half[2] //= 2
    right_half[0] += right_half[2]
    combat_deploy(510, 345, 400, 320)
    # 调试结束 抛出异常强制退出
    fail_safe("DEBUG MODE: Process Stop")


# 肉鸽首页检测
def rouge_home_check():
    logging.info("Get Game UI size")
    # 打开剧场宣传板
    auto.fl_click("Rouge/Ready/Rouge_Board.png")
    time.sleep(3)
    auto.fl_click("Rouge/Ready/Rouge_Intro_2_Button.png")
    # 定位游戏界面范围
    archive_size = auto.fl_loc("Rouge/Ready/Rouge_Intro_2.png")
    global full_size, right_half
    full_size = list(archive_size)
    # auto.move(size[0], size[1], 0.5)
    # auto.move(size[0] + size[2], size[1], 0.5)
    # auto.move(size[0], size[1] + size[3], 0.5)
    # auto.move(size[0] + size[2], size[1] + size[3], 0.5)
    logging.warning(f"Game UI size detected: {full_size}")
    if full_size[2] != 1280 or full_size[3] != 720:
        logging.critical("Wrong Resolution, Exit")
        logging.critical("Make sure your device or emulator")
        logging.critical("works at 1280x720 and try again.")
        fail_safe("Wrong Resolution")
    # 计算右半屏范围
    right_half = list(full_size)
    right_half[2] //= 2
    right_half[0] += right_half[2]
    auto.fl_click("Rouge/Ready/Rouge_Intro_Close_2.png")


# 开始肉鸽
def explore_start():
    # 检测冷却时间
    if auto.try_loc("Rouge/Start/Explore_Cooldown.png"):
        fail_safe("Wait for rouge cooldown")
        # 继续或开始探索
    if auto.try_click("Rouge/Start/Continue_Explore.png"):
        logging.info("Continue Explore")
        time.sleep(1)
        auto.click()
        time.sleep(1)
        return
    logging.info("Start Explore")
    auto.fl_click("Rouge/Start/Start_Explore.png")
    time.sleep(2)
    # 初始收藏品 - 直面灾厄
    auto.try_click("Rouge/Start/Initial_Collection_Yes.png")
    # 选择分队 - 指挥分队：Unit_A
    # auto.fl_click("Rouge/Start/Unit_A.png")
    # auto.fl_click("Rouge/Start/Yes.png")
    # 选择分队 - 突击战术分队：Unit_E
    # if auto.try_click("Rouge/Start/Unit_E.png"):
    #     pass
    # else:
    #     auto.drag_rel(-640, 0, duration=2)
    #     auto.fl_click("Rouge/Start/Unit_E.png")
    # auto.fl_click("Rouge/Start/Yes.png")
    # 选择分队 - 突击战术分队：Unit_E - 边缘
    auto.fl_click("Rouge/Start/Unit_E_Mini.png")
    auto.click()
    # 选择支援（如果有）
    if auto.try_loc("Rouge/Start/Support_Select.png"):
        auto.try_click("Rouge/Start/Support_Money.png")
        auto.try_click("Rouge/Start/Yes.png")
    # 选择招募组合 - 取长补短：Recruit_C
    auto.fl_click("Rouge/Start/Recruit_C.png")
    auto.fl_click("Rouge/Start/Yes.png")
    # 初始招募 - 近卫 - 山
    auto.fl_click("Rouge/Start/Guard_Ticket.png")
    auto.try_click("Rouge/Start/Recruit_Help_Close.png")
    if not auto.try_click("Rouge/Start/Recruit_Mountain.png", recheck=1):
        auto.fl_click("Rouge/Start/Recruit_Mountain_Skin.png")
    auto.fl_click("Rouge/Start/Recruit_Yes.png")
    auto.try_click("Rouge/Start/Recruit_Skip.png", recheck=3)
    auto.click()
    # 初始招募 - 辅助 - 放弃
    auto.fl_click("Rouge/Start/Supporter_Ticket.png")
    auto.fl_click("Rouge/Start/Recruit_GiveUp.png")
    auto.fl_click("Rouge/Start/Recruit_GiveUp_Yes.png")
    # 初始招募 - 医疗 - 放弃
    auto.fl_click("Rouge/Start/Medic_Ticket.png")
    auto.fl_click("Rouge/Start/Recruit_GiveUp.png")
    auto.fl_click("Rouge/Start/Recruit_GiveUp_Yes.png")
    # 进入古堡
    auto.fl_click("Rouge/Start/Enter_Castle.png")
    time.sleep(3)
    # 配置编队
    logging.info("Edit Squad")
    while not auto.try_loc("Rouge/Start/Squad_Edit.png"):
        pass
    auto.fl_click("Rouge/Start/Squad_Edit.png")
    auto.fl_click("Rouge/Start/Add_Opr.png")
    if not auto.try_click("Rouge/Start/Add_Mountain.png", recheck=1):
        auto.fl_click("Rouge/Start/Add_Mountain_Skin.png")
    auto.fl_click("Rouge/Start/Add_Mountain_Select_Skill2.png")
    auto.fl_click("Rouge/Start/Add_Opr_Yes.png")
    auto.fl_click("Rouge/Start/Back.png")


# 智能分析
def map_analyze(region=()):
    logging.info("Analyze Map")
    # 等待地图加载
    time.sleep(1)
    # 匹配节点
    if auto.try_click("Rouge/Explore/Analyze/Encounter.png", region=region):
        encounter()
    elif auto.try_click("Rouge/Explore/Analyze/Downtime_Recreation.png", region=region):
        downtime_recreation()
    elif auto.try_click("Rouge/Explore/Analyze/Combat_Ops.png", region=region):
        combat_ops()
    elif auto.try_click("Rouge/Explore/Analyze/Emergency_Ops.png", region=region):
        emergency_ops()
    elif auto.try_click("Rouge/Explore/Analyze/Rouge_Trader.png", region=region):
        rouge_trader()
    else:
        raise UnknownMap("Unknown Map Node")


# 作战
def combat_ops():
    logging.info("Combat Ops")
    # 匹配关卡
    if auto.try_loc("Rouge/Explore/Analyze/Combat_LiPaoXiaoDui.png"):
        combat_li_pao_xiao_dui()
    elif auto.try_loc("Rouge/Explore/Analyze/Combat_SiDou.png"):
        combat_si_dou()
    elif auto.try_loc("Rouge/Explore/Analyze/Combat_XunShouXiaoWu.png"):
        combat_xun_shou_xiao_wu()
    elif auto.try_loc("Rouge/Explore/Analyze/Combat_YiWai.png"):
        combat_yi_wai()
    elif auto.try_loc("Rouge/Explore/Analyze/Combat_YuChongWeiBan.png"):
        combat_yu_chong_wei_ban()


# 紧急作战
def emergency_ops():
    logging.info("Emergency Ops")
    logging.warning("emergency_ops in progress")
    logging.warning("Using normal combat_ops() temporary")
    combat_ops()


# 作战：礼炮小队
def combat_li_pao_xiao_dui():
    logging.info("Combat Li Pao Xiao Dui")
    combat_start()
    while not auto.try_loc("Rouge/Explore/Combat/LPXD/Cost.png"):
        pass
    combat_deploy(510, 345, 400, 320)
    time.sleep(80)
    combat_end()


# 作战：礼炮小队
def combat_si_dou():
    logging.info("Combat Si Dou")
    combat_start()
    while not auto.try_loc("Rouge/Explore/Combat/SD/Cost.png"):
        pass
    combat_deploy(435, 440, 295, 425)
    time.sleep(80)
    combat_end()


# 作战：驯兽小屋
def combat_xun_shou_xiao_wu():
    logging.info("Combat Xun Shou Xiao Wu")
    combat_start()
    while not auto.try_loc("Rouge/Explore/Combat/XSXW/Cost.png"):
        pass
    combat_deploy(1030, 330, 970, 380)
    time.sleep(65)
    combat_end()


# 作战：意外
def combat_yi_wai():
    logging.info("Combat Yi Wai")
    combat_start()
    while not auto.try_loc("Rouge/Explore/Combat/YW/Cost.png"):
        pass
    combat_deploy(710, 320, 640, 320)
    time.sleep(85)
    combat_end()


# 作战：与虫为伴
def combat_yu_chong_wei_ban():
    logging.info("Combat Yu Chong Wei Ban")
    combat_start()
    while not auto.try_loc("Rouge/Explore/Combat/YCWB/Cost.png"):
        pass
    combat_deploy(580, 360, 510, 360)
    time.sleep(75)
    combat_end()


# 作战开始
def combat_start():
    logging.info("Combat Start")
    # 进入作战
    auto.fl_click("Rouge/Explore/Analyze/Ops_Enter.png")
    auto.fl_click("Rouge/Explore/Analyze/Ops_Start.png")
    if auto.try_loc("Rouge/Explore/Combat/Empty_Squad_Warn.png"):
        fail_safe("Empty Squad Before Combat")
    time.sleep(5)


# 作战部署
def combat_deploy(dp_x, dp_y, slc_x, slc_y):
    logging.info("Combat Deploy")
    # 相对转绝对坐标运算
    global full_size
    speed_x, speed_y = auto.rel_to_abs(1100, 50, full_size)
    opr_x, opr_y = auto.rel_to_abs(1220, 660, full_size)
    dp_x, dp_y = auto.rel_to_abs(dp_x, dp_y, full_size)
    slc_x, slc_y = auto.rel_to_abs(slc_x, slc_y, full_size)
    skl_x, skl_y = auto.rel_to_abs(850, 400, full_size)
    time.sleep(1)
    while not auto.try_loc("Rouge/Explore/Combat/Ready_Deploy.png"):
        auto.click(opr_x, opr_y)
    # 拖动到目标位置
    auto.drag_from_to(opr_x, opr_y, dp_x, dp_y, duration=3)
    # 选择朝向
    auto.drag_rel(+200, 0)
    # 开启二倍速
    auto.click(speed_x, speed_y)
    # 等待技能CD
    time.sleep(1.5)
    # 开启技能
    auto.click(slc_x, slc_y)
    auto.click(skl_x, skl_y)


# 作战结束
def combat_end():
    logging.info("Combat End")
    # 检查通过状态
    while not auto.try_loc("Rouge/Explore/Combat/End/Success.png"):
        time.sleep(1)
        if auto.try_click("Rouge/Explore/Combat/End/Signal_Lost.png"):
            logging.error("Signal Lost")
            time.sleep(5)
            raise SignalLost("Signal Lost")
        time.sleep(1)
    time.sleep(5)
    auto.try_click("Rouge/Explore/Combat/End/Success.png")
    time.sleep(3)
    # 拿走源石锭
    auto.try_click("Rouge/Explore/Combat/End/Take_Money.png")
    while auto.try_loc("Rouge/Explore/Combat/End/Take_Money.png"):
        auto.click()
        time.sleep(1)
    # 拿走道具
    while auto.try_loc("Rouge/Explore/Combat/End/Take_Item.png"):
        auto.click()
        time.sleep(1)
    # 不要了，走了
    if auto.try_click("Rouge/Explore/Combat/End/Leave_1.png"):
        pass
    elif auto.try_click("Rouge/Explore/Combat/End/Leave_2Y.png"):
        pass
    elif auto.try_click("Rouge/Explore/Combat/End/Leave_2B.png"):
        pass
    elif auto.try_click("Rouge/Explore/Combat/End/Leave_3.png"):
        pass
    else:
        auto.move_rel(+800, 0)
        auto.drag_rel(-300, 0, duration=1)
        if auto.try_click("Rouge/Explore/Combat/End/Leave_4.png"):
            pass
        else:
            fail_safe("Can't Find Combat Success Leave Option")
    auto.fl_click("Rouge/Explore/Combat/End/Leave_Yes.png")


# 不期而遇
def encounter():
    logging.info("Encounter")
    # 进入不期而遇
    auto.fl_click("Rouge/Explore/Encounter/Enter.png")
    while not auto.try_loc("Rouge/Explore/Encounter/Squad_Edit.png"):
        auto.click()
    time.sleep(1)
    # 匹配选项
    if auto.try_loc("Rouge/Explore/Encounter/Option_Hope.png"):
        auto.try_click("Rouge/Explore/Encounter/Option_Hope.png")
    elif auto.try_loc("Rouge/Explore/Encounter/Option_Leave.png"):
        auto.try_click("Rouge/Explore/Encounter/Option_Leave.png")
    elif auto.try_loc("Rouge/Explore/Encounter/Option_Money.png"):
        auto.try_click("Rouge/Explore/Encounter/Option_Money.png")
    elif auto.try_loc("Rouge/Explore/Encounter/Option_Sleep.png"):
        auto.try_click("Rouge/Explore/Encounter/Option_Sleep.png")
    else:
        fail_safe("Unknown Encounter Option")
    # 确认并离开
    auto.click()
    time.sleep(3)
    auto.click()


# 幕间余兴
def downtime_recreation():
    logging.info("Downtime Recreation")
    logging.info("Using encounter() temporary")
    encounter()


# 诡异行商
def rouge_trader():
    logging.info("Rouge Trader")
    # 进入行商
    auto.fl_click("Rouge/Explore/Trader/Enter.png")
    # 进入投资系统
    if not auto.try_loc("Rouge/Explore/Trader/Invest_Main_999.png", recheck=3):
        if auto.try_loc("Rouge/Explore/Trader/Invest_Main.png", recheck=3):
            auto.fl_click("Rouge/Explore/Trader/Invest_Main.png")
            auto.fl_click("Rouge/Explore/Trader/Invest_Entrance.png")
            # 开始投资
            auto.try_click("Rouge/Explore/Trader/Invest_Yes.png")
            while not (auto.try_loc("Rouge/Explore/Trader/Invest_Limited.png")
                       or auto.try_loc("Rouge/Explore/Trader/No_Money.png")
                       or auto.try_loc("Rouge/Explore/Trader/Invest_1000.png")):
                auto.click()
            auto.fl_click("Rouge/Explore/Trader/Invest_Leave_1.png")
            auto.click()
    # 退出行商
    auto.fl_click("Rouge/Explore/Trader/Leave_Trader_1.png")
    auto.click()
    time.sleep(3)


# 退出肉鸽
def explore_leave():
    logging.info("Leave Explore")
    # 退出肉鸽地图
    while not auto.try_loc("Rouge/Leave/Leave.png"):
        pass
    auto.fl_click("Rouge/Leave/Leave.png")
    # 放弃探索
    auto.fl_click("Rouge/Leave/GiveUp_Explore.png")
    auto.fl_click("Rouge/Leave/GiveUp_Explore_Yes.png")
    reverberation()


# 凋零残响
def reverberation():
    logging.info("Reverberation")
    auto.fl_loc("Rouge/Leave/End_Step_Title.png")
    time.sleep(1)
    auto.fl_click("Rouge/Leave/End_Step_1.png")
    time.sleep(6)
    auto.fl_click("Rouge/Leave/End_Step_2.png")
    while not auto.try_loc("Rouge/Ready/Rouge_Board.png"):
        auto.click()


# 意外情况处理
def fail_safe(msg="unknown error(s)"):
    logging.critical("AutoRouge fail_safe triggered")
    raise UnknownError(msg)


# 战斗失败异常
class SignalLost(Exception):
    def __init__(self, value):
        self.value = value


# 地图识别异常
class UnknownMap(Exception):
    def __init__(self, value):
        self.value = value


# 未知情况异常
class UnknownError(Exception):
    def __init__(self, value):
        self.value = value


# 主函数
if __name__ == "__main__":
    # 参数1 识别循环次数
    if len(sys.argv) > 1:
        try:
            loop_times = int(sys.argv[1])
        except ValueError:
            print("=====================================")
            print(" Unrecognized loop times parameter!")
            print(" loop times must be an Integer value")
            print("=====================================")
            time.sleep(1)
            raise
        print(f"Loop time(s): {loop_times}")
    else:
        loop_times = 1
        print(f"Loop time(s): 1 (Default)")
    # 参数2 识别日志模式
    if len(sys.argv) > 2:
        match sys.argv[2]:
            case "DEBUG":
                level = logging.DEBUG
            case "INFO":
                level = logging.INFO
            case "WARNING":
                level = logging.WARNING
            case "ERROR":
                level = logging.ERROR
            case "CRITICAL":
                level = logging.CRITICAL
            case _:
                print("=====================================")
                print(" Unrecognized log mode parameter!")
                print(" log mode must be one of following")
                print(" DEBUG INFO WARNING ERROR CRITICAL")
                print("=====================================")
                time.sleep(1)
                raise ValueError(sys.argv[2])
        print(f"Logging module: {sys.argv[2]} MODE")
    else:
        level = logging.INFO
        print("Logging module: INFO MODE (Default)")
    # 参数3+ 全部忽略
    if len(sys.argv) > 3:
        print("Too many parameters")
        print("Extra parameters will be ignored")
    # 设定基本操作间隔
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)-8s : %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    auto.pyautogui.PAUSE = 1
    time.sleep(1)
    # 倒计时执行
    countDown = list(range(3))[::-1]
    logging.warning("=====================================")
    logging.warning("Move your mouse pointer to (0,0) for Emergency EXIT !")
    for i in countDown:
        logging.warning(f"AutoRouge will start in {i + 1} sec(s)...")
        time.sleep(1)
    logging.warning("=====================================")
    # 开始执行
    try:
        main_proc_loop(loop_times)
    except auto.pyautogui.FailSafeException:
        logging.critical("=====================================")
        logging.critical("   PyAutoGUI fail-safe triggered   ")
        logging.critical("=====================================")
    except auto.LocateError as e:
        logging.critical("=====================================")
        logging.critical("   Can't locate target picture:   ")
        logging.critical(f"   {e.value}")
        logging.exception(e)
        logging.critical("=====================================")
    except UnknownError as e:
        logging.critical("=====================================")
        logging.critical("   Can't handle unknown error:    ")
        logging.critical(f"   {e.value}")
        logging.exception(e)
        logging.critical("=====================================")
    except KeyboardInterrupt as e:
        logging.critical("=====================================")
        logging.critical("   Keyboard Interrupt by Ctrl C  ")
        logging.exception(e)
        logging.critical("=====================================")
    else:
        logging.warning("=====================================")
        logging.warning("     All Done     ")
        logging.warning("=====================================")
    finally:
        logging.critical("===== PROGRAM HAS STOPPED =====")
