"""Student Attendance Cleaner.

Reads attendance.txt, cleans and de-duplicates the names,
and saves the sorted result to attendance_clean.csv.
"""

import csv

INPUT_FILE = "attendance.txt"
OUTPUT_FILE = "attendance_clean.csv"


def read_names(filename=INPUT_FILE):
    """Return the non-blank lines of the attendance file."""
    with open(filename, encoding="utf-8") as f:
        return [line for line in f if line.strip()]


def clean_names(raw_names):
    """Remove extra spaces and normalize capitalization."""
    return [" ".join(name.strip().split()).title() for name in raw_names]


def save_clean(names, filename=OUTPUT_FILE):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["student_name"])
        writer.writerows([name] for name in names)


def main():
    try:
        raw_names = read_names()
    except FileNotFoundError:
        print(f"Error: '{INPUT_FILE}' was not found. Place it in the same folder.")
        return

    if not raw_names:
        print(f"'{INPUT_FILE}' has no student names.")
        return

    cleaned = clean_names(raw_names)       # list comprehension
    unique_students = set(cleaned)         # set removes duplicates
    final_list = sorted(unique_students)   # alphabetical order

    save_clean(final_list)

    print(f"Original records : {len(raw_names)}")
    print(f"Unique students  : {len(unique_students)}")
    print(f"Saved to         : {OUTPUT_FILE}\n")
    print("Cleaned attendance list:")
    for i, name in enumerate(final_list, start=1):
        print(f"{i:>3}. {name}")


if __name__ == "__main__":
    main()
