import time
import random

from sprints.database.Student_DB import StudentDB
from sprints.database.User_DB import UserDB


class Admin:
    def __init__(self):
        self.__username = 'admin'
        self.__password = 'password'
        self.stdb = StudentDB()
        self.udb = UserDB()

    def generate_student_id(self):
        student_id = time.strftime("%Y%m") + str(random.randint(101, 999))
        data = self.stdb.get_student_num_all()
        if data.__contains__(student_id):
            self.generate_student_id()

        return student_id

    def add_user(self, student_id):
        data = self.stdb.get_student_num_all()
        print(data)
        if student_id in data:
            password = str(input("Enter Password for : "))
            self.udb.insert_user(student_id, password)
        else:
            print(f"Student {student_id} not found")

    def add_student(self):
        print("---Add Student to School Record---")
        fname = eval(input("Enter given name: "))
        lname = eval(input("Enter surname: "))
        student_no = self.generate_student_id()
        college = eval(input("Enter College: "))
        program = eval(input("Enter Program: "))
        yr_lvl = eval(input("Enter Year Level: "))
        is_registered = False
        is_enrolled = False

        if StudentDB.insert_student(fname, lname, student_no, college, program, yr_lvl, is_registered, is_enrolled):
            print(f"Record added successfully. Student ID: {student_no}")
        else:
            pass

    def delete_user_data(self):
        print("---Delete Student to School Record---")
        student_no = str(input("Enter Student Number: "))
        data = self.stdb.get_student_num_all()
        if data.__contains__(student_no) and eval(input(f"Do you want to delete the record?")) == "Yes":
            if self.stdb.delete_student(student_no):
                print(f"Record for student {student_no} has been deleted")
        else:
            pass
