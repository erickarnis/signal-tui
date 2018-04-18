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
import pathlib

USERNAME_MAX_LENGTH = 20

screen = None

from curses.textpad import rectangle

def open_user_creation_screen(scr, error_message):

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

    if error_message == 0:
        screen.addstr(22, int(curses.COLS / 2 - len("Create new user")/2), "Create new user")
    else:
        screen.addstr(22, int(curses.COLS / 2 - len(error_message)/2), error_message)

    curses.curs_set(True)

    username = input_username()
    password = input_password()

    username_test = check_username(username)

    if username_test == 0 and check_password(password):
        return True
    else:
        open_user_creation_screen(screen, username_test)

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
    # signal-tui's directory
    user_database = "/home/vgatz/Projects/signal-tui/" + username
    p = pathlib.Path(user_database)

    # user exists if database exists
    if p.is_file():
        return "Username taken"

    # else create user database

    if len(username) > USERNAME_MAX_LENGTH:
        return "Username too long"

    return 0

# TODO implement password creation, hashing, and storing
def check_password(password):
    if password == "e":
        return True
    else:
        return False