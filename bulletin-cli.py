#!/usr/bin/env python

from os import system
import curses

username = 0

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
    print ""
    if a == 0:
         print "Command executed correctly"
    else:
         print "Command terminated with error"
    raw_input("Press enter")
    print ""

def register():
    global username
    username = get_param("Enter your phone number with country code eg for canada +16477798192")
    curses.endwin()
    execute_cmd("signal-cli -u " + username + " register")

def verify():
    verification_number = get_param("Enter verification code that should have been texted to your phone")
    curses.endwin()
    #not sure why username has to be cast to string here, but not in register
    execute_cmd("signal-cli -u " + str(username) + " verify " + str(verification_number))

#TODO
def send_message():
	recipient = get_param("Enter reciepient number with country code eg for canada +16477798292")


#TODO
def check_messages():

#main
#TODO make register write to encrypted file, make main check for file on startup
x = 0

while x != ord('5'):
    screen = curses.initscr()

    screen.clear()
    screen.border(0)
    screen.addstr(2, 2, "Please enter a number...")
    screen.addstr(4, 4, "1 - Register your number")
    screen.addstr(5, 4, "2 - Enter verification code")
    screen.addstr(6, 4, "3 - Send a message")
    screen.addstr(7, 4, "4 - Check messages")
    screen.addstr(8, 4, "5 - Exit")
    screen.refresh()

    x = screen.getch()

    if x == ord('1'): register()
    if x == ord('2'): verify()
    if x == ord('3'): send_message()
    if x == ord('4'): check_messages()

curses.endwin()