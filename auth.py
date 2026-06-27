import getpass

from config import ADMIN_USERNAME
from config import ADMIN_PASSWORD
from config import STUDENT_FILE

from database import load_data

from utils import hash_password


def admin_login():

    username = input("Username: ")

    password = getpass.getpass("Password: ")

    if (
        username == ADMIN_USERNAME
        and password == ADMIN_PASSWORD
    ):

        print("✅ Login Successful")

        return True

    print("❌ Invalid Credentials")

    return False


def student_login():

    students = load_data(STUDENT_FILE)

    student_id = input("Student ID: ")

    password = input("Password: ")

    for student in students:

        if (
            student["student_id"] == student_id
            and student["password"] == hash_password(password)
        ):

            print(f"Welcome {student['name']}")

            return student

    print("Invalid Student ID or Password")

    return None