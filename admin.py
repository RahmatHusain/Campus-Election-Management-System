from config import CANDIDATE_FILE

from database import load_data
from database import save_data


def register_candidate():

    candidates = load_data(CANDIDATE_FILE)

    name = input("Candidate Name: ")

    department = input("Department: ")

    candidates.append(
        {
            "name": name,
            "department": department,
            "votes": 0,
        }
    )

    save_data(CANDIDATE_FILE, candidates)

    print("Candidate Registered Successfully")


def view_candidates():

    candidates = load_data(CANDIDATE_FILE)

    if not candidates:

        print("No Candidates Registered")

        return

    print()

    for candidate in candidates:

        print(f"Name       : {candidate['name']}")
        print(f"Department : {candidate['department']}")
        print(f"Votes      : {candidate['votes']}")
        print("-" * 40)