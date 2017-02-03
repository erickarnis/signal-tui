'''
 ____  __ __ _     _       ___ ______ ____ ____           __ _     ____ 
|    \|  |  | |   | |     /  _|      |    |    \         /  | |   |    |
|  o  |  |  | |   | |    /  [_|      ||  ||  _  |_____  /  /| |    |  | 
|     |  |  | |___| |___|    _|_|  |_||  ||  |  |     |/  / | |___ |  | 
|  O  |  :  |     |     |   [_  |  |  |  ||  |  |_____/   \_|     ||  | 
|     |     |     |     |     | |  |  |  ||  |  |     \     |     ||  | 
|_____|\__,_|_____|_____|_____| |__| |____|__|__|      \____|_____|____|

By Eric Karnis and Thales Ferria
'''
#!/usr/bin/env python
import os
from os import system
import curses

#global variables
username = "+16477798191"

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

#Main functionality

#working
def register():
    curses.endwin()
    execute_cmd("signal-cli -u " + username + " register")
#working
def verify(verification_number):
    curses.endwin()
    #not sure why username has to be cast to string here, but not in register
    execute_cmd("signal-cli -u " + username + " verify " + str(verification_number))

#TODO works
def send_message(recipient, message):
    curses.endwin()
    execute_cmd("signal-cli -u " + username + " send -m \"" + message + "\"[" + recipient + "]")

#TODO
def check_messages():
    curses.endwin()
    execute_cmd("signal-cli -u " + str(username) + " receive")

#startup functions
def user_data_open():
	if( file_is_empty("user_data.txt") ):
		user_data = open("user_data.txt", "w+")
	else: 
		user_data = open("user_data.txt", "r+")
	print "Opening mode : ", user_data.mode
	user_data.close()




#main
#TODO make register write to encrypted file, make main check for file on startup
user_data_open()
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

    if x == ord('1'):
        global username
    	username = get_param("Enter your phone number with country code eg for canada +16477798192") 
    	register()
    if x == ord('2'):
        verification_number = get_param("Enter verification code that should have been texted to your phone")
    	verify(verification_number)
    if x == ord('3'):
        recipient = get_param("Enter recipient's phone number with country code eg for canada +16477798192") 
    	message = get_param("Enter message") 
    	send_message(recipient, message)
    if x == ord('4'): 
    	check_messages()

curses.endwin()