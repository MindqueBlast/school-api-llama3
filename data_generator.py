import json
import random

teachers = list(range(6, 106))
students = list(range(106, 606))
subjects = ["Math", "Science", "History", "Art", "English", "Music", "PE", "Geography", "Biology", "Chemistry"]
grades = ["A", "B", "C", "D", "E", "F"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
budget_fields = ["total", "spent", "remaining"]

def random_teacher():
    tid = random.choice(teachers)
    subj = random.choice(subjects)
    return [
        {
            "instruction": f"Get details of teacher {tid}.",
            "input": "",
            "output": f"GET http://localhost:5001/api/teachers/{tid}"
        },
        {
            "instruction": f"Delete teacher {tid}.",
            "input": "",
            "output": f"DELETE http://localhost:5001/api/teachers/{tid}"
        },
        {
            "instruction": f"Update teacher {tid}'s subject to {subj}.",
            "input": "",
            "output": f"PUT http://localhost:5001/api/teachers/{tid} {{\\\"subject\\\": \\\"{subj}\\\"}}"
        }
    ]

def random_student():
    sid = random.choice(students)
    grade_num = random.randint(9, 12)
    return [
        {
            "instruction": f"Get details of student {sid}.",
            "input": "",
            "output": f"GET http://localhost:5001/api/students/{sid}"
        },
        {
            "instruction": f"Delete student {sid}.",
            "input": "",
            "output": f"DELETE http://localhost:5001/api/students/{sid}"
        },
        {
            "instruction": f"Update student {sid}'s grade to {grade_num}.",
            "input": "",
            "output": f"PUT http://localhost:5001/api/students/{sid} {{\\\"grade\\\": {grade_num}}}"
        }
    ]

def random_grades():
    sid = random.choice(students)
    subj1, subj2 = random.sample(subjects, 2)
    grade1, grade2 = random.sample(grades, 2)
    return [
        {
            "instruction": f"Get all grades for student {sid}.",
            "input": "",
            "output": f"GET http://localhost:5001/api/grades?student_id={sid}"
        },
        {
            "instruction": f"Delete all grades for student {sid}.",
            "input": "",
            "output": f"DELETE http://localhost:5001/api/grades/{sid}"
        },
        {
            "instruction": f"Update grades for student {sid} to {grade1} in {subj1} and {grade2} in {subj2}.",
            "input": "",
            "output": f"PUT http://localhost:5001/api/grades/{sid} [{{\\\"subject\\\": \\\"{subj1}\\\", \\\"grade\\\": \\\"{grade1}\\\"}}, {{\\\"subject\\\": \\\"{subj2}\\\", \\\"grade\\\": \\\"{grade2}\\\"}}]"
        }
    ]

def random_schedule():
    day = random.choice(days)
    classes = random.sample(subjects, 3)
    return [
        {
            "instruction": f"Get schedule for {day}.",
            "input": "",
            "output": f"GET http://localhost:5001/api/schedule?day={day}"
        },
        {
            "instruction": f"Delete schedule for {day}.",
            "input": "",
            "output": f"DELETE http://localhost:5001/api/schedule/{day}"
        },
        {
            "instruction": f"Update schedule for {day} to have {', '.join(classes)}.",
            "input": "",
            "output": f"PUT http://localhost:5001/api/schedule/{day} {{\\\"classes\\\": [\\\"{classes[0]}\\\", \\\"{classes[1]}\\\", \\\"{classes[2]}\\\"]}}"
        }
    ]

def random_budget():
    field = random.choice(budget_fields)
    value = random.randint(100000, 999999)
    return [
        {
            "instruction": f"Update the school budget {field} to {value}.",
            "input": "",
            "output": f"PUT http://localhost:5001/api/budget {{\\\"{field}\\\": {value}}}"
        }
    ]

def random_listings():
    return [
        {
            "instruction": "Get a list of all students.",
            "input": "",
            "output": "GET http://localhost:5001/api/students"
        },
        {
            "instruction": "Get a list of all grades.",
            "input": "",
            "output": "GET http://localhost:5001/api/grades"
        },
        {
            "instruction": "Get the full school schedule.",
            "input": "",
            "output": "GET http://localhost:5001/api/schedule"
        }
    ]

def random_grade_level():
    grade = random.randint(9, 12)
    return [
        {
            "instruction": f"Get all students in grade {grade}.",
            "input": "",
            "output": f"GET http://localhost:5001/api/students?gradeLevel={grade}"
        }
    ]

def random_teacher_list():
    return [
        {
            "instruction": "List all teachers.",
            "input": "",
            "output": "GET http://localhost:5001/api/teachers"
        }
    ]

def random_budget_get():
    return [
        {
            "instruction": "Get the school budget details.",
            "input": "",
            "output": "GET http://localhost:5001/api/budget"
        }
    ]

all_generators = [
    random_teacher, random_student, random_grades, random_schedule,
    random_budget, random_listings, random_grade_level, random_teacher_list, random_budget_get
]

entries = []
while len(entries) < 1000:
    gen = random.choice(all_generators)
    for entry in gen():
        if len(entries) < 1000:
            entries.append(entry)
        else:
            break

with open("synthetic_school_api_data.json", "w") as f:
    json.dump(entries, f, indent=2)