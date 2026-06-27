from auth import admin_login
from auth import student_login

from admin import register_candidate
from admin import view_candidates

from student import register_student
from student import student_dashboard

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
        student = student_login()

if student:
    student_dashboard(student)

    elif choice == "4":
        print("Thank you for using the system.")
        break

    else:
        print("Invalid Choice")

def cast_vote(student):

    candidates = load_data(CANDIDATE_FILE)

    print("\n===== Candidates =====")

    for index, candidate in enumerate(candidates, start=1):

        print(f"{index}. {candidate['name']} ({candidate['department']})")

        try:

    choice = int(input("Choose Candidate: "))

except ValueError:

    print("Invalid Choice")

    return

    if choice < 1 or choice > len(candidates):

    print("Candidate does not exist.")

    return

    save_data(CANDIDATE_FILE, candidates)

    if student["has_voted"]:

    print("❌ You have already voted.")

    return
    students = load_data(STUDENT_FILE)

    for s in students:

        if s["student_id"] == student["student_id"]:

            s["has_voted"] = True

    save_data(STUDENT_FILE, students)

    append_data(

        AUDIT_LOG_FILE,

        {
            "student_id": student["student_id"],
            "candidate": candidates[choice - 1]["name"]
        }
    )
    print("\n✅ Vote Cast Successfully!")