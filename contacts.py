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

contact_highlighted = 0

first_contact_on_page = 0

def import_contacts(sn):
    # TODO add a database
    global screen, contact_buffer
    screen = sn
    contact_buffer = [[0,"Thales Ferreira"], [1, "Manuela Bartolomeo"], [2, "Ace Falkner"], [3, "Bryan Hayes"], [4, "Luke Doliszny"], [5, "Noah Stranger"], [6, "Eliot Old"],[7,"John Smith"], [8, "Manuel Bart"], [9, "Aces Falk"], [10, "Bry Hay"], [11, "Luk Dol"], [12, "No Strange"], [13, "Felix Beiderman"], [14, "Linus T"], [15, "Richard S"], [16, "Peter Parker"],[17,"Tales Ferreira"], [111, "Manuela Bartolomeo"], [211, "Ace Falkner"], [311, "Bryan Hayes"], [411, "Luke Doliszny"], [511, "Noah Stranger"], [611, "Eliot Old"],[711,"John Smith"], [811, "Manuel Bart"], [911, "Aces Falk"], [101, "Bry Hay"], [111, "Luk Dol"], [112, "No Strange"], [113, "Felix Beiderman"], [114, "Linus T"], [115, "Richard S"], [116, "Peter Parker"]]
    return contact_buffer

def open_contacts_screen(sn):
    global screen, first_contact_on_page

    screen = sn

    first_contact_on_page = 0

    draw_contacts(0)

    screen.refresh()

def erase(top_x,top_y, bottom_x, bottom_y):
    for x in range(top_x, bottom_x):
            for y in range(top_y, bottom_y):
                    screen.addstr(y, x, " ")

def draw_contacts(name_highlighted):
    erase(1, 3, curses.COLS - 1, curses.LINES - 1)

    top_y = 4
    bottom_y = int(curses.COLS/6)
    left_x = 1
    right_x = int(curses.COLS/4)

    for contact in contact_buffer[first_contact_on_page:]:

        if contact_buffer.index(contact) == name_highlighted:
            screen.addstr(top_y + 2, left_x + 2, contact[1][:right_x - left_x - 2], curses.A_STANDOUT)

        else: 
            screen.addstr(top_y + 2, left_x + 2, contact[1][:right_x - left_x - 2], curses.A_NORMAL)

        rectangle(screen, top_y, left_x, bottom_y, right_x)


        left_x += int(curses.COLS/4)
        right_x += int(curses.COLS/4)

        if right_x > curses.COLS: 
            top_y += int(curses.COLS/6) - 2
            bottom_y += int(curses.COLS/6) - 2
            left_x = 2
            right_x = int(curses.COLS/4)

        if first_contact_on_page != 0:
            screen.addstr(3, int(curses.COLS/2) - 5, "more above")

        if bottom_y > curses.LINES - 2:
            screen.addstr(top_y, int(curses.COLS/2) - 5, "more below")
            break

def left():
    global contact_highlighted, first_contact_on_page

    if (contact_highlighted % 16) != 0:
        contact_highlighted -= 1
        draw_contacts(contact_highlighted)
    elif contact_highlighted != 0:
        contact_highlighted -= 1
        first_contact_on_page -= 16
        draw_contacts(contact_highlighted)   

def down():
    global contact_highlighted, first_contact_on_page

    if (contact_highlighted + 3) < contact_buffer.index(contact_buffer[-1]):

        if (((contact_highlighted + 1) % 16) <= 12 and ((contact_highlighted + 1) % 16) != 0) or contact_highlighted == 0: 
            contact_highlighted += 4   
            draw_contacts(contact_highlighted)
        else: 
            contact_highlighted += 4
            first_contact_on_page += 16
            draw_contacts(contact_highlighted)   

def up():
    global contact_highlighted, first_contact_on_page

    if (contact_highlighted % 16) >= 4:
        contact_highlighted -= 4
        draw_contacts(contact_highlighted)
    elif contact_highlighted >= 4:
        contact_highlighted -= 4
        first_contact_on_page -= 16
        draw_contacts(contact_highlighted)  

def right():
    global contact_highlighted, first_contact_on_page

    if contact_highlighted != contact_buffer.index(contact_buffer[-1]):

        if ((contact_highlighted + 1) % 16) != 0:    
            contact_highlighted += 1
            draw_contacts(contact_highlighted)
        else: 
            contact_highlighted += 1
            first_contact_on_page += 16
            draw_contacts(contact_highlighted)   

