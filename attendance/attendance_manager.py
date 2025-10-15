# attendance/attendance_manager.py

attendance_records = []


def mark_attendance(date, class_name, student_name, status):
    attendance_records.append({
        "date": date,
        "class_name": class_name,
        "student_name": student_name,
        "status": status  # 'Present' or 'Absent'
    })


def get_attendance_by_class(class_name):
    return [record for record in attendance_records if record["class_name"] == class_name]


def get_attendance_by_student(student_name):
    return [record for record in attendance_records if record["student_name"] == student_name]
