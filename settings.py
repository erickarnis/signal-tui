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

    settings_buffer = ["register device", "enter verification code", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o"]

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

    screen.addstr(3, 3, "")
    screen.addstr(3, curses.COLS - len("I to edit") - 3, "I to edit")

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