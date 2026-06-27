import json
import os


def load_data(filename):
    """Load data from a JSON file."""
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    return []


def save_data(filename, data):
    """Save data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def append_data(filename, record):

    data = load_data(filename)

    data.append(record)

    save_data(filename, data)