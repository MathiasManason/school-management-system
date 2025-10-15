from flask import Flask, render_template, request, redirect, url_for, make_response, Response
from students.student_manager import students, add_student
from teachers.teacher_manager import teachers, add_teacher
from classes.class_manager import classes, add_class
from attendance.attendance_manager import attendance_records
from grades.grade_manager import grades, add_grade, edit_grade, delete_grade, calculate_grade_letter

import csv
from datetime import datetime

app = Flask(__name__)

# --------------------
# Home Route
# --------------------
@app.route('/')
def home():
    return render_template('home.html')


# --------------------
# Student Routes
# --------------------
@app.route('/students', methods=['GET', 'POST'])
def manage_students():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        grade = request.form.get('grade')
        if name and age and grade:
            add_student(name, age, grade)
            return redirect(url_for('manage_students'))
    return render_template('students.html', students=students)


@app.route('/students/edit/<int:index>', methods=['GET', 'POST'])
def edit_student(index):
    student = students[index]
    if request.method == 'POST':
        student['name'] = request.form.get('name')
        student['age'] = request.form.get('age')
        student['grade'] = request.form.get('grade')
        return redirect(url_for('manage_students'))
    return render_template('edit_student.html', student=student, index=index)


@app.route('/students/delete/<int:index>')
def delete_student(index):
    if 0 <= index < len(students):
        students.pop(index)
    return redirect(url_for('manage_students'))


# --------------------
# Teacher Routes
# --------------------
@app.route('/teachers', methods=['GET', 'POST'])
def manage_teachers():
    if request.method == 'POST':
        name = request.form.get('name')
        subject = request.form.get('subject')
        experience = request.form.get('experience')
        if name and subject and experience:
            add_teacher(name, subject, experience)
            return redirect(url_for('manage_teachers'))
    return render_template('teachers.html', teachers=teachers)


@app.route('/teachers/edit/<int:index>', methods=['GET', 'POST'])
def edit_teacher(index):
    teacher = teachers[index]
    if request.method == 'POST':
        teacher['name'] = request.form.get('name')
        teacher['subject'] = request.form.get('subject')
        teacher['experience'] = request.form.get('experience')
        return redirect(url_for('manage_teachers'))
    return render_template('edit_teacher.html', teacher=teacher, index=index)


@app.route('/teachers/delete/<int:index>')
def delete_teacher(index):
    if 0 <= index < len(teachers):
        teachers.pop(index)
    return redirect(url_for('manage_teachers'))


# --------------------
# Class Routes
# --------------------
@app.route('/classes', methods=['GET', 'POST'])
def manage_classes():
    if request.method == 'POST':
        name = request.form.get('name')
        teacher = request.form.get('teacher')
        students_str = request.form.get('students')
        student_list = [s.strip() for s in students_str.split(',')] if students_str else []

        if name and teacher:
            add_class(name, teacher, student_list)
            return redirect(url_for('manage_classes'))

    return render_template('classes.html', classes=classes, teachers=teachers)


@app.route('/classes/edit/<int:index>', methods=['GET', 'POST'])
def edit_class(index):
    school_class = classes[index]
    if request.method == 'POST':
        school_class['name'] = request.form.get('name')
        school_class['teacher'] = request.form.get('teacher')
        students_str = request.form.get('students')
        school_class['students'] = [s.strip() for s in students_str.split(',')] if students_str else []
        return redirect(url_for('manage_classes'))
    return render_template('edit_class.html', school_class=school_class, index=index)


@app.route('/classes/delete/<int:index>')
def delete_class(index):
    if 0 <= index < len(classes):
        classes.pop(index)
    return redirect(url_for('manage_classes'))


# --------------------
# Attendance Routes
# --------------------
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    selected_class = None
    if request.method == 'POST':
        class_name = request.form.get('class_name')
        selected_class = next((c for c in classes if c['name'] == class_name), None)
    return render_template(
        'attendance.html',
        classes=classes,
        selected_class=selected_class,
        attendance_records=attendance_records
    )


@app.route('/attendance/save/<class_name>', methods=['POST'])
def save_attendance(class_name):
    present_students = request.form.getlist('present_students')
    attendance_records.append({
        'class': class_name,
        'present_students': present_students,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return redirect(url_for('attendance'))


@app.route('/attendance/export')
def export_attendance():
    response = make_response()
    response.headers['Content-Disposition'] = 'attachment; filename=attendance_records.csv'
    response.headers['Content-Type'] = 'text/csv'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Class', 'Present Students'])

    for record in attendance_records:
        writer.writerow([
            record.get('date', 'N/A'),
            record['class'],
            ', '.join(record['present_students'])
        ])

    return response


# --------------------
# Grades Routes (with Export)
# --------------------
@app.route('/grades', methods=['GET', 'POST'])
def manage_grades():
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        subject = request.form.get('subject')
        score = request.form.get('score')
        term = request.form.get('term')
        remarks = request.form.get('remarks')

        if student_name and subject and score and term:
            add_grade(student_name, subject, score, term, remarks)
            return redirect(url_for('manage_grades'))

    # Calculate grade letters for each entry
    for g in grades:
        g["grade_letter"] = calculate_grade_letter(g["score"])

    return render_template('grades.html', grades=grades, students=students, teachers=teachers)


@app.route('/grades/edit/<int:index>', methods=['GET', 'POST'])
def edit_grade_route(index):
    grade = grades[index]
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        subject = request.form.get('subject')
        score = request.form.get('score')
        term = request.form.get('term')
        remarks = request.form.get('remarks')

        edit_grade(index, student_name, subject, score, term, remarks)
        return redirect(url_for('manage_grades'))

    return render_template('edit_grade.html', grade=grade, index=index)


@app.route('/grades/delete/<int:index>')
def delete_grade_route(index):
    delete_grade(index)
    return redirect(url_for('manage_grades'))


@app.route('/grades/export')
def export_grades():
    # Direct CSV download to local memory
    def generate():
        data = [['Student Name', 'Subject', 'Score', 'Grade Letter', 'Term', 'Remarks']]
        for g in grades:
            data.append([
                g['student_name'],
                g['subject'],
                g['score'],
                calculate_grade_letter(g['score']),
                g['term'],
                g['remarks']
            ])
        return '\n'.join([','.join(map(str, row)) for row in data])

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=grades_export.csv"}
    )


# --------------------
# Run App
# --------------------
if __name__ == '__main__':
    app.run(debug=True)
