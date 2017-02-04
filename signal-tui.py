'''
          @@\                               @@\          @@\               @@\ 
          \__|                              @@ |         @@ |              \__|
 @@@@@@@\ @@\  @@@@@@\  @@@@@@@\   @@@@@@\  @@ |       @@@@@@\   @@\   @@\ @@\ 
@@  _____|@@ |@@  __@@\ @@  __@@\  \____@@\ @@ |@@@@@@\\_@@  _|  @@ |  @@ |@@ |
\@@@@@@\  @@ |@@ /  @@ |@@ |  @@ | @@@@@@@ |@@ |\______| @@ |    @@ |  @@ |@@ |
 \____@@\ @@ |@@ |  @@ |@@ |  @@ |@@  __@@ |@@ |         @@ |@@\ @@ |  @@ |@@ |
@@@@@@@  |@@ |\@@@@@@@ |@@ |  @@ |\@@@@@@@ |@@ |         \@@@@  |\@@@@@@  |@@ |
\_______/ \__| \____@@ |\__|  \__| \_______|\__|          \____/  \______/ \__|
              @@\   @@ |                                                       
              \@@@@@@  |                                                       
               \______/     

By Eric Karnis
This will be under gpl someday
'''
#!/usr/bin/env python3
import curses, traceback, os
from os import system

#helper functions
def get_param(prompt_string):
    stdscr.clear()
    stdscr.border(0)
    stdscr.addstr(2, 2, prompt_string)
    stdscr.refresh()
    input = stdscr.getstr(10, 10, 60)
    return input

def execute_cmd(cmd_string):
    system("clear")
    a = system(cmd_string)
    print ("")
    if a == 0:
         print ("Command executed correctly")
    else:
         print ("Command terminated with error")
    raw_input("Press enter")
    print("")

def file_is_empty(path):
    return os.stat(path).st_size==0

#prepare username and user data file
with open('user_data.txt', 'r') as file:
    user_data = file.readlines()

username = user_data[0]

########################
##Signal functionality##
########################

#Registers the user with Whisper Systems. If it works, they will send a
#verification number to the user's phone
def register():
    user_data[0] = username
    with open('user_data.txt', 'w') as file:
        file.writelines( user_data )
    curses.endwin()
    execute_cmd("signal-cli -u " + username + " register")

#Sned's user's verification number to Whisper Systems
def verify(verification_number):
    curses.endwin()
    #not sure why username has to be cast to string here, but not in register
    execute_cmd("signal-cli -u " + username + " verify " + str(verification_number))

#Sends a message to another signal user
def send_message(recipient, message):
    curses.endwin()
    execute_cmd("signal-cli -u " + username + " send -m \"" + message + "\"[" + recipient + "]")

#Checks for unread messages
#TODO have this check periodically and write all messages to a file
def check_messages():
    curses.endwin()
    execute_cmd("signal-cli -u " + str(username) + " receive")

#############
##Interface##
#############

def main(stdscr):
    x = 0
    
    while x != ord('5'):
        stdscr = curses.initscr()
    
        stdscr.clear()
        stdscr.border(0)
        stdscr.addstr(2, 2, "Please enter a number...")
        stdscr.addstr(4, 4, "1 - Register your number")
        stdscr.addstr(5, 4, "2 - Enter verification code")
        stdscr.addstr(6, 4, "3 - Send a message")
        stdscr.addstr(7, 4, "4 - Check messages")
        stdscr.addstr(8, 4, "5 - Exit")
        stdscr.refresh()
    
        x = stdscr.getch()
    
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

#Initialize and call main
if __name__=='__main__':
    try:
        # Initialize curses
        stdscr=curses.initscr()
        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        curses.noecho()
        curses.cbreak()
  
        # In keypad mode, escape sequences for special keys
        # (like the cursor keys) will be interpreted and
        # a special value like curses.KEY_LEFT will be returned
        stdscr.keypad(1)
        # Enter the main loop
        main(stdscr)                    
        # Set everything back to normal
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        # Terminate curses
        curses.endwin()                 

    #If something goes wrong, restore terminal and report exception
    except:
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        #Print the exception
        traceback.print_exc()           
