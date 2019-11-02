import time
import os

check_result = os.popen('netsh interface ip show dnsservers "以太网"').read()

print(check_result)
time.sleep(3)
