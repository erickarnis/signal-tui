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