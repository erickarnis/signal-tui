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
