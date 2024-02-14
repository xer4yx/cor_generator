import os
import time
import random

from sprints.database import populator_config
from sprints.database.Student_DB import StudentDB
from sprints.database.User_DB import UserDB
from sprints.database.Course_DB import CourseDB
from sprints.database.StCr_DB import StCrDB


class Admin:
    def __init__(self):
        self.__stdb = StudentDB()
        self.__udb = UserDB()
        self.__crdb = CourseDB()
        self.__stcr = StCrDB()

    def generate_student_id(self):
        student_id = time.strftime("%Y%m") + str(random.randint(101, 999))
        data = self.__stdb.get_student_num_all()
        if data.__contains__(student_id):
            self.generate_student_id()

        return student_id

    def add_user(self, student_id):
        data = self.__stdb.get_student_num_all()
        if student_id in data:
            password = str(input(f"Enter Password for {student_id}: ")).encode("utf-8")
            self.__udb.insert_user(student_id, password)
        else:
            print(f"Student {student_id} not found")

    def add_student(self):
        os.system('cls')
        print("---Add Student to School Record---")
        fname = str(input("Enter given name: "))
        lname = str(input("Enter surname: "))
        student_no = self.generate_student_id()
        college = str(input("Enter College: "))
        program = str(input("Enter Program: "))
        yr_lvl = int(input("Enter Year Level: "))

        if self.__stdb.insert_student(fname, lname, student_no, college, program, yr_lvl):
            self.add_user(student_no)
            print(f"Record added successfully. "
                  f"Student ID: {student_no}")
        else:
            print(f"Student ID {student_no} failed to add")

    def add_course(self):
        os.system('cls')
        course_code = str(input("Enter Course Code for the subject: "))
        title = str(input("Enter course name: "))
        section = str(input("Enter section: "))
        units = int(input("Enter number of units: "))
        days = str(input("Enter days: "))
        time = str(input("Enter time for the course: "))
        room = eval(input("Enter room for the course. Leave blank for TBA: "))
        year = int(input("Enter year for the course: "))
        term = int(input("Enter term for the course: "))
        if self.__crdb.add_course(course_code, title, section, units, days, time, year, term, room):
            print(f"Course Added successfully. "
                  f"Course ID: {course_code}")
        else:
            print(f"Course ID {course_code} failed to add")

    def delete_student_data(self):
        os.system('cls')
        print("---Delete Student to School Record---")
        student_no = str(input("Enter Student Number: "))
        data = self.__stdb.get_student_num_all()
        if student_no in data and str(input(f"Do you want to delete the record?")) == 'Yes':
            self.__udb.delete_user(student_no)
            self.__stcr.delete_student_course(student_no)
            self.__stdb.delete_student(student_no)
            print(f"Record for student {student_no} has been deleted")
        else:
            print("Invalid student record.")

    def delete_course(self):
        os.system('cls')
        print("---Delete Course to School Record---")
        course_code = str(input("Enter Course Code: "))
        section = str(input("Enter Section: "))
        data = self.__crdb.select_course(course_code, section)
        if data:
            if self.__crdb.delete_course(course_code, section):
                print(f"Course {course_code} has been deleted")
            else:
                print("Failed to delete course")
        else:
            print("Course not found")

    def update_course(self):
        os.system('cls')
        print("---Update Course---")
        course_code = str(input("Enter Course Code:"))
        section = str(input("Enter section for the course code:"))
        data = self.__crdb.select_course(course_code, section)
        if data:
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
                    self.__crdb.update_course(course_code, title=title)

                case 2:
                    units = str(input("Update course unit: "))
                    self.__crdb.update_course(course_code, units=units)

                case 3:
                    days = str(input("Update course schedule: "))
                    self.__crdb.update_course(course_code, days=days)

                case 4:
                    timeslot = str(input("Update course time slot: "))
                    self.__crdb.update_course(course_code, time=timeslot)

                case 5:
                    room = str(input("Update course room: "))
                    self.__crdb.update_course(course_code, room=room)

                case 6:
                    year = int(input("Update course year: "))
                    self.__crdb.update_course(course_code, year=year)

                case 7:
                    term = int(input("Update course term: "))
                    self.__crdb.update_course(course_code, term=term)

                case _:
                    print(f"Column {choice} doesn't exist in the table")
        else:
            print("Course doesn't exist")

    def update_student(self):
        os.system('cls')
        print("---Update Student Record---")
        student_id = str(input("Enter Student ID: "))
        data = self.__stdb.get_student_num_all()
        if student_id in data:
            choice = int(input("""Select what record you want to update
                [1] First Name
                [2] Last Name
                [3] College
                [4] Program
                [5] Year Level
                [6] Registration Status
                [7] Enrollment Status
                [8] Exit"""))
            match choice:
                case 1:
                    fname = str(input("Update student given name: "))
                    self.__stdb.update_student_info(student_id, fname=fname)

                case 2:
                    lname = str(input("Update student surname: "))
                    self.__stdb.update_student_info(student_id, lname=lname)

                case 3:
                    college = str(input("Update student college: "))
                    self.__stdb.update_student_info(student_id, college=college)

                case 4:
                    program = str(input("Update student program: "))
                    self.__stdb.update_student_info(student_id, program=program)

                case 5:
                    year_level = int(input("Update student year level: "))
                    self.__stdb.update_student_info(student_id, year=year_level)

                case 6:
                    registration = bool(input("Update student registration status: "))
                    self.__stdb.update_student_info(student_id, is_registered=registration)

                case 7:
                    enrollment = bool(input("Update student enrollment status: "))
                    self.__stdb.update_student_info(student_id, is_enrolled=enrollment)

                case 8:
                    return

                case _:
                    print(f"Column {choice} doesn't exist in the table")

    def _student_populator(self,
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

            if (self.__stdb.insert_student(fname=first,
                                           lname=last,
                                           student_no=id,
                                           college=college,
                                           program=course,
                                           yr_lvl=year,
                                           is_enrolled=enrolled)):
                self.__udb.insert_user(student_number=id, password=id.encode())
                success += 1
            else:
                faults += 1

        print(f"{self.__stdb.__class__.__name__} result: {success} data inserted while {faults} failures.")

    def _course_populator(self, batch_size=100):
        faults = 0
        success = 0
        course_data = []

        for code, title in zip(populator_config.COURSE_COL1, populator_config.COURSE_COL2):
            year = random.choice(populator_config.COURSE_COL8)
            term = random.choice(populator_config.COURSE_COL9)
            units = random.choice(populator_config.COURSE_COL4)
            for sections in populator_config.COURSE_COL3:
                for schedules in populator_config.COURSE_COL5:
                    for times in populator_config.COURSE_COL6:
                        for rooms in populator_config.COURSE_COL7:
                            course_data.append({
                                "course_code": code,
                                "title": title,
                                "section": sections,
                                "units": units,
                                "days": schedules,
                                "time": times,
                                "year": year,
                                "term": term,
                                "room": rooms
                            })
                            if len(course_data) == batch_size:
                                if self.__crdb.add_course_batch(course_data):
                                    success += len(course_data)
                                else:
                                    faults += len(course_data)
                                course_data = []

        if course_data:
            if self.__crdb.add_course_batch(course_data):
                success += len(course_data)
            else:
                faults += len(course_data)

        print(f"{self.__crdb.__class__.__name__} result: {success} data inserted while {faults} failures.")

    def populate_tables(self):
        os.system('cls')
        choice = str(input("""Do you want to populate the tables?
            [] Yes
            [] No
            Enter your choice: """))
        if choice == "Yes":
            max = int(input("How many do you want to populate: "))
            self._student_populator(max_population=max)
            self._course_populator()
        elif choice == "No":
            pass
        else:
            print("Invalid input. Please try again.")

    def add_records_menu(self):
        os.system('cls')
        choice = int(input("""COR Generator - Insert Record
            [1] Insert on Student Table
            [2] Insert on Course Table
            [3] Exit
            
            Enter your choice: """))

        match choice:
            case 1:
                self.add_student()

            case 2:
                self.add_course()

            case 3:
                return

            case _:
                print("Invalid choice. Please try again.")

    def delete_records_menu(self):
        os.system('cls')
        choice = int(input("""COR Generator - Insert Record
            [1] Delete on Student Table
            [2] Delete on Course Table
            [3] Exit

            Enter your choice: """))

        match choice:
            case 1:
                self.delete_student_data()

            case 2:
                self.delete_course()

            case 3:
                return

            case _:
                print("Invalid choice. Please try again.")

    def update_records_menu(self):
        os.system('cls')
        choice = int(input("""COR Generator - Insert Record
            [1] Update on Student Table
            [2] Update on Course Table
            [3] Exit

            Enter your choice: """))

        match choice:
            case 1:
                self.update_student()

            case 2:
                self.update_course()

            case 3:
                return

            case _:
                print("Invalid choice. Please try again.")

    def admin_menu(self):
        os.system('cls')
        print("""COR Generator Admin
            [1] Add Record
            [2] Delete Record
            [3] Update Record
            [4] Populate Tables
            [5] Logout""")
        choice = int(input("Enter your choice: "))
        match choice:
            case 1:
                self.add_records_menu()

            case 2:
                self.delete_records_menu()

            case 3:
                self.update_records_menu()

            case 4:
                self.populate_tables()

            case 5:
                exit()

            case _:
                print("Invalid choice. Please try again.")
