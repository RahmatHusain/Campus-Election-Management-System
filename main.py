print("===================================")
print(" UNIVERSITY ELECTION VOTING SYSTEM ")
print("===================================")

import json
import os
import getpass
import hashlib

CANDIDATE_FILE = "candidates.json"

STUDENT_FILE = "students.json"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def load_candidates():

    if os.path.exists(CANDIDATE_FILE):

        try:

            with open(CANDIDATE_FILE, "r") as file:
                return json.load(file)

        except json.JSONDecodeError:
            return []

    return []

def save_candidates(candidates):

    with open(CANDIDATE_FILE, "w") as file:
        json.dump(candidates, file, indent=4)

def admin_login():

    username = input("Username: ")

    password = getpass.getpass("Password: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

        print("✅ Login Successful")

        return True

    print("❌ Invalid Credentials")

    return False

def register_candidate():

    candidates = load_candidates()

    name = input("Candidate Name: ")

    department = input("Department: ")

    candidates.append({

        "name": name,

        "department": department,

        "votes": 0

    })

    save_candidates(candidates)

    print("✅ Candidate Registered")

def view_candidates():

    candidates = load_candidates()

    if not candidates:

        print("No Candidates Registered.")

        return

    print("\nRegistered Candidates\n")

    for candidate in candidates:

        print(f"Name: {candidate['name']}")

        print(f"Department: {candidate['department']}")

        print("-" * 30)

def load_students():

    if os.path.exists(STUDENT_FILE):

        try:
            with open(STUDENT_FILE, "r") as file:
                return json.load(file)

        except json.JSONDecodeError:
            return []

    return []

def save_students(students):

    with open(STUDENT_FILE, "w") as file:
        json.dump(students, file, indent=4)

def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()

def register_student():

    students = load_students()

    student_id = input("Student ID: ")
    name = input("Student Name: ")
    department = input("Department: ")
    password = input("Password: ")

    for student in students:

        if student["student_id"] == student_id:

            print("❌ Student ID already exists.")

            return

    students.append({

        "student_id": student_id,
        "name": name,
        "department": department,
        "password": hash_password(password),
        "has_voted": False

    })

    save_students(students)

    print("✅ Student Registered Successfully")

def student_login():

    student_id = input("Student ID: ")
    password = input("Password: ")

    students = load_students()

    for student in students:

        if (
            student["student_id"] == student_id
            and student["password"] == hash_password(password)
        ):

            print(f"✅ Welcome {student['name']}")

            return student

    print("❌ Invalid Student ID or Password")

    return None

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

if admin_login():
    admin_menu()

    def student_menu():

    while True:

        print("\n===== STUDENT MENU =====")

        print("1. Login")

        print("2. Back")

        choice = input("Choose: ")

        if choice == "1":

            student_login()

        elif choice == "2":

            break

        else:

            print("Invalid Choice")

while True:

    print("\n===== UNIVERSITY ELECTION SYSTEM =====")

    print("1. Admin Login")
    print("2. Student Registration")
    print("3. Student Login")
    print("4. Exit")