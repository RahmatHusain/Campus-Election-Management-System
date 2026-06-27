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