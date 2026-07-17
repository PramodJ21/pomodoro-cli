import sqlite3

import db
import session


def ask_session_input():
    while 1:
        work_duration = 0
        break_duration = 0
        print("Select a timer")
        print("1. 25/5")
        print("2. 50/10")
        print("3. 75/15")
        print("4. 110/20")
        print("5. Custom")
        choice = input("Choice: ")

        if choice == "1":
            work_duration = 25*60
            break_duration = 5*60
            break
        elif choice == "2":
            work_duration = 50*60
            break_duration = 10*60
            break
        elif choice == "3":
            work_duration = 75*60
            break_duration = 15*60
            break
        elif choice == "4":
            work_duration = 110*60
            break_duration = 20*60
            break
        elif choice == "5":
            while 1:
                try:
                    work_duration = int(input("Enter work duration"))
                    break
                except ValueError:
                    print("Please enter an integer")

            while 1:
                try:
                    break_duration = int(input("Enter break duration"))
                    break
                except ValueError:
                    print("Please enter an integer")

            break

    return (work_duration,break_duration)

def main(connection: sqlite3.Connection):
    print()
    duration = ask_session_input()
    work_duration = duration[0]
    break_duration = duration[1]

    session.start_session(connection=connection, break_duration=break_duration, work_duration=work_duration)

    user_continue = input("Start a new session (y/n): ")
    return user_continue

connection = db.get_connection()
db.initialize_db(connection=connection)

while True:
    print("Choose an option: ")
    print("1. Start a session")
    print("2. Show Session Stats")
    print("3. Exit")
    print()
    choice = input("Option: ")

    if choice == "1":
        while True:
            user_continue = main(connection)
            if user_continue != "y":
                break
    elif choice == "2":
        print()
        session.show_statistics(connection=connection)
        print()
    elif choice == "3":
        break
    else:
        print("Choose a valid choice")
        print()
