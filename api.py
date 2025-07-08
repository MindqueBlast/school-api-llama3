from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy data
teachers = [
    {"id": 1, "name": "Mr. Smith", "subject": "Math"},
    {"id": 2, "name": "Ms. Johnson", "subject": "English"},
    {"id": 3, "name": "Mrs. Lee", "subject": "Science"},
    {"id": 4, "name": "Mr. Brown", "subject": "History"},
    {"id": 5, "name": "Ms. Green", "subject": "Art"},
]

students = [
    {"id": 101, "name": "Alice", "grade": 11},
    {"id": 102, "name": "Bob", "grade": 10},
    {"id": 103, "name": "Charlie", "grade": 12},
    {"id": 104, "name": "David", "grade": 11},
    {"id": 105, "name": "Eva", "grade": 9},
]

grades = [
    {"student_id": 101, "subject": "Math", "grade": "A"},
    {"student_id": 101, "subject": "Science", "grade": "B"},
    {"student_id": 102, "subject": "English", "grade": "B"},
    {"student_id": 103, "subject": "History", "grade": "A"},
    {"student_id": 104, "subject": "Math", "grade": "C"},
    {"student_id": 105, "subject": "Art", "grade": "A"},
]

schedule = [
    {"day": "Monday", "classes": ["Math", "English", "History"]},
    {"day": "Tuesday", "classes": ["Science", "Math", "PE"]},
    {"day": "Wednesday", "classes": ["English", "Art", "History"]},
    {"day": "Thursday", "classes": ["Math", "Science", "PE"]},
    {"day": "Friday", "classes": ["History", "Art", "English"]},
]

budget = {
    "year": 2025,
    "total": 500000,
    "spent": 300000,
    "remaining": 200000,
    "categories": {
        "staff": 250000,
        "facilities": 100000,
        "supplies": 50000,
        "activities": 100000
    }
}

# --------- Teacher Routes ---------

@app.route("/api/teachers", methods=["GET"])
def get_teachers():
    return jsonify(teachers)

@app.route("/api/teachers/<int:teacher_id>", methods=["GET"])
def get_teacher(teacher_id):
    teacher = next((t for t in teachers if t["id"] == teacher_id), None)
    if teacher:
        return jsonify(teacher)
    return jsonify({"error": "Teacher not found"}), 404

@app.route("/api/teachers/<int:teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
    global teachers
    teachers = [t for t in teachers if t["id"] != teacher_id]
    return jsonify({"message": f"Teacher {teacher_id} deleted"}), 200

@app.route("/api/teachers/<int:teacher_id>", methods=["PUT"])
def update_teacher(teacher_id):
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid input"}), 400
    for t in teachers:
        if t["id"] == teacher_id:
            t.update(data)
            return jsonify(t), 200
    return jsonify({"error": "Teacher not found"}), 404

# --------- Student Routes ---------

@app.route("/api/students", methods=["GET"])
def get_students():
    grade = request.args.get('gradeLevel')
    if grade:
        filtered = [s for s in students if str(s.get("grade")) == grade]
        return jsonify(filtered)
    return jsonify(students)

@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    if (student := next((s for s in students if s["id"] == student_id), None)):
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    return jsonify({"message": f"Student {student_id} deleted"}), 200

@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid input"}), 400
    for s in students:
        if s["id"] == student_id:
            s.update(data)
            return jsonify(s), 200
    return jsonify({"error": "Student not found"}), 404

# --------- Grades Routes ---------

@app.route("/api/grades", methods=["GET"])
def get_grades():
    student_id = request.args.get("student_id")
    if student_id:
        filtered = [g for g in grades if str(g.get("student_id")) == student_id]
        return jsonify(filtered)
    return jsonify(grades)

@app.route("/api/grades/<int:student_id>", methods=["DELETE"])
def delete_grades_for_student(student_id):
    global grades
    grades = [g for g in grades if g["student_id"] != student_id]
    return jsonify({"message": f"Grades for student {student_id} deleted"}), 200

@app.route("/api/grades/<int:student_id>", methods=["PUT"])
def update_grades_for_student(student_id):
    data = request.json  # expect list of grades or one grade
    global grades
    # remove existing grades for student
    grades = [g for g in grades if g["student_id"] != student_id]
    # add new grades
    if isinstance(data, list):
        for g in data:
            grades.append({"student_id": student_id, **g})
    else:
        grades.append({"student_id": student_id, **data})
    return jsonify({"message": f"Grades for student {student_id} updated"}), 200

# --------- Schedule Routes ---------

@app.route("/api/schedule", methods=["GET"])
def get_schedule():
    day = request.args.get("day")
    if day:
        filtered = [s for s in schedule if s["day"].lower() == day.lower()]
        return jsonify(filtered)
    return jsonify(schedule)

@app.route("/api/schedule/<string:day>", methods=["DELETE"])
def delete_schedule_day(day):
    global schedule
    schedule = [s for s in schedule if s["day"].lower() != day.lower()]
    return jsonify({"message": f"Schedule for {day} deleted"}), 200

@app.route("/api/schedule/<string:day>", methods=["PUT"])
def update_schedule_day(day):
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid input"}), 400
    for s in schedule:
        if s["day"].lower() == day.lower():
            s.update(data)
            return jsonify(s), 200
    return jsonify({"error": "Schedule day not found"}), 404

# --------- Budget Routes ---------

@app.route("/api/budget", methods=["GET"])
def get_budget():
    return jsonify(budget)

@app.route("/api/budget", methods=["PUT"])
def update_budget():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid input"}), 400
    budget.update(data)
    return jsonify(budget), 200


if __name__ == "__main__":
    app.run(port=5001)
