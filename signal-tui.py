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

#Signal-tui modules
import login
import messages
import contacts
import settings
import signal_cli_wrapper

# Define the appearance of some interface elements
hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
menu_attr = curses.A_NORMAL

# Define additional constants
EXIT = 0
CONTINUE = 1

# Give screen module scope
screen = None

# Define the topbar menus
menu_items = ["Messages", "Contacts", "Settings", "Exit"]

# variables that define the state of the program
current_screen = "login"

current_conversation = 0

contact_buffer = []
message_buffer = []

# fills a box with the given coordinates with spaces
def erase(top_x, top_y, bottom_x, bottom_y):
    for x in range(top_x, bottom_x):
        for y in range(top_y, bottom_y):
            screen.addstr(y, x, " ")

    screen.refresh()


####################
##### Top Menu #####
####################

def draw_top_menu():
    left = 6

    for menu_name in menu_items:
        menu_hotkey = menu_name[0]
        menu_no_hot = menu_name[1:]
        offset = int(curses.COLS/10 - len(menu_name)/2)
        screen.addstr(1, left + offset, menu_hotkey, hotkey_attr)
        screen.addstr(1, left + offset + 1, menu_no_hot, menu_attr)
        left = left + int(curses.COLS/5)

    # Draw application title
    offset = int(curses.COLS - len("signal-tui"))
    screen.addstr(1, offset - 3, "signal-tui", curses.A_STANDOUT)

    #bottom line of menu area
    screen.hline(2, 2, curses.ACS_HLINE, curses.COLS - 4)

    screen.refresh()


##############
#### Main ####
##############

def main(stdscr):

    global screen, contact_buffer, message_buffer, current_conversation, current_screen
    screen = stdscr
    screen.box()
    screen.refresh()

    # Start the program
    if login.open_login_screen(screen, 0):
        screen.clear()
        draw_top_menu()
        screen.border(0)
        contact_buffer = contacts.import_contacts(screen)
        message_buffer = messages.import_messages()
        messages.open_messages_screen(screen, 0, contact_buffer)
        current_screen = "messages"
        curses.curs_set(False)

    # This loop controls the hotkeys. Pressing e will exit the loop and the program
    key_struck = 0
    while key_struck != ord("e"):
        #global current_conversation
        key_struck = screen.getch()

        # These hotkeys should be available from every screen
        if key_struck == ord("m"):
            erase(1, 3, curses.COLS - 1, curses.LINES - 1)
            messages.open_messages_screen(screen, current_conversation, contact_buffer)
            current_screen = "messages"

        elif key_struck == ord("c"):
            current_screen = "contacts"
            erase(1, 3, curses.COLS - 1, curses.LINES - 1)
            contacts.open_contacts_screen(screen)

        elif key_struck == ord("s"):
            current_screen = "settings"
            erase(1, 3, curses.COLS - 1, curses.LINES - 1)
            settings.open_settings_screen(screen)

        if current_screen == "messages":
            if key_struck == ord("i"):
                messages.write_message(current_conversation)

            elif key_struck == ord("h"):
                if current_conversation != len(contact_buffer) - 1:
                    current_conversation += 1
                    messages.open_messages_screen(screen, current_conversation, contact_buffer)

            elif key_struck == ord("j"):
                messages.page_down(current_conversation)

            elif key_struck == ord("k"):
                messages.page_up(current_conversation)

            elif key_struck == ord("l"):
                if current_conversation != 0:
                    current_conversation -= 1
                    messages.open_messages_screen(screen, current_conversation, contact_buffer)

        elif current_screen == "contacts":
            if key_struck == ord("i"):
                contacts.edit_contact()

            elif key_struck == ord("a"):
                contacts.add_contact()

            elif key_struck == ord("h"):
                contacts.left()

            elif key_struck == ord("j"):
                contacts.down()

            elif key_struck == ord("k"):
                contacts.up()

            elif key_struck == ord("l"):
                contacts.right()

        elif current_screen == "settings":
            if key_struck == ord("i"):
                settings.edit_setting()

            elif key_struck == ord("j"):
                settings.down()

            elif key_struck == ord("k"):
                settings.up()


if __name__ == '__main__':
    try:
        # Initialize curses
        stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
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

    # If something goes wrong, restore terminal and report exception
    except:
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        # Print the exception
        traceback.print_exc()
