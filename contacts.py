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

screen = None

contact_buffer = []

def import_contacts(sn):
    # TODO add a database
    global screen, contact_buffer
    screen = sn
    contact_buffer = [[0,"Thales Ferreira"], [1, "Manuela Bartolomeo"], [2, "Ace Falkner"], [3, "Bryan Hayes"], [4, "Luke Doliszny"], [5, "Noah Stranger"], [6, "Eliot Old"],[7,"John Smith"], [8, "Manuel Bart"], [9, "Aces Falk"], [10, "Bry Hay"], [11, "Luk Dol"], [12, "No Strange"], [13, "Felix Beiderman"], [14, "Linus T"], [15, "Richard S"], [16, "Peter Parker"]]
    return contact_buffer

def open_contacts_screen(sn):
    global screen

    screen = sn

    draw_contacts()

    screen.refresh()

def draw_contacts():
    top_y = 4
    bottom_y = int(curses.COLS/6)
    left_x = 1
    right_x = int(curses.COLS/4)

    for contact in contact_buffer:

        rectangle(screen, top_y, left_x, bottom_y, right_x)
        screen.addstr(top_y + 2, left_x + 2, contact[1][:right_x - left_x - 2], curses.A_STANDOUT)

        left_x += int(curses.COLS/4)
        right_x += int(curses.COLS/4)

        if right_x > curses.COLS: 
            top_y += int(curses.COLS/6) - 2
            bottom_y += int(curses.COLS/6) - 2
            left_x = 2
            right_x = int(curses.COLS/4)

        if bottom_y > curses.LINES - 2:
            screen.addstr(top_y, int(curses.COLS/2) - 5, "more below")
            break