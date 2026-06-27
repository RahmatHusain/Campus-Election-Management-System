from config import STUDENT_FILE

from database import load_data
from database import save_data

from utils import hash_password

from config import CANDIDATE_FILE
from config import AUDIT_LOG_FILE

from database import append_data


def register_student():

    students = load_data(STUDENT_FILE)

    student_id = input("Student ID: ")

    for student in students:

        if student["student_id"] == student_id:

            print("Student ID already exists.")

            return

    name = input("Name: ")

    department = input("Department: ")

    password = input("Password: ")

    students.append(
        {
            "student_id": student_id,
            "name": name,
            "department": department,
            "password": hash_password(password),
            "has_voted": False,
        }
    )

    save_data(STUDENT_FILE, students)

    print("Student Registered Successfully")

def student_dashboard(student):

    while True:

        print("\n===== STUDENT DASHBOARD =====")
        print("1. Cast Vote")
        print("2. Logout")

        choice = input("Choose: ")

        if choice == "1":
            cast_vote(student)

        elif choice == "2":
            break

        else:
            print("Invalid Choice")