import ctypes
import sys
import os

check_result = os.popen('netsh interface ip show dnsservers "以太网"').read()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    if 'DHCP' in str(check_result):
        os.system('netsh interface ip set dns name="以太网" source=static addr=8.8.8.8 register=primary')
        print('Modify Successfully!')
    else:
        os.system('netsh interface ip set dns name="以太网" source=dhcp')
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
