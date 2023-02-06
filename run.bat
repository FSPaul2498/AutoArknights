@echo off
chcp 65001
title AutoArknights - AutoRouge.py
echo 模拟控制需要申请管理员权限
echo 请在弹出窗口中选择"是"以授权继续执行
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cls
echo PATH: %~dp0
echo Python Interpreter: .\venv\Scripts\python.exe
cd /d %~dp0
pause
.\venv\Scripts\python.exe AutoRouge.py 100 INFO
rem .\venv\Scripts\python.exe AutoRouge.py [loop_times] [log_mode]
rem [loop_times]: 循环次数，仅限正整数，留空默认为1次
rem  [log_mode] : 日志模式，仅限DEBUG、INFO、WARNING、ERROR、CRITICAL，留空默认为INFO
pause