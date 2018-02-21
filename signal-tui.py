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
import messages
import signal

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

    messages_area_bottom_y = int(curses.LINES*(4/5))

    # Prepare the login screen
    password_attempts = 0
    if login.open_login_screen(screen, password_attempts):
        screen.clear()
        draw_top_menu()
        screen.border(0)
        messages.import_messages()
        messages.open_messages_panel(screen, messages_area_bottom_y)


    curses.curs_set(False)
    x = 0
    while x != ord("e"):
        x = screen.getch()
        if x == ord("m"):
            messages.open_messages_panel(screen, messages_area_bottom_y)
        # TODO right now you can write a message from any tab, not just the messages tab
        # TODO I need to change the listeners depending on the current tab
        elif x == ord("i"):
            messages.write_message()
            
        elif x == ord("c"):
            open_contacts_panel()

        elif x == ord("s"):
            open_settings_panel()
        '''
        elif x == ord("\t"):
            messages.open_next_conversation()

        elif x == curses.KEY_PPAGE:
            messages.next_message_page()

        elif x == curses.KEY_NPAGE:
            messages.previous_message_page()
        '''




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
