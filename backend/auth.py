from backend.database import get_connection

def assign_class_group(student_class):
    if student_class in [9, 10]:
        return "Group_1"
    elif student_class in [11, 12]:
        return "Group_2"
    else:
        return "Unknown"

def register_student(name, roll_no, student_class, password):
    class_group = assign_class_group(student_class)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students (name, roll_no, class_group, password)
    VALUES (?, ?, ?, ?)
    """, (name, roll_no, class_group, password))

    conn.commit()
    conn.close()

    return {
        "message": "Student registered successfully",
        "class_group": class_group
    }
def login_student(roll_no, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, name, class_group FROM students
    WHERE roll_no = ? AND password = ?
    """, (roll_no, password))

    student = cursor.fetchone()
    conn.close()

    if student:
        return {
            "message": "Login successful",
            "student_id": student[0],
            "name": student[1],
            "class_group": student[2]
        }
    else:
        return {
            "message": "Invalid roll number or password"
        }
