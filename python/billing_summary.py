import json
import os

TUITION_PER_CREDIT = 300.0
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_json(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r") as f:
        return json.load(f)


def load_students():
    return {s["id"]: s for s in load_json("students.json")}


def load_courses():
    return {c["code"]: c for c in load_json("courses.json")}


def calculate_tuition(student, courses):
    total_credits = 0
    enrolled = student.get("enrolledCourses", [])
    for code in enrolled:
        course = courses.get(code)
        if course:
            total_credits += course["credits"]
    return total_credits * TUITION_PER_CREDIT


def display_billing(student, courses):
    print("=" * 50)
    print(f"  Billing Summary for {student['name']} ({student['id']})")
    print(f"  Major: {student['major']}")
    print("=" * 50)

    enrolled = student.get("enrolledCourses", [])
    if not enrolled:
        print("  No courses enrolled.")
        print(f"\n  Total Tuition: $0.00")
        print("=" * 50)
        return

    print(f"  {'Course':<10} {'Title':<25} {'Credits':>7}")
    print("  " + "-" * 44)

    total_credits = 0
    for code in enrolled:
        course = courses.get(code)
        if course:
            print(f"  {code:<10} {course['title']:<25} {course['credits']:>7}")
            total_credits += course["credits"]

    tuition = total_credits * TUITION_PER_CREDIT
    print("  " + "-" * 44)
    print(f"  {'Total Credits:':<36} {total_credits:>7}")
    print(f"  Rate per credit: ${TUITION_PER_CREDIT:,.2f}")
    print(f"\n  Total Tuition: ${tuition:,.2f}")
    print("=" * 50)


def main():
    students = load_students()
    courses = load_courses()

    print("\n" + "=" * 50)
    print("  Course Enrollment - Billing Summary")
    print("=" * 50)

    student_id = input("\n  Enter Student ID: ").strip()

    student = students.get(student_id)
    if not student:
        print(f"\n  [✗] Student not found: {student_id}")
        return

    print()
    display_billing(student, courses)


if __name__ == "__main__":
    main()
