from pydantic import BaseModel

class Student(BaseModel):
    studentid: int
    username: str
    email: str
    is_active: bool
    name: str
    age: int
    country: str
    plan: str
    expire_at: str



class Student_update(BaseModel):
    username: str
    email: str
    is_active: bool
    name: str
    age: int
    country: str
    plan: str
    expire_at: str


class Course(BaseModel):
    courseId: int
    courseName: str
    semester: int


class Teacher(BaseModel):
    TeacherId: int
    TeacherName: str
    TeacherUsername: str
    TeacherEmail: str
    TeacherAge: int



class enrolled_course(BaseModel):
    studentid: int
    courseId: int
    title: str
    progress: int
    status1: str
