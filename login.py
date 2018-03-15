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
import time

MAX_ATTEMPTS = 3

screen = None

from curses.textpad import rectangle

def open_login_screen(scr, attempts):
    global screen

    screen = scr

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

    if attempts != 0 and attempts < MAX_ATTEMPTS:
        screen.addstr(22, int(curses.COLS / 2 - 13), "Wrong Password or Username")
    elif attempts >= MAX_ATTEMPTS:
        screen.addstr(25, int(curses.COLS / 2 - 7), "Too Many Attempts")
        screen.refresh()
        time.sleep(5)
        quit("\033[1m" + "Too Many Attempts" + "\033[1m")

    username = input_username()
    password = input_password()

    if check_username(username) and check_password(password):
        return True
    else:
        attempts += 1
        return open_login_screen(screen, attempts)

def input_username():

    screen.addstr(24, int(curses.COLS / 2 - 7), "Enter Username")
    rectangle(screen, 25, int(curses.COLS / 2 - 31), 27, int(curses.COLS / 2 + 31))
    screen.refresh()

    # Get then clean up username
    username = screen.getstr(26, int(curses.COLS / 2 - 30), 60)
    username = str(username)[2:-1]

    return username

def input_password():

    screen.addstr(24, int(curses.COLS / 2 - 7), "Enter Password")
    rectangle(screen, 25, int(curses.COLS / 2 - 31), 27, int(curses.COLS / 2 + 31))
    screen.refresh()

    # Get then clean up password
    password = screen.getstr(26, int(curses.COLS / 2 - 30), 60)
    password = str(password)[2:-1]

    return password


def check_username(username):
    if username == "e":
        return True
    else:
        return False

# TODO implement password creation, hashing, and storing
def check_password(password):
    if password == "e":
        return True
    else:
        return False