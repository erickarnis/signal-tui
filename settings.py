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
import threading

#Signal-tui modules
import signal_cli_wrapper

from curses.textpad import Textbox, rectangle

screen = None

first_item_on_page = 0

item_highlighted = 0

settings_buffer = []

def open_settings_screen(sn):
    global screen, first_item_on_page, item_highlighted

    screen = sn

    first_item_on_page = 0

    item_highlighted = 0

    import_settings()

    draw_settings(0)

    screen.refresh()

def import_settings():
    global settings_buffer

    settings_buffer = ["register device", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o"]

def erase(top_x, top_y, bottom_x, bottom_y):
    for x in range(top_x, bottom_x):
        for y in range(top_y, bottom_y):
            screen.addstr(y, x, " ")

    screen.refresh()

def draw_settings(item_highlighted):
    erase(1, 3, curses.COLS - 1, curses.LINES - 1)

    y_increment = int((curses.LINES)/10) - 1

    top_y = 5
    bottom_y = int((curses.LINES)/8)
    left_x = int(curses.COLS/4)
    right_x = int(3*curses.COLS/4)

    for setting in settings_buffer[first_item_on_page:]:

        # if selected
        if settings_buffer.index(setting) == item_highlighted:
            screen.addstr(top_y + 1, left_x + 2, setting, curses.A_STANDOUT)
        # if unselected
        else:
            screen.addstr(top_y + 1, left_x + 2, setting, curses.A_NORMAL)

        rectangle(screen, top_y, left_x, bottom_y, right_x)

        top_y += y_increment
        bottom_y += y_increment

        if first_item_on_page != 0:
            screen.addstr(3, int(curses.COLS/2) - 5, "more above")

        if bottom_y > curses.LINES - 3:
            screen.addstr(curses.LINES - 2, int(curses.COLS/2) - 5, "more below")
            break

def down():
    global item_highlighted, first_item_on_page

    if (item_highlighted % 11) == 10:
        item_highlighted += 1
        first_item_on_page += 11
        draw_settings(item_highlighted)
    elif item_highlighted != settings_buffer.index(settings_buffer[-1]):
        item_highlighted += 1
        draw_settings(item_highlighted)

def up():
    global item_highlighted, first_item_on_page

    if (item_highlighted % 11) >= 1:
        item_highlighted -= 1
        draw_settings(item_highlighted)
    elif item_highlighted != 0:
        item_highlighted -= 1
        first_item_on_page -= 11
        draw_settings(item_highlighted)

def edit_setting():
    erase(1, 3, curses.COLS - 1, curses.LINES - 1)
    screen.addstr(int(curses.LINES/6) + 1, int(curses.COLS/2 - (len(settings_buffer[item_highlighted]))/2), settings_buffer[item_highlighted])
    rectangle(screen, 
              int(curses.LINES/6), 
              int(curses.COLS/6), 
              int(5 * (curses.LINES/6)), 
              int(5 * (curses.COLS/6)))
    if (settings_buffer[item_highlighted] == "register device"):
        register_device()

def register_device():
    screen.addstr(int(curses.LINES/6) + 4, int(curses.COLS/6 + 4), "enter your phone number like this: 1234567891")
    screen.refresh()
    number_to_register = add_text_box(1, 
                                    int((curses.COLS - 4)/4) - 9, 
                                    int(curses.LINES/6) + 6, 
                                    int(curses.COLS/6 + 5))

    try: number_to_register = int(number_to_register)
    except ValueError:
        screen.addstr(int(curses.LINES/6) + 8, int(curses.COLS/6 + 4), "not an int")
        screen.refresh()
        time.sleep(3)
        edit_setting()

    if type(number_to_register) is int:
        if len(str(number_to_register)) == 10:
            t = threading.Thread(target=signal_cli_wrapper.register_device, args=(number_to_register,))
            t.start()
        else:
            screen.addstr(int(curses.LINES/6) + 8, int(curses.COLS/6 + 4), "not 10 digits")
            screen.refresh()
            time.sleep(3)
            edit_setting()

    screen.addstr(int(curses.LINES/6) + 8, int(curses.COLS/6 + 4), "request sent")
    screen.addstr(int(curses.LINES/6) + 10, int(curses.COLS/6 + 4), "enter verification code")
    screen.refresh()

    code_to_verify = add_text_box(1, 
                                    int((curses.COLS - 4)/4) - 9, 
                                    int(curses.LINES/6) + 12, 
                                    int(curses.COLS/6 + 5))

    t = threading.Thread(target=signal_cli_wrapper.verify_code, args=(code_to_verify,))
    t.start()
    screen.addstr(int(curses.LINES/6) + 14, int(curses.COLS/6 + 4), "your number is verified")
    screen.refresh()
    time.sleep(3)    
    open_settings_screen(screen)


def add_text_box(height, width, top_y, left_x):
    rectangle(screen, 
              top_y - 1,
              left_x - 1, 
              top_y + height,
              left_x + width)
    screen.refresh()
    curses.curs_set(True)
    # height, width, top_y, top_x
    editwin = curses.newwin(height, width, top_y, left_x)
    editwin.bkgdset(curses.A_STANDOUT)
    box = Textbox(editwin)
    box.stripspaces = True
    # Let the user edit until Ctrl-G is struck.
    box.edit()

    # Get resulting contents
    message = box.gather()

    #this renders the blinking cursor invisible again
    curses.curs_set(False)

    return message
