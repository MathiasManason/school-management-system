# classes/class_manager.py

classes = []

def add_class(name, teacher, students):
    new_class = {
        "name": name,
        "teacher": teacher,
        "students": students
    }
    classes.append(new_class)
