import time
import random

from sprints.database.Student_DB import StudentDB
from sprints.database.User_DB import UserDB
from sprints.database.Course_DB import CourseDB
from sprints.database.StCr_DB import StCrDB


class Admin:
    def __init__(self):
        self.stdb = StudentDB()
        self.udb = UserDB()
        self.crdb = CourseDB()
        self.stcr = StCrDB()

    def generate_student_id(self):
        student_id = time.strftime("%Y%m") + str(random.randint(101, 999))
        data = self.stdb.get_student_num_all()
        if data.__contains__(student_id):
            self.generate_student_id()

        return student_id

    def add_user(self, student_id):
        data = self.stdb.get_student_num_all()
        if student_id in data:
            password = str(input("Enter Password for : "))
            self.udb.insert_user(student_id, password)
        else:
            print(f"Student {student_id} not found")

    def add_student(self):
        print("---Add Student to School Record---")
        fname = str(input("Enter given name: "))
        lname = str(input("Enter surname: "))
        student_no = self.generate_student_id()
        college = str(input("Enter College: "))
        program = str(input("Enter Program: "))
        yr_lvl = int(input("Enter Year Level: "))
        is_registered = False
        is_enrolled = False

        if self.stdb.insert_student(fname, lname, student_no, college, program, yr_lvl, is_registered, is_enrolled):
            print(f"Record added successfully. "
                  f"Student ID: {student_no}")
        else:
            print(f"Student ID {student_no} failed to add")

    def add_course(self):
        course_code = str(input("Enter Course Code for the subject: "))
        title = str(input("Enter course name: "))
        section = str(input("Enter section: "))
        units = int(input("Enter number of units: "))
        days = str(input("Enter days: "))
        time = str(input("Enter time for the course: "))
        room = eval(input("Enter room for the course. Leave blank for TBA: "))
        year = int(input("Enter year for the course: "))
        term = int(input("Enter term for the course: "))
        if self.crdb.add_course(course_code, title, section, units, days, time, year, term, room):
            print(f"Course Added successfully. "
                  f"Course ID: {course_code}")
        else:
            print(f"Course ID {course_code} failed to add")

    def delete_student_data(self):
        print("---Delete Student to School Record---")
        student_no = str(input("Enter Student Number: "))
        data = self.stdb.get_student_num_all()
        if data['student_number'].__contains__(student_no) and eval(input(f"Do you want to delete the record?")) == 'Yes':
            if self.udb.delete_user(student_no) and self.stdb.delete_student(student_no):
                print(f"Record for student {student_no} has been deleted")
        else:
            print("Invalid student record.")

    def delete_course(self):
        print("---Delete Course to School Record---")
        course_code = str(input("Enter Course Code: "))
        section = str(input("Enter Section: "))
        data = self.crdb.select_course(course_code, section)
        if data['course_code'].__contains__(course_code) and data['section'].__contains__(section):
            if self.crdb.delete_course(course_code, section):
                print(f"Course {course_code} has been deleted")

        else:
            print("Course doesn't exist")



