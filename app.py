from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from database import mydb
from schemas import Student, Student_update, Course, Teacher, enrolled_course 


import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="fastapi",
        password="abc123",
        database="school_management"
    )


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =========================================================
# POST API - Insert Student
# =========================================================

@app.post("/students")
def create_student(student: Student):

    mycursor = mydb.cursor()

    sql = """
        INSERT INTO student
        (
            studentid,
            username,
            email,
            is_active,
            name,
            age,
            country,
            plan,
            expire_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        student.studentid,
        student.username,
        student.email,
        student.is_active,
        student.name,
        student.age,
        student.country,
        student.plan,
        student.expire_at
    )

    mycursor.execute(sql, values)
    mydb.commit()

    return {
        "message": "Student inserted successfully",
        "rows": mycursor.rowcount
    }

'''
# =========================================================
# GET API - Fetch All Students
# =========================================================

@app.get("/students")
def get_students():

    mycursor = mydb.cursor(dictionary=True)

    sql = "SELECT * FROM student"

    mycursor.execute(sql)

    students = mycursor.fetchall()

    return students  '''
                    


@app.get("/students")
def get_students(
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=100)
):

    print("PAGE:", page, type(page))
    print("LIMIT:", limit, type(limit))

    offset = (page - 1) * limit

    conn = get_connection()

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT *
            FROM student
            ORDER BY studentid
            LIMIT %s OFFSET %s
        """

        cursor.execute(query, (limit, offset))

        students = cursor.fetchall()

        return {
            "current_page": page,
            "limit": limit,
            "students": students
        }

    finally:
        cursor.close()
        conn.close()






# =========================================================
# GET API - Fetch One Student
# =========================================================

@app.get("/students/{studentid}")
def get_student(studentid: int):

    mycursor = mydb.cursor(dictionary=True)

    sql = """
        SELECT *
        FROM student
        WHERE studentid = %s
    """

    mycursor.execute(sql, (studentid,))

    student = mycursor.fetchone()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# =========================================================
# PUT API - Update Student
# =========================================================

@app.put("/students/{studentid}")
def update_student(studentid: int, student: Student_update):

    mycursor = mydb.cursor()

    sql = """
        UPDATE student
        SET
            username = %s,
            email = %s,
            is_active = %s,
            name = %s,
            age = %s,
            country = %s,
            plan = %s,
            expire_at = %s
        WHERE studentid = %s
    """

    values = (
        student.username,
        student.email,
        student.is_active,
        student.name,
        student.age,
        student.country,
        student.plan,
        student.expire_at,
        studentid
    )

    mycursor.execute(sql, values)
    mydb.commit()

    if mycursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student updated successfully",
        "rows": mycursor.rowcount
    }


# =========================================================
# DELETE API - Delete Student
# =========================================================

@app.delete("/student/{studentid}")
def delete_student(studentid: int):

    mycursor = mydb.cursor(dictionary=True)

    # Check whether student exists
    sql = """
        SELECT *
        FROM students
        WHERE studentid = %s
    """

    mycursor.execute(sql, (studentid,))

    student = mycursor.fetchone()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Delete student
    sql = """
        DELETE FROM students
        WHERE studentid = %s
    """

    mycursor.execute(sql, (studentid,))

    mydb.commit()

    return {
        "message": f"Student with ID {studentid} deleted successfully"
    }








# =========================================================
# COURSE MANAGEMENT
# =========================================================

# CREATE Course
@app.post("/courses")
def create_course(course: Course):
    mycursor = mydb.cursor()

    sql = """
        INSERT INTO course (courseId, courseName, semester)
        VALUES (%s, %s, %s)
    """

    values = (
        course.courseId,
        course.courseName,
        course.semester
    )

    mycursor.execute(sql, values)
    mydb.commit()

    return {
        "message": "Course inserted successfully",
        "rows": mycursor.rowcount
    }


# GET All Courses
@app.get("/courses")
def get_courses():
    mycursor = mydb.cursor(dictionary=True)

    sql = "SELECT * FROM course"
    mycursor.execute(sql)

    courses = mycursor.fetchall()
    mycursor.close()

    return courses

# GET COURSE BY ID
@app.get("/course/{courseId}")
def get_course(courseId: int):

    mycursor = mydb.cursor(dictionary=True)

    sql = """
        SELECT *
        FROM courses
        WHERE courseId = %s
    """

    mycursor.execute(sql, (courseId,))

    course = mycursor.fetchone()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course



# =========================================================
# UPDATE Course
# =========================================================

@app.put("/courses/{courseId}")
def update_course(courseId: int, course: Course):
    mycursor = mydb.cursor()

    sql = """
        UPDATE course
        SET courseName = %s,
            semester = %s
        WHERE courseId = %s
    """

    values = (
        course.courseName,
        course.semester,
        courseId
    )

    mycursor.execute(sql, values)
    mydb.commit()

    if mycursor.rowcount == 0:
        mycursor.close()
        return {
            "message": "Course not found or no changes made"
        }

    mycursor.close()

    return {
        "message": "Course updated successfully",
        "rows": mycursor.rowcount
    }



# DELETE COURSE
@app.delete("/courses/{courseId}")
def delete_course(courseId: int):

    mycursor = mydb.cursor(dictionary=True)

    # Check course exists
    sql = """
        SELECT *
        FROM courses
        WHERE courseId = %s
    """

    mycursor.execute(sql, (courseId,))

    course = mycursor.fetchone()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # Delete course
    sql = """
        DELETE FROM courses
        WHERE courseId = %s
    """

    mycursor.execute(sql, (courseId,))
    mydb.commit()

    return {
        "message": f"Course with ID {courseId} deleted successfully"
    }







