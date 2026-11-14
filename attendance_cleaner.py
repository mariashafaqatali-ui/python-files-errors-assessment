"""
Student Attendance Cleaner
--------------------------
Reads raw student names from attendance.txt, cleans the formatting, removes
duplicates, sorts alphabetically and saves the result to attendance_clean.csv.

Concepts used: file handling, exception handling (FileNotFoundError),
list comprehension, set.
"""

import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "attendance.txt")
OUTPUT_FILE = os.path.join(BASE_DIR, "attendance_clean.csv")


def read_names():
    """Return the non-empty raw lines of attendance.txt."""
    try:
        with open(INPUT_FILE, encoding="utf-8") as file:
            lines = file.read().splitlines()
    except FileNotFoundError:
        print("Error: attendance.txt was not found. Place it next to this script and try again.")
        return None
    return [line for line in lines if line.strip()]  # ignore blank lines


def main():
    raw_names = read_names()
    if raw_names is None:
        return
    if not raw_names:
        print("attendance.txt is empty - nothing to clean.")
        return

    # List comprehension: strip() removes extra spaces, title() fixes capitalization.
    # split()/join() also collapses repeated spaces *inside* a name.
    cleaned = [" ".join(name.strip().split()).title() for name in raw_names]

    # Set: keeps only one copy of every student.
    unique_students = set(cleaned)

    # Sorted alphabetically.
    final_list = sorted(unique_students)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Student Name"])
        writer.writerows([name] for name in final_list)

    print("=" * 40)
    print("   STUDENT ATTENDANCE CLEANER")
    print("=" * 40)
    print(f"Original number of records : {len(raw_names)}")
    print(f"Unique student count       : {len(unique_students)}")
    print(f"Duplicates removed         : {len(raw_names) - len(unique_students)}")
    print("\nCleaned attendance list:")
    for number, name in enumerate(final_list, start=1):
        print(f"  {number:>2}. {name}")
    print(f"\nSaved to {os.path.basename(OUTPUT_FILE)}")


if __name__ == "__main__":
    main()
