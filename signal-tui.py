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
#!/usr/bin/env python3
import curses, traceback, os, string
from os import system

#-- Define the appearance of some interface elements
hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
menu_attr = curses.A_NORMAL

#-- Define additional constants
EXIT = 0
CONTINUE = 1

#-- Give screen module scope
screen = None

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

#-- Create the topbar menu
def topbar_menu(menus):
    left = 2
    for menu in menus:
        menu_name = menu[0]
        menu_hotkey = menu_name[0]
        menu_no_hot = menu_name[1:]
        screen.addstr(1, left, menu_hotkey, hotkey_attr)
        screen.addstr(1, left+1, menu_no_hot, menu_attr)
        left = left + len(menu_name) + 3
        # Add key handlers for this hotkey
        topbar_key_handler((menu_hotkey.upper(), menu[1]))
        topbar_key_handler((menu_hotkey.lower(), menu[1]))
    # Little aesthetic thing to display application title
    screen.addstr(1, left-1,
                  ">"*(52-left)+ " signal-tui",
                  curses.A_STANDOUT)
    screen.refresh()

#-- Magic key handler both loads and processes keys strokes
def topbar_key_handler(key_assign=None, key_dict={}):
    if key_assign:
        key_dict[ord(key_assign[0])] = key_assign[1]
    else:
        c = screen.getch()
        if c in (curses.KEY_END, ord('!')):
            return 0
        elif c not in key_dict.keys():
            curses.beep()
            return 1
        else:
            return eval(key_dict[c])

#-- Display the currently selected options
def draw_dict():
    screen.addstr(5,33, " "*43, curses.A_NORMAL)
    screen.addstr(8,33, " "*43, curses.A_NORMAL)
    screen.addstr(11,33, " "*43, curses.A_NORMAL)
    screen.addstr(14,33, " "*43, curses.A_NORMAL)
    screen.addstr(5, 33, cfg_dict['source'], curses.A_STANDOUT)
    screen.addstr(8, 33, cfg_dict['target'], curses.A_STANDOUT)
    screen.addstr(11,33, cfg_dict['type'], curses.A_STANDOUT)
    screen.addstr(14,33, cfg_dict['proxy'], curses.A_STANDOUT)
    screen.addstr(17,33, str(counter), curses.A_STANDOUT)
    screen.refresh()



#############
##Interface##
#############

def main(stdscr):
    # Frame the interface area at fixed VT100 size
    global screen
    screen = stdscr.subwin(23, 79, 0, 0)
    screen.box()
    screen.hline(2, 1, curses.ACS_HLINE, 77)
    screen.refresh()

    # Define the topbar menus
    file_menu = ("Register", "register()")
    proxy_menu = ("Verify", "verify()")
    doit_menu = ("Send message", "send_message()")
    help_menu = ("Check messages", "check_messages()")
    exit_menu = ("Exit", "EXIT")
    # Add the topbar menus to screen object
    topbar_menu((file_menu, proxy_menu, doit_menu,
                 help_menu, exit_menu))

    # Enter the topbar menu loop
    while topbar_key_handler():
        draw_dict()

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
