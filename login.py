'''
          @@\                               @@\          @@\               @@\
          \__|                              @@ |         @@ |              \__|
 @@@@@@@\ @@\  @@@@@@\  @@@@@@@\   @@@@@@\  @@ |       @@@@@@\   @@\   @@\ @@\
@@  _____|@@ |@@  __@@\ @@  __@@\  \____@@\ @@ |@@@@@@\|_@@  _|  @@ |  @@ |@@ |
\@@@@@@\  @@ |@@ /  @@ |@@ |  @@ | @@@@@@@ |@@ |\______\ @@ |    @@ |  @@ |@@ |
 \____@@\ @@ |@@ |  @@ |@@ |  @@ |@@  __@@ |@@ |         @@ |@@\ @@ |  @@ |@@ |
@@@@@@@  |@@ |\@@@@@@@ |@@ |  @@ |\@@@@@@@ |@@ |         \@@@@  |\@@@@@@  |@@ |
\_______/ \__| \____@@ |\__|  \__| \_______|\__|          \____/  \______/ \__|
              @@\   @@ |
              \@@@@@@  |
               \______/

By Eric Karnis
This will be under gpl someday
'''
# !/usr/bin/env python3
import curses
import traceback
import os
import string
import math
import time

from curses.textpad import Textbox, rectangle
from os import system

def open_login_screen(screen, password_attempts):
    screen.clear()

    x = int(curses.COLS / 2 - 40)

    screen.addstr(10, x, "          @@\                               @@\          @@\               @@\ ")
    screen.addstr(11, x, "          \__|                              @@ |         @@ |              \__|")
    screen.addstr(12, x, " @@@@@@@\ @@\  @@@@@@\  @@@@@@@\   @@@@@@\  @@ |       @@@@@@\   @@\   @@\ @@\ ")
    screen.addstr(13, x, "@@  _____|@@ |@@  __@@\ @@  __@@\  \____@@\ @@ |@@@@@@\|_@@  _|  @@ |  @@ |@@ |")
    screen.addstr(14, x, "\@@@@@@\  @@ |@@ /  @@ |@@ |  @@ | @@@@@@@ |@@ |\______\ @@ |    @@ |  @@ |@@ |")
    screen.addstr(15, x, " \____@@\ @@ |@@ |  @@ |@@ |  @@ |@@  __@@ |@@ |         @@ |@@\ @@ |  @@ |@@ |")
    screen.addstr(16, x, "@@@@@@@  |@@ |\@@@@@@@ |@@ |  @@ |\@@@@@@@ |@@ |         \@@@@  |\@@@@@@  |@@ |")
    screen.addstr(17, x, "\_______/ \__| \____@@ |\__|  \__| \_______|\__|          \____/  \______/ \__|")
    screen.addstr(18, x, "              @@\   @@ |")
    screen.addstr(19, x, "              \@@@@@@  |                                         By Eric Karnis")
    screen.addstr(20, x, "               \______/ ")

    if password_attempts == 0:
        screen.addstr(23, int(curses.COLS / 2 - 7), "Enter Password")
    elif password_attempts < 3:
        screen.addstr(23, int(curses.COLS / 2 - 7), "Wrong Password")
    else:
        screen.addstr(25, int(curses.COLS / 2 - 7), "Too Many Attempts")
        screen.refresh()
        time.sleep(5)
        quit("\033[1m" + "Too Many Password Attempts" + "\033[1m")

    rectangle(screen, 24, int(curses.COLS / 2 - 31), 26, int(curses.COLS / 2 + 31))
    screen.refresh()

    # Get then clean up password
    password = screen.getstr(25, int(curses.COLS / 2 - 30), 60)
    password = str(password)[2:]
    password = password[:-1]


    if check_password(password):
        return True
    else:
        password_attempts += 1
        return open_login_screen(screen, password_attempts)

# TODO implement password creation, hashing, and storing
def check_password(password):
    if password == "e":
        return True
    else:
        return False