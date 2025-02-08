from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="dbms_project"
)
cursor = db.cursor()

# Add student route
@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    roll_no = data['Roll_no']
    name = data['Name']
    branch = data['Branch']
    sem = data['Sem']
    cgpa = data['CGPA']
    hobby = data['Hobby']

    # Check if roll_no exists
    cursor.execute("SELECT * FROM students WHERE Roll_no = %s", (roll_no,))
    existing = cursor.fetchone()
    if existing:
        return jsonify({"message": "Roll No already exists!"}), 400

    # Insert data
    query = "INSERT INTO students (Roll_no, Name, Branch, Sem, CGPA, Hobby) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (roll_no, name, branch, sem, cgpa, hobby)
    cursor.execute(query, values)
    db.commit()

    return jsonify({"message": "Student added successfully!"})

# Get student details
@app.route('/get_student', methods=['GET'])
def get_student():
    roll_no = request.args.get('Roll_no')

    cursor.execute("SELECT * FROM students WHERE Roll_no = %s", (roll_no,))
    student = cursor.fetchone()

    if student:
        student_data = {
            "Roll_no": student[0],
            "Name": student[1],
            "Branch": student[2],
            "Sem": student[3],
            "CGPA": student[4],
            "Hobby": student[5]
        }
        return jsonify(student_data)
    else:
        return jsonify({"message": "Student not found!"}), 404

# Delete student route
@app.route('/delete_student', methods=['DELETE'])
def delete_student():
    roll_no = request.args.get('Roll_no')

    # Check if the student exists
    cursor.execute("SELECT * FROM students WHERE Roll_no = %s", (roll_no,))
    student = cursor.fetchone()

    if student:
        cursor.execute("DELETE FROM students WHERE Roll_no = %s", (roll_no,))
        db.commit()
        return jsonify({"message": "Student deleted successfully!"})
    else:
        return jsonify({"message": "Student not found!"}), 404

# Update student route
@app.route('/update_student', methods=['PUT'])
def update_student():
    roll_no = request.args.get('Roll_no')
    data = request.json
    
    # Check if the student exists
    cursor.execute("SELECT * FROM students WHERE Roll_no = %s", (roll_no,))
    student = cursor.fetchone()

    if student:
        # Extract updated data
        name = data.get('Name', student[1])  # If Name is not provided, keep the existing one
        branch = data.get('Branch', student[2])  # If Branch is not provided, keep the existing one
        sem = data.get('Sem', student[3])  # If Sem is not provided, keep the existing one
        cgpa = data.get('CGPA', student[4])  # If CGPA is not provided, keep the existing one
        hobby = data.get('Hobby', student[5])  # If Hobby is not provided, keep the existing one

        # Update student data
        query = """
        UPDATE students 
        SET Name = %s, Branch = %s, Sem = %s, CGPA = %s, Hobby = %s 
        WHERE Roll_no = %s
        """
        values = (name, branch, sem, cgpa, hobby, roll_no)
        cursor.execute(query, values)
        db.commit()

        return jsonify({"message": "Student details updated successfully!"})
    else:
        return jsonify({"message": "Student not found!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
