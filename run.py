#!/usr/bin/env python3

#
# اپن شد برای اولین بار در کانال آیرا تیم منبع نزنی بی ناموسی

# @IRA_Team
# https://t.me/IRA_Team
#

import os
import psutil
import subprocess

directory = os.path.dirname(os.path.abspath(__file__))
filename = str(os.path.basename(__file__))
try:
    with open(f"{directory}/pid/{filename}.txt", "r") as file:
        pid = int(file.read())
    if psutil.pid_exists(pid):
        pid = psutil.Process(pid)
        pid.terminate()
        print("terminate")
except:
    pass

subprocess.Popen(["python", "bot.py"])
subprocess.Popen(["python", "cr.settings.py"])
subprocess.Popen(["python", "tl.send-to-pv.py"])

#
# اپن شد برای اولین بار در کانال آیرا تیم منبع نزنی بی ناموسی

# @IRA_Team
# https://t.me/IRA_Team
#