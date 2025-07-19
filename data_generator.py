import json
import random

NUM_EXAMPLES = 1000
BASE_URL = "http://localhost:5001/api"

# Define categories and patterns
api_templates = {
    "teachers": [
        lambda: ("List all teachers.", "GET {}/teachers".format(BASE_URL)),
        lambda: ("Get details of teacher {}.".format(tid := random.randint(1, 50)), f"GET {BASE_URL}/teachers/{tid}"),
        lambda: ("Delete teacher {}.".format(tid := random.randint(1, 50)), f"DELETE {BASE_URL}/teachers/{tid}"),
        lambda: ("Update teacher {}'s subject to {}.".format(tid := random.randint(1, 50), subj := random.choice(["Math", "Science", "History"])),
                 f"PUT {BASE_URL}/teachers/{tid} {{\"subject\": \"{subj}\"}}"),
    ],
    "students": [
        lambda: ("List all students.", "GET {}/students".format(BASE_URL)),
        lambda: ("Get student {}'s information.".format(sid := random.randint(100, 200)), f"GET {BASE_URL}/students/{sid}"),
        lambda: ("Delete student {}.".format(sid := random.randint(100, 200)), f"DELETE {BASE_URL}/students/{sid}"),
        lambda: ("Add a new student named {}.".format(name := random.choice(["John Doe", "Jane Smith", "Alice", "Bob"])),
                 f"POST {BASE_URL}/students {{\"name\": \"{name}\", \"grade\": {random.randint(1,12)}}}"),
    ],
    "grades": [
        lambda: ("Get grades for student {}.".format(sid := random.randint(100, 200)), f"GET {BASE_URL}/grades?student_id={sid}"),
        lambda: ("Update grade for student {} in subject {}.".format(sid := random.randint(100, 200), subj := random.choice(["Math", "Science", "History"])),
                 f"PUT {BASE_URL}/grades/{sid} {{\"subject\": \"{subj}\", \"grade\": \"{random.choice(['A','B','C'])}\"}}"),
        lambda: ("Delete grades for student {}.".format(sid := random.randint(100, 200)), f"DELETE {BASE_URL}/grades/{sid}"),
    ],
    "schedule": [
        lambda: ("Get schedule for {}.".format(day := random.choice(["Monday", "Tuesday", "Friday"])),
                 f"GET {BASE_URL}/schedule?day={day}"),
        lambda: ("Update schedule for {}.".format(day := random.choice(["Monday", "Tuesday", "Friday"])),
                 f"PUT {BASE_URL}/schedule/{day} {{\"classes\": [\"Math\", \"English\"]}}"),
        lambda: ("Delete schedule for {}.".format(day := random.choice(["Monday", "Tuesday", "Friday"])),
                 f"DELETE {BASE_URL}/schedule/{day}"),
    ],
    "budget": [
        lambda: ("Get the current school budget.", f"GET {BASE_URL}/budget"),
        lambda: ("Update the budget to {} dollars.".format(amt := random.randint(100000, 500000)),
                 f"PUT {BASE_URL}/budget {{\"amount\": {amt}}}"),
        lambda: ("Delete the current budget entry.", f"DELETE {BASE_URL}/budget"),
    ],
}

# Generate dataset
all_examples = []
categories = list(api_templates.keys())

for _ in range(NUM_EXAMPLES):
    category = random.choice(categories)
    example_generator = random.choice(api_templates[category])
    instruction, output = example_generator()
    all_examples.append({
        "instruction": instruction,
        "input": "",
        "output": output
    })

# Save to JSON file
with open("school_api_data.json", "w") as f:
    json.dump(all_examples, f, indent=2)

print("Generated school_api_data.json with", len(all_examples), "examples.")
