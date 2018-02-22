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
    contact_buffer = [[1,"Thales Ferreira"], [2, "Ace Falkner"], [3, "Bryan Hayes"], [4, "Luke Doliszny"], [5, "Noah Stranger"], [6, "jkdhfljdhfjksdhfklasdjfhkljasdhfkjasdhflasdkjhfklsdfhj"]]

def draw_conversations_list():
    y = 4
    for contact in contact_buffer:
        screen.addstr(y, 2, contact[1], curses.A_STANDOUT)
        y += 2
