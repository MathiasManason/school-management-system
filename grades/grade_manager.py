import csv
import os

# Path to store the grades file
GRADES_FILE = "grades.csv"

# In-memory list to hold all grade data
grades = []




def load_grades():
    """Load grades from the CSV file if it exists."""
    global grades
    if os.path.exists(GRADES_FILE):
        with open(GRADES_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            grades = [
                {
                    "student_name": row["student_name"],
                    "subject": row["subject"],
                    "score": float(row["score"]),
                    "term": row.get("term", ""),
                    "remarks": row.get("remarks", ""),
                }
                for row in reader
            ]
    else:
        grades = []


def save_grades():
    """Save the grades list to the CSV file."""
    with open(GRADES_FILE, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["student_name", "subject", "score", "term", "remarks"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for g in grades:
            writer.writerow(g)


def add_grade(student_name, subject, score, term="", remarks=""):
    """Add a new grade and save automatically."""
    grades.append({
        "student_name": student_name,
        "subject": subject,
        "score": float(score),
        "term": term,
        "remarks": remarks
    })
    save_grades()


def edit_grade(index, student_name, subject, score, term, remarks):
    """Edit an existing grade entry."""
    if 0 <= index < len(grades):
        grades[index] = {
            "student_name": student_name,
            "subject": subject,
            "score": float(score),
            "term": term,
            "remarks": remarks
        }
        save_grades()


def delete_grade(index):
    """Delete a grade by index."""
    if 0 <= index < len(grades):
        grades.pop(index)
        save_grades()


def calculate_grade_letter(score):
    """Return a letter grade based on score."""
    score = float(score)
    if score >= 70:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 40:
        return "D"
    else:
        return "F"


# Load data automatically when the module imports
load_grades()