# =========================================================
# TEACHER MANAGEMENT
# =========================================================


# CREATE Teacher
@app.post("/teachers")
def create_teacher(teacher: Teacher):

    mycursor = mydb.cursor()

    sql = """
        INSERT INTO teachers
        (
            TeacherId,
            TeacherName,
            TeacherUsername,
            TeacherEmail,
            TeacherAge
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        teacher.TeacherId,
        teacher.TeacherName,
        teacher.TeacherUsername,
        teacher.TeacherEmail,
        teacher.TeacherAge
    )

    mycursor.execute(sql, values)
    mydb.commit()

    return {
        "message": "Teacher inserted successfully",
        "rows": mycursor.rowcount
    }


# GET ALL TEACHERS
@app.get("/teachers")
def get_teachers():

    mycursor = mydb.cursor(dictionary=True)

    sql = """
        SELECT *
        FROM teachers
        ORDER BY TeacherId
    """

    mycursor.execute(sql)

    teachers = mycursor.fetchall()

    return teachers


# GET TEACHER BY ID
@app.get("/teachers/{TeacherId}")
def get_teacher(TeacherId: int):

    mycursor = mydb.cursor(dictionary=True)

    sql = """
        SELECT *
        FROM teachers
        WHERE TeacherId = %s
    """

    mycursor.execute(sql, (TeacherId,))

    teacher = mycursor.fetchone()

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return teacher


# UPDATE TEACHER
@app.put("/teachers/{TeacherId}")
def update_teacher(
    TeacherId: int,
    teacher: Teacher
):

    mycursor = mydb.cursor()

    sql = """
        UPDATE teachers
        SET
            TeacherName = %s,
            TeacherUsername = %s,
            TeacherEmail = %s,
            TeacherAge = %s
        WHERE TeacherId = %s
    """

    values = (
        teacher.TeacherName,
        teacher.TeacherUsername,
        teacher.TeacherEmail,
        teacher.TeacherAge,
        TeacherId
    )

    mycursor.execute(sql, values)
    mydb.commit()

    if mycursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return {
        "message": "Teacher updated successfully",
        "rows": mycursor.rowcount
    }


# DELETE TEACHER
@app.delete("/teachers/{TeacherId}")
def delete_teacher(TeacherId: int):

    mycursor = mydb.cursor(dictionary=True)

    # Check teacher exists
    sql = """
        SELECT *
        FROM teachers
        WHERE TeacherId = %s
    """

    mycursor.execute(sql, (TeacherId,))

    teacher = mycursor.fetchone()

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    # Delete teacher
    sql = """
        DELETE FROM teachers
        WHERE TeacherId = %s
    """

    mycursor.execute(sql, (TeacherId,))
    mydb.commit()

    return {
        "message": f"Teacher with ID {TeacherId} deleted successfully"
    }










# =========================================================
# CREATE ENROLLED COURSE
# =========================================================

@app.post("/enrolled-courses")
def create_enrolled_course(course: enrolled_course):

    mycursor = mydb.cursor()

    sql = """
        INSERT INTO enrolled_courses
        (
            studentid,
            courseId,
            title,
            progress,
            status1
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        course.studentid,
        course.courseId,
        course.title,
        course.progress,
        course.status1
    )

    mycursor.execute(sql, values)
    mydb.commit()

    return {
        "message": "Course enrolled successfully",
        "rows": mycursor.rowcount
    }


# =========================================================
# GET ALL ENROLLED COURSES
# =========================================================

@app.get("/enrolled-courses")
def get_enrolled_courses():

    mycursor = mydb.cursor(dictionary=True)

    sql = """
        SELECT *
        FROM enrolled_courses
        ORDER BY studentid
    """

    mycursor.execute(sql)

    enrolled_courses = mycursor.fetchall()

    return enrolled_courses


# =========================================================
# GET ENROLLED COURSE BY STUDENT ID
# =========================================================

@app.get("/enrolled-courses/{studentid}")
def get_enrolled_course(studentid: int):

    mycursor = mydb.cursor(dictionary=True)

    sql = """
        SELECT *
        FROM enrolled_courses
        WHERE studentid = %s
    """

    mycursor.execute(sql, (studentid,))

    enrolled_courses = mycursor.fetchall()

    if not enrolled_courses:
        raise HTTPException(
            status_code=404,
            detail="Enrolled course not found"
        )

    return enrolled_courses


# =========================================================
# UPDATE ENROLLED COURSE
# =========================================================

@app.put("/enrolled-courses/{studentid}/{courseId}")
def update_enrolled_course(
    studentid: int,
    courseId: int,
    course: enrolled_course
):

    mycursor = mydb.cursor()

    sql = """
        UPDATE enrolled_courses
        SET
            title = %s,
            progress = %s,
            status1 = %s
        WHERE studentid = %s
        AND courseId = %s
    """

    values = (
        course.title,
        course.progress,
        course.status1,
        studentid,
        courseId
    )

    mycursor.execute(sql, values)
    mydb.commit()

    if mycursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Enrolled course not found"
        )

    return {
        "message": "Enrolled course updated successfully",
        "rows": mycursor.rowcount
    }


# =========================================================
# DELETE ENROLLED COURSE
# =========================================================

@app.delete("/enrolled-courses/{studentid}/{courseId}")
def delete_enrolled_course(
    studentid: int,
    courseId: int
):

    mycursor = mydb.cursor()

    sql = """
        DELETE FROM enrolled_courses
        WHERE studentid = %s
        AND courseId = %s
    """

    mycursor.execute(sql, (studentid, courseId))
    mydb.commit()

    if mycursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Enrolled course not found"
        )

    return {
        "message": "Enrolled course deleted successfully",
        "rows": mycursor.rowcount
    }
