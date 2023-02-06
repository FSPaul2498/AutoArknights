import ctypes, os, sys, time


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    time.sleep(1)
    if is_admin():
        # Code of your program here
        print("is Admin")
    else:
        # Re-run the program with admin rights
        print("not Admin")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
        os.system("pause")
        raise None
    print(sys.argv[0])
    os.system("pause")
