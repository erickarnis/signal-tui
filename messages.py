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

message_buffer = []
page_index = [0]
current_page = 0
messages_area_bottom_y = 0

def open_messages_screen(sn, current_conversation, contact_buffer):
    global screen, messages_area_bottom_y, current_page

    screen = sn
    messages_area_bottom_y = int(curses.LINES*(4/5))
    current_page = 0

    draw_conversations_list(current_conversation, contact_buffer)

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

    refresh_page_index(current_conversation)
    draw_messages(current_conversation)
    screen.refresh()



def write_message(current_conversation):
    curses.curs_set(True)
    # length, width, y, x
    editwin = curses.newwin(int(curses.LINES/5),
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
        add_message(current_conversation, "s", message)

    curses.curs_set(False)
    screen.refresh()


def add_message(current_conversation, originator, message):
    # TODO: write the message to a database here
    message_buffer[current_conversation].append([originator, message])

    refresh_page_index(current_conversation)
    draw_messages(current_conversation)

def erase(top_x,top_y, bottom_x, bottom_y):
    for x in range(top_x, bottom_x):
            for y in range(top_y, bottom_y):
                    screen.addstr(y, x, " ")

def import_messages():
    # TODO add a database
    global message_buffer
    message_buffer = [
    [["s", "Sed vitae magna non eros luctus viverra."],["r","Vivamus ullamcorper gravida augue, ut fermentum enim aliquet sit amet."],["s","Fusce libero ipsum, feugiat nec libero at, placerat rhoncus dui."],["r", "Etiam elit erat, luctus accumsan felis ut, finibus sollicitudin metus.bus."],["r","Vivamus ornare commodo tellus in vestibulum."],["s","Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent et sollicitudin massa."],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s"," Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam imperdiet, felis a euismod rhoncus, dui nibh lobortis leo, auctor fringilla eros nisl nec eros."],["r","Curabitur ut blandit diam, eget rhoncus arcu."],["s", "Maecenas feugiat dolor nibh, nec pharetra leo auctor ut. Duis sagittis maximus eros, vitae aliquam elit luctus a. Ut sed orci eget arcu efficitur tempor. Aenean pulvinar fermentum leo et suscipit. Duis semper eros sit amet porta interdum. "],["r","what's up?"],["s","hey"],["r", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["s","hey"],["r","what's up?"],["s","u nerd"],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s","hey"],["r","pls respond"]],
    [["s", "18"],["r","17"],["s","16"],["r", "15"],["s","14"],["r","13"],["s","12"],["r","11"],["s","10"],["r","9"],["s", "8"],["r","7"],["r", "6"],["s","5"],["r","4"],["s","3"],["r","2"],["s","1"],["r","0"]],
    [["s", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["r","what's up?"],["s","hey"],["r", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["s","hey"],["r","what's up?"],["s","u loser"],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s","hey"],["r","pls respond"]],
    [["s", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["r","what's up?"],["s","hey"],["r", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["s","hey"],["r","what's up?"],["s","u dum dum"],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s","hey"],["r","pls respond"]],
    [["s", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["r","what's up?"],["s","hey"],["r", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["s","hey"],["r","what's up?"],["s","u baby"],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s","hey"],["r","pls respond"]],
    [["s", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["r","what's up?"],["s","hey"],["r", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["s","hey"],["r","what's up?"],["s","u lame-o"],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s","hey"],["r","pls respond"]],
    [["s", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["r","what's up?"],["s","hey"],["r", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["s","hey"],["r","what's up?"],["s","u jerk"],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s","hey"],["r","pls respond"]],
    [["s", "Sed vitae magna non eros luctus viverra."],["r","Vivamus ullamcorper gravida augue, ut fermentum enim aliquet sit amet."],["s","Fusce libero ipsum, feugiat nec libero at, placerat rhoncus dui."],["r", "Etiam elit erat, luctus accumsan felis ut, finibus sollicitudin metus.bus."],["r","Vivamus ornare commodo tellus in vestibulum."],["s","Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent et sollicitudin massa."],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s"," Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam imperdiet, felis a euismod rhoncus, dui nibh lobortis leo, auctor fringilla eros nisl nec eros."],["r","Curabitur ut blandit diam, eget rhoncus arcu."],["s", "Maecenas feugiat dolor nibh, nec pharetra leo auctor ut. Duis sagittis maximus eros, vitae aliquam elit luctus a. Ut sed orci eget arcu efficitur tempor. Aenean pulvinar fermentum leo et suscipit. Duis semper eros sit amet porta interdum. "],["r","what's up?"],["s","hey"],["r", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["s","hey"],["r","what's up?"],["s","u nerd"],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s","hey"],["r","pls respond"]],
    [["s", "18"],["r","17"],["s","16"],["r", "15"],["s","14"],["r","13"],["s","12"],["r","11"],["s","10"],["r","9"],["s", "8"],["r","7"],["r", "6"],["s","5"],["r","4"],["s","3"],["r","2"],["s","1"],["r","0"]],
    [["s", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["r","what's up?"],["s","hey"],["r", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["s","hey"],["r","what's up?"],["s","u loser"],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s","hey"],["r","pls respond"]],
    [["s", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["r","what's up?"],["s","hey"],["r", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["s","hey"],["r","what's up?"],["s","u dum dum"],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s","hey"],["r","pls respond"]],
    [["s", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["r","what's up?"],["s","hey"],["r", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["s","hey"],["r","what's up?"],["s","u baby"],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s","hey"],["r","pls respond"]],
    [["s", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["r","what's up?"],["s","hey"],["r", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["s","hey"],["r","what's up?"],["s","u lame-o"],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s","hey"],["r","pls respond"]],
    [["s", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["r","what's up?"],["s","hey"],["r", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["s","hey"],["r","what's up?"],["s","u jerk"],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s","hey"],["r","pls respond"]],
    [["s", "Sed vitae magna non eros luctus viverra."],["r","Vivamus ullamcorper gravida augue, ut fermentum enim aliquet sit amet."],["s","Fusce libero ipsum, feugiat nec libero at, placerat rhoncus dui."],["r", "Etiam elit erat, luctus accumsan felis ut, finibus sollicitudin metus.bus."],["r","Vivamus ornare commodo tellus in vestibulum."],["s","Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent et sollicitudin massa."],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s"," Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam imperdiet, felis a euismod rhoncus, dui nibh lobortis leo, auctor fringilla eros nisl nec eros."],["r","Curabitur ut blandit diam, eget rhoncus arcu."],["s", "Maecenas feugiat dolor nibh, nec pharetra leo auctor ut. Duis sagittis maximus eros, vitae aliquam elit luctus a. Ut sed orci eget arcu efficitur tempor. Aenean pulvinar fermentum leo et suscipit. Duis semper eros sit amet porta interdum. "],["r","what's up?"],["s","hey"],["r", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["s","hey"],["r","what's up?"],["s","u nerd"],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s","hey"],["r","pls respond"]],
    [["s", "Sed vitae magna non eros luctus viverra."],["r","Vivamus ullamcorper gravida augue, ut fermentum enim aliquet sit amet."],["s","Fusce libero ipsum, feugiat nec libero at, placerat rhoncus dui."],["r", "Etiam elit erat, luctus accumsan felis ut, finibus sollicitudin metus.bus."],["r","Vivamus ornare commodo tellus in vestibulum."],["s","Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent et sollicitudin massa."],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s"," Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam imperdiet, felis a euismod rhoncus, dui nibh lobortis leo, auctor fringilla eros nisl nec eros."],["r","Curabitur ut blandit diam, eget rhoncus arcu."],["s", "Maecenas feugiat dolor nibh, nec pharetra leo auctor ut. Duis sagittis maximus eros, vitae aliquam elit luctus a. Ut sed orci eget arcu efficitur tempor. Aenean pulvinar fermentum leo et suscipit. Duis semper eros sit amet porta interdum. "],["r","what's up?"],["s","hey"],["r", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["s","hey"],["r","what's up?"],["s","u nerd"],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s","hey"],["r","pls respond"]],
    [["s", "Sed vitae magna non eros luctus viverra."],["r","Vivamus ullamcorper gravida augue, ut fermentum enim aliquet sit amet."],["s","Fusce libero ipsum, feugiat nec libero at, placerat rhoncus dui."],["r", "Etiam elit erat, luctus accumsan felis ut, finibus sollicitudin metus.bus."],["r","Vivamus ornare commodo tellus in vestibulum."],["s","Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent et sollicitudin massa."],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s"," Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam imperdiet, felis a euismod rhoncus, dui nibh lobortis leo, auctor fringilla eros nisl nec eros."],["r","Curabitur ut blandit diam, eget rhoncus arcu."],["s", "Maecenas feugiat dolor nibh, nec pharetra leo auctor ut. Duis sagittis maximus eros, vitae aliquam elit luctus a. Ut sed orci eget arcu efficitur tempor. Aenean pulvinar fermentum leo et suscipit. Duis semper eros sit amet porta interdum. "],["r","what's up?"],["s","hey"],["r", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50."],["s","hey"],["r","what's up?"],["s","u nerd"],["r","jdflkjdlfkjsdlfjbdslfhjblsdjhfbdlsjhflsadfhlsdjfhlkjshlkfsd?"],["s","hey"],["r","pls respond"]]
    ]
    return message_buffer


def draw_conversations_list(name_highlighted, contact_buffer):
    y = 4
    for contact in contact_buffer:
        if contact_buffer.index(contact) == name_highlighted:
            screen.addstr(y, 2, contact[1], curses.A_STANDOUT)

        else: screen.addstr(y, 2, contact[1], curses.A_NORMAL)

        y += 2
        if y > curses.LINES - 2:
            break

    screen.vline(3, int(curses.COLS/4), curses.ACS_VLINE, curses.COLS - 3)
    screen.refresh()


# This draws the messages of the conversation given as an argument to the message screen
# TODO: The first character of each line except the first get's cut off. This bug has been 
# TODO: around for a while and if anyone can help I would appreciate it.
def draw_messages(current_conversation):

    # clear the messages area, ie the space to the left of the contacts panel and above the 
    # message writing panel
    erase(int(curses.COLS/4) + 1, 3, curses.COLS - 2, messages_area_bottom_y - 2)

    line_len = int(curses.COLS*(1/2) - 5)

    reversed_message = message_buffer[current_conversation][::-1]

    message_bottom_y = messages_area_bottom_y - 3

    if current_page > 0:
        screen.addstr(messages_area_bottom_y - 3, int(5*curses.COLS/8) - 5, "more below")
        message_bottom_y -= 1

    for message in reversed_message[page_index[current_page]:]:

        # Check if the message was sent or received and put the message on the left 
        # or right respectively
        if message[0] == "s":
            left_x = int(curses.COLS*(1/2))
            right_x = curses.COLS - 3
        elif message[0] == "r":
            left_x = int(curses.COLS*(1/4) + 2)
            right_x = int(curses.COLS*(3/4) - 1)
        else:
            quit("Incorrect Sent/Recieved code in buffer")

        # Calculate the number of lines in the message
        line_num = int(math.ceil(len(message[1])/line_len))

        # If the message does not fit on the page, stop drawing messages
        # and print "more above" at the top
        if (message_bottom_y - 3 - line_num) < 3:
            global top_message
            top_message = reversed_message.index(message)
            screen.addstr(4, int(5*curses.COLS/8) - 5, "more above")
            break

        for x in range(0, line_num):
            start_line_index = x * line_len
            end_line_index = (x + 1) * line_len - 1
            line = message[1][start_line_index: end_line_index]
            try:
                screen.addstr(message_bottom_y - 2 - line_num + x + 1,
                              left_x + 1,
                              line, curses.A_STANDOUT)
            except curses.error:
                pass

        rectangle(screen,
                  message_bottom_y - 2 - line_num,
                  left_x,
                  message_bottom_y,
                  right_x)

        message_bottom_y = message_bottom_y - 3 - line_num

    screen.border(0)
    screen.refresh()

def page_down(current_conversation):
    global current_page
    if current_page != 0: 
        current_page -=1
        draw_messages(current_conversation)

def page_up(current_conversation):
    global current_page
    if current_page != page_index.index(page_index[-1]): 
        current_page += 1
        draw_messages(current_conversation)


def refresh_page_index(current_conversation):
    global page_index

    page_index = [0]

    line_len = int(curses.COLS*(1/2) - 5)

    message_bottom_y = messages_area_bottom_y - 3

    reversed_message = message_buffer[current_conversation][::-1]

    for message in reversed_message:

        # Calculate the number of lines in the message
        line_num = int(math.ceil(len(message[1])/line_len))

        if (message_bottom_y - 3 - line_num) < 3:
            # append the index of the bottom message of the new page by adding 1 to 
            # the index of the top message of the last page
            page_index.append(reversed_message.index(message))
            message_bottom_y = messages_area_bottom_y - 3

        message_bottom_y = message_bottom_y - 3 - line_num
