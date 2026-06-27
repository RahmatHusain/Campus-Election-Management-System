from auth import admin_login
from auth import student_login

from admin import register_candidate
from admin import view_candidates

from student import register_student


def admin_menu():

    while True:

        print("\n===== ADMIN MENU =====")
        print("1. Register Candidate")
        print("2. View Candidates")
        print("3. Logout")

        choice = input("Choose: ")

        if choice == "1":
            register_candidate()

        elif choice == "2":
            view_candidates()

        elif choice == "3":
            break

        else:
            print("Invalid Choice")


while True:

    print("\n===== UNIVERSITY ELECTION SYSTEM =====")
    print("1. Admin Login")
    print("2. Student Registration")
    print("3. Student Login")
    print("4. Exit")

    choice = input("Choose: ")

    if choice == "1":

        if admin_login():
            admin_menu()

    elif choice == "2":
        register_student()

    elif choice == "3":
        student_login()

    elif choice == "4":
        print("Thank you for using the system.")
        break

    else:
        print("Invalid Choice")