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

#Signal-tui modules
import login

# Define the appearance of some interface elements
hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
menu_attr = curses.A_NORMAL

# Define additional constants
EXIT = 0
CONTINUE = 1

# Give screen module scope
screen = None

message_buffer = [["s", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["r","what's up?"],["s","hey"],["r", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["s","hey"],["r","what's up?"],["s","u nerd"],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s","hey"],["r","pls respond"]]
top_message_on_page_index = 0

# Define the topbar menus
menu_items = ["Messages", "Contacts", "Settings", "Exit"]

# helper functions
def get_param(prompt_string):
    screen.clear()
    screen.border(0)
    screen.addstr(2, 2, prompt_string)
    screen.refresh()
    input = screen.getstr(10, 10, 60)
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

def erase(top_x,top_y, bottom_x, bottom_y):
    for x in range(top_x, bottom_x):
            for y in range(top_y, bottom_y):
                    screen.addstr(y, x, " ")

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
    screen.clear()
    draw_top_menu()
    screen.border(0)
    # Top line of text area
    screen.hline(messages_area_bottom_y - 2,
                 int(curses.COLS/4),
                 curses.ACS_HLINE, curses.COLS - 3)
    # right line of conversations panel
    screen.vline(3, int(curses.COLS/4), curses.ACS_VLINE, curses.COLS - 3)
    screen.addstr(messages_area_bottom_y - 2,
                  int(curses.COLS/4) + 1,
                  " I to enter edit mode ")
    screen.addstr(messages_area_bottom_y - 2,
                  curses.COLS - 17,
                  " Ctrl-G to send ")
    draw_messages()
    screen.refresh()


def write_message():
    curses.curs_set(True)
    # length, width, y, x
    editwin = curses.newwin(int(curses.LINES/4),
                            int(curses.COLS*(3/4)) - 2,
                            messages_area_bottom_y,
                            int(curses.COLS/4) + 1)
    editwin.bkgdset(curses.A_STANDOUT)
    box = Textbox(editwin)
    box.stripspaces = True
    # Let the user edit until Ctrl-G is struck.
    box.edit()

    # Get resulting contents
    message = box.gather()

    if message:
        # if send_message(recipient, input):
        add_message("s", message)

    curses.curs_set(False)
    screen.refresh()


def add_message(originator, message):
    # TODO: write the message to a database here
    message_buffer.append([originator, message])
    draw_messages()

def import_messages():
    # TODO add a database
    void

def draw_messages():

    # clear the messages area
    erase(int(curses.COLS/4) + 1, 3, curses.COLS - 2, messages_area_bottom_y - 2)

    message_line_len = int(curses.COLS*(1/2) - 5)

    message_bottom_y = messages_area_bottom_y - 3

    for message in reversed(message_buffer):

        # Check if the message was sent or received and put the message on the left 
        # or right respectively
        if message[0] == "s":
            message_box_left_x = int(curses.COLS*(1/2))
            message_box_right_x = curses.COLS - 3
        else:
            message_box_left_x = int(curses.COLS*(1/4) + 2)
            message_box_right_x = int(curses.COLS*(3/4) - 1)

        # Write the message line by line
        message_line_num = int(math.ceil(len(message[1])/message_line_len))

        # If the message does not fit on the page, stop drawing messages
        # and print more above at the top
        if (message_bottom_y - 3 - message_line_num) < 3:
            top_message_on_page_index = message_buffer.index(message) - 1
            screen.addstr(5, int(5*curses.COLS/8) - 5, "more above")
            break

        for x in range(0, message_line_num):
            start_line_index = x * message_line_len
            end_line_index = (x + 1) * message_line_len - 1
            line = message[1][start_line_index: end_line_index]
            try:
                screen.addstr(message_bottom_y - 2 - message_line_num + x + 1,
                              message_box_left_x + 1,
                              line, curses.A_STANDOUT)
            except curses.error:
                pass

        rectangle(screen,
                  message_bottom_y - 2 - message_line_num,
                  message_box_left_x,
                  message_bottom_y,
                  message_box_right_x)

        message_bottom_y = message_bottom_y - 3 - message_line_num



        screen.border(0)
        screen.refresh()

def open_contacts_panel():
    get_param("hi")


def open_settings_panel():
    get_param("hi")


##############
#### Main ####
##############

def main(stdscr):

    global screen
    screen = stdscr
    screen.box()
    screen.refresh()

    # UI globals
    # Needs to be defined here to use curses
    global messages_area_bottom_y 
    messages_area_bottom_y = int(curses.LINES*(4/5))

    # Prepare the login screen
    password_attempts = 0
    if login.open_login_screen(screen, password_attempts):
            open_messages_panel()

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

        #elif ( x == ord("\t"):
            #open_next_conversation()

        elif x == curses.KEY_PPAGE:
            next_message_page()

        elif x == curses.KEY_NPAGE:
            previous_message_page()

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
