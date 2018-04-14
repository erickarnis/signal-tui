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
import subprocess

from curses.textpad import Textbox, rectangle

phone_number = "+16476952076"

# Registers the user with Whisper Systems. If it works, they will send a
# verification number to the user's phone
def register_device(pnum):
    global phone_number
    phone_number = pnum
    phone_number = "+1" + str(phone_number)
    x = subprocess.run(["signal-cli", "-u", phone_number, "register"])

# Send's user's verification number to Whisper Systems
def verify_code(verification_number):
    verification_number = str(verification_number)
    x = subprocess.run(["signal-cli", "-u", phone_number, "verify", verification_number])

# Sends a message to another signal user
def send_message(recipient, message):
    curses.curs_set(0)
    recipient = "[+1" + str(recipient) + "]"
    x = subprocess.run(["signal-cli", "-u", phone_number, "send", "-m", message, recipient])

# Checks for unread messages
# TODO have this check periodically and write all messages to a file
def check_messages():
    curses.endwin()
    execute_cmd("signal-cli -u " + str(username) + " receive")