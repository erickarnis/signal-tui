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

# Define the appearance of some interface elements
hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
menu_attr = curses.A_NORMAL

# Define additional constants
EXIT = 0
CONTINUE = 1

# Give screen module scope
screen = None

# Define the topbar menus
menu_items = ["Messages", "Contacts", "Settings", "Exit"]

# helper functions
def get_param(prompt_string):
    stdscr.clear()
    stdscr.border(0)
    stdscr.addstr(2, 2, prompt_string)
    stdscr.refresh()
    input = stdscr.getstr(10, 10, 60)
    return input


def execute_cmd(cmd_string):
    system("clear")
    a = system(cmd_string)

    print("")
    if a == 0:
        print("Command executed correctly")
    else:
        print("Command terminated with error")
    raw_input("Press enter")
    print("")


def file_is_empty(path):
    return os.stat(path).st_size == 0


# prepare username and user data file
with open('user_data.txt', 'r') as file:
    user_data = file.readlines()

if user_data:
    username = user_data[0]

##########################
## Signal functionality ##
##########################


# Registers the user with Whisper Systems. If it works, they will send a
# verification number to the user's phone
def register_device():
    user_data[0] = username
    with open('user_data.txt', 'w') as file:
        file.writelines(user_data)
    curses.endwin()
    execute_cmd("signal-cli -u " + username + " register")


# Send's user's verification number to Whisper Systems
def verify_code(verification_number):
    curses.endwin()
    execute_cmd(
        "signal-cli -u " + username + " verify " + str(verification_number)
    )


# Sends a message to another signal user
def send_message(recipient, message):
    curses.endwin()
    execute_cmd(
        "signal-cli -u " + username + ' send -m \"'
        + message + '\"[' + recipient + "]"
    )


# Checks for unread messages
# TODO have this check periodically and write all messages to a file
def check_messages():
    curses.endwin()
    execute_cmd("signal-cli -u " + str(username) + " receive")


#########################
#### Password Screen ####
#########################
def open_password_screen(password_attempts):
    stdscr.clear()

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
        quit()

    rectangle(stdscr, 24, int(curses.COLS / 2 - 31), 26, int(curses.COLS / 2 + 31))
    screen.refresh()

    # Get then clean up password
    password = stdscr.getstr(25, int(curses.COLS / 2 - 30), 60)
    password = str(password)[2:]
    password = password[:-1]

    if password:
        screen.addstr(27, int(curses.COLS / 2 - 7), password)

    if check_password(password):
        open_messages_panel()
    else:
        password_attempts += 1
        open_password_screen(password_attempts)


# TODO implement password creation, hashing, and storing
def check_password(password):
    if password == "eric":
        return True
    else:
        return False


####################
##### Top Menu #####
####################

def draw_top_menu():
    left = 2
    for menu_name in menu_items:
        menu_hotkey = menu_name[0]
        menu_no_hot = menu_name[1:]
        offset = int(curses.COLS/10 - len(menu_name)/2)
        screen.addstr(1, left + offset, menu_hotkey, hotkey_attr)
        screen.addstr(1, left + offset + 1, menu_no_hot, menu_attr)
        left = left + int(curses.COLS/5)
    # Draw application title
    offset = int(curses.COLS/10 - len("signal-tui"))
    screen.addstr(1, left + offset, "signal-tui", curses.A_STANDOUT)
    screen.hline(2, 1, curses.ACS_HLINE, curses.COLS - 3)
    screen.refresh()


###########################
#### Hotkey Functions #####
###########################

def open_messages_panel():
    # Clear screen
    stdscr.clear()
    draw_top_menu()
    stdscr.border(0)
    # Top line of text area
    screen.hline(int(curses.LINES*(3/4))-2,
                 int(curses.COLS/4),
                 curses.ACS_HLINE, curses.COLS - 3)
    # right line of conversations panel
    screen.vline(3, int(curses.COLS/4), curses.ACS_VLINE, curses.COLS - 3)
    stdscr.addstr(int(curses.LINES*(3/4)) - 2,
                  int(curses.COLS/4) + 1,
                  " I to enter edit mode ")
    stdscr.addstr(int(curses.LINES*(3/4)) - 2,
                  curses.COLS - 17,
                  " Ctrl-G to send ")
    # rectangle(stdscr, 1,0, 7, 32)
    stdscr.refresh()


def write_message():
    curses.curs_set(True)
    # length, width, y, x
    editwin = curses.newwin(int(curses.LINES/4),
                            int(curses.COLS*(3/4)) - 2,
                            int(curses.LINES*(3/4)),
                            int(curses.COLS/4) + 1)
    editwin.bkgdset(curses.A_STANDOUT)
    box = Textbox(editwin)
    box.stripspaces = True
    # Let the user edit until Ctrl-G is struck.
    box.edit()

    # Get resulting contents
    message = box.gather()

    if message:
        # send_message(recipient, input)
        add_message(message)

    curses.curs_set(False)
    stdscr.refresh()


def add_message(message):
    # TODO push other messages about the page when a new one arrives
    # TODO have a linked list or something similar to store messages in a buffer
    message_line_len = int(curses.COLS*(1/2) - 5)
    message_line_num = int(math.ceil(len(message)/message_line_len))
    for x in range(0, message_line_num):
        start_line_index = x * message_line_len
        end_line_index = (x + 1) * message_line_len - 1
        line = message[start_line_index: end_line_index]
        try:
            stdscr.addstr(int(curses.LINES*(1/2)) + x + 1,
                          int(curses.COLS*(1/2)) + 1,
                          line, curses.A_STANDOUT)
        except curses.error:
            pass

    rectangle(stdscr,
              int(curses.LINES*(1/2)),
              int(curses.COLS*(1/2)),
              int(curses.LINES*(3/4)) - 3,
              curses.COLS - 3)
    stdscr.border(0)
    stdscr.refresh()


def open_contacts_panel():
    get_param("hi")


def open_settings_panel():
    get_param("hi")


##############
#### Main ####
##############

def main(stdscr):

    global screen
    screen = stdscr.subwin(curses.LINES - 1, curses.COLS - 1, 0, 0)
    screen.box()
    screen.refresh()

    # Prepare the login screen
    password_attempts = 0
    open_password_screen(password_attempts)
    curses.curs_set(False)
    x = 0
    while x != ord("e"):
        x = screen.getch()
        if x == ord("m"):
            open_messages_panel()
        # TODO right now you can write a message from any tab, not just the messages tab
        # TODO I need to change the listeners depending on the current tab
        elif x == ord("i"):
            write_message()

        elif x == ord("c"):
            open_contacts_panel()

        elif x == ord("s"):
            open_settings_panel()


# Initialize and call main
if __name__ == '__main__':
    try:
        # Initialize curses
        stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        curses.noecho()
        curses.cbreak()

        # In keypad mode, escape sequences for special keys
        # (like the cursor keys) will be interpreted and
        # a special value like curses.KEY_LEFT will be returned
        stdscr.keypad(1)
        # Enter the main loop
        main(stdscr)
        # Set everything back to normal
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        # Terminate curses
        curses.endwin()

    # If something goes wrong, restore terminal and report exception
    except:
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        # Print the exception
        traceback.print_exc()
