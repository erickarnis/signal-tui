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
    contact_buffer = [[0,"Thales Ferreira"], [1, "Manuela Bartolomeo"], [2, "Ace Falkner"], [3, "Bryan Hayes"], [4, "Luke Doliszny"], [5, "Noah Stranger"], [6, "jkdhfljdhfjksdhfklasdjfhkljasdhfkjasdhflasdkjhfklsdfhj"]]
    return contact_buffer

def draw_conversations_list(name_highlighted):
    y = 4
    for contact in contact_buffer:
        if contact_buffer.index(contact) == name_highlighted:
            screen.addstr(y, 2, contact[1], curses.A_STANDOUT)

        else: screen.addstr(y, 2, contact[1], curses.A_NORMAL)

        y += 2

    screen.vline(3, int(curses.COLS/4), curses.ACS_VLINE, curses.COLS - 3)
    screen.refresh()
