import time
import random

from sprints.database import populator_config
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
            self.add_user(student_no)
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
        if data['student_number'].__contains__(student_no) and eval(
                input(f"Do you want to delete the record?")) == 'Yes':
            if (self.udb.delete_user(student_no) and self.stcr.delete_student_course(student_no)
                    and self.stdb.delete_student(student_no)):
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

    def update_course(self):
        print("---Update Course---")
        course_code = str(input("Enter Course Code:"))
        section = str(input("Enter section for the course code:"))
        data = self.crdb.select_course(course_code, section)
        if data['course_code'].__contains__(course_code) and data['section'].__contains__(section):
            choice = int(input("""Select what record you want to update
                [1] Title
                [2] Units
                [3] Days
                [4] Time
                [5] Room
                [6] Year
                [7] Term"""))
            match choice:
                case 1:
                    title = str(input("Update course title: "))
                    self.crdb.update_course(course_code, title=title)

                case 2:
                    units = str(input("Update course unit: "))
                    self.crdb.update_course(course_code, units=units)

                case 3:
                    days = str(input("Update course schedule: "))
                    self.crdb.update_course(course_code, days=days)

                case 4:
                    timeslot = str(input("Update course time slot: "))
                    self.crdb.update_course(course_code, time=timeslot)

                case 5:
                    room = str(input("Update course room: "))
                    self.crdb.update_course(course_code, room=room)

                case 6:
                    year = int(input("Update course year: "))
                    self.crdb.update_course(course_code, year=year)

                case 7:
                    term = int(input("Update course term: "))
                    self.crdb.update_course(course_code, term=term)

                case _:
                    print(f"Column {choice} doesn't exist in the table")
        else:
            print("Course doesn't exist")

    def update_student(self):
        print("---Update Student Record---")
        student_id = str(input("Enter Student ID: "))
        data = self.stdb.get_student_num_all()
        if student_id in data:
            choice = int(input("""Select what record you want to update
                [1] First Name
                [2] Last Name
                [3] College
                [4] Program
                [5] Year Level
                [6] Registration Status
                [7] Enrollment Status"""))
            match choice:
                case 1:
                    fname = str(input("Update student given name: "))
                    self.stdb.update_student_info(student_id, fname=fname)

                case 2:
                    lname = str(input("Update student surname: "))
                    self.stdb.update_student_info(student_id, lname=lname)

                case 3:
                    college = str(input("Update student college: "))
                    self.stdb.update_student_info(student_id, college=college)

                case 4:
                    program = str(input("Update student program: "))
                    self.stdb.update_student_info(student_id, program=program)

                case 5:
                    year_level = int(input("Update student year level: "))
                    self.stdb.update_student_info(student_id, year=year_level)

                case 6:
                    registration = bool(input("Update student registration status: "))
                    self.stdb.update_student_info(student_id, is_registered=registration)

                case 7:
                    enrollment = bool(input("Update student enrollment status: "))
                    self.stdb.update_student_info(student_id, is_enrolled=enrollment)

                case _:
                    print(f"Column {choice} doesn't exist in the table")

    def student_populator(self,
                          max_population=5):
        faults = 0
        success = 0
        for _ in range(1, max_population + 1):
            first = random.choice(populator_config.STUDENT_COL1)
            last = random.choice(populator_config.STUDENT_COL2)
            id = self.generate_student_id()
            college = random.choice(populator_config.STUDENT_COL4)
            course = random.choice(populator_config.STUDENT_COL5[0]) if college == "Computer Studies" \
                else random.choice(populator_config.STUDENT_COL5[1])
            year = random.choice(populator_config.STUDENT_COL6)
            enrolled = random.choice([True, False])

            if (self.stdb.insert_student(fname=first,
                                         lname=last,
                                         student_no=id,
                                         college=college,
                                         program=course,
                                         yr_lvl=year,
                                         is_enrolled=enrolled)):
                self.udb.insert_user(student_number=id, password=id.encode())
                success += 1
            else:
                faults += 1

        print(f"{self.stdb.__class__.__name__} result: {success} data inserted while {faults} failures.")

    def course_populator(self):
        faults = 0
        success = 0
        for code, title in zip(populator_config.COURSE_COL1, populator_config.COURSE_COL2):
            section = random.choice(populator_config.COURSE_COL3)
            units = random.choice(populator_config.COURSE_COL4)
            sched = random.choice(populator_config.COURSE_COL5)
            time = random.choice(populator_config.COURSE_COL6)
            room = random.choice(populator_config.COURSE_COL7)
            year = random.choice(populator_config.COURSE_COL8)
            term = random.choice(populator_config.COURSE_COL9)

            if self.crdb.add_course(course_code=code,
                                    title=title,
                                    section=section,
                                    units=units,
                                    days=sched,
                                    time=time,
                                    year=year,
                                    term=term,
                                    room=room):
                success += 1
            else:
                faults += 1

        print(f"{self.crdb.__class__.__name__} result: {success} data inserted while {faults} failures.")

    def populate_tables(self, max):
        choice = str(input("""Do you want to populate the tables?
            [] Yes
            [] No"""))
        if choice == "Yes":
            self.student_populator(max_population=max)
            self.course_populator()
        elif choice == "No":
            pass
        else:
            print("Invalid input. Please try again.")
