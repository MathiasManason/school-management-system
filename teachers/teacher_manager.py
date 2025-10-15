# teachers/teacher_manager.py

teachers = []

def add_teacher(name, subject, experience):
    teacher = {
        "name": name,
        "subject": subject,
        "experience": experience
    }
    teachers.append(teacher)
