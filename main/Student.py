from sprints.exceptions.CustomExceptions import *
from sprints.database.Course_DB import CourseDB
from sprints.database.Student_DB import StudentDB
from sprints.database.User_DB import UserDB
from sprints.database.StCr_DB import StCrDB


class Student:
    def __init__(self, student_id):
        self.__crdb = CourseDB()
        self.__stdb = StudentDB()
        self.__udb = UserDB()
        self.__stcrdb = StCrDB()
        self.__user_data = self.__udb.select_user(student_id)
        self.__student_data = self.__stdb.get_student_info(student_id)
        self.__stcr_data = self.__stcrdb.select_student_courses(student_id)

        if self.__user_data:
            self.__username, self.__password = self.__user_data
        else:
            self.__username, self.__password = None, None

        if self.__student_data:
            (self.__fname, self.__lname, self.__student_id, self.__college, self.__program,
             self.__year_lvl, self.__is_registered, self.__is_enrolled) = self.__student_data
        else:
            (self.__fname, self.__lname, self.__student_id, self.__college, self.__program, self.__year_lvl,
             self.__is_registered, self.__is_enrolled) = None, None, None, None, None, None, None, None

        self.__course_data = self.__crdb.select_course_by_year(self.__year_lvl)

        if self.__course_data:
            (self.__course_id, self.__title, self.__section, self.__units,
             self.__days, self.__time, self.__room, self.__year, self.__term) = zip(*self.__course_data)
        else:
            (self.__course_id, self.__title, self.__section, self.__units, self.__days, self.__time,
             self.__room, self.__year, self.__term) = None, None, None, None, None, None, None, None, None

        if self.__stcr_data:
            (self.__c_id, self.__s_id, self.__c_title, self.__c_year, self.__c_term, self.__c_section,
             self.__c_units, self.__c_days, self.__c_time, self.__c_room) = zip(*self.__stcr_data)
        else:
            (self.__c_id, self.__s_id, self.__c_title, self.__c_year, self.__c_term, self.__c_section, self.__c_units,
             self.__c_days, self.__c_time, self.__c_room) = None, None, None, None, None, None, None, None, None, None

    def view_available_course(self):
        try:
            if None not in (self.__course_id, self.__title, self.__section, self.__units,
                            self.__days, self.__time, self.__room, self.__year, self.__term):
                for course_id, title, section, units, days, time, room, year, term in zip(
                        self.__course_id, self.__title, self.__section, self.__units,
                        self.__days, self.__time, self.__room, self.__year, self.__term
                ):
                    print(course_id, title, section, units, days, year, term)
            else:
                print(f"No courses offered for {self.__student_id}")

        except ValueError as ve:
            print(ve)

    def change_password(self, password, new_password):
        try:
            if self.__password != password:
                raise CredentialError("Wrong password")

            self.__udb.update_user(self.__username, new_password)
        except Exception as e:
            print(e)

    def generate_cor(self):
        try:
            if self.__is_registered is not False:
                registration_status = "Registered"
            else:
                raise RegistrationError()

            if self.__is_enrolled is not False:
                enrollment_status = "Enrolled"
            else:
                enrollment_status = "COR invalid. Student is not yet enrolled."

            print(f"""
                {registration_status}
                {enrollment_status}
                STUDENT NO: {self.__student_id}\t\t\t\t\t\t\t\t\t\t\tCOLLEGE: {self.__college} - {self.__program}
                NAME: {self.__fname} {self.__lname}\t\t\t\t\t\t\t\t\t\tYEAR: {self.__year_lvl}

                |\tCourses\t|\t\t\tTitle\t\t\t|\tSection\t|\tUnits\t|\tDays\t|\t\tTime\t\t|\tRoom\t|""")

            if None not in (self.__c_id, self.__c_title, self.__c_year, self.__c_term, self.__c_section,
                            self.__c_units, self.__c_days, self.__c_time, self.__c_room):
                for course_id, title, year, term, section, units, days, time, room in zip(
                        self.__c_id, self.__c_title,
                        self.__c_year, self.__c_term, self.__c_section,
                        self.__c_units, self.__c_days, self.__c_time,
                        self.__c_room):
                    print(f"""
                    {course_id}\t {title}\t\t {section}\t\t {units}\t\t\t{days}\t\t\t{time}\t\t {room}""")
            else:
                print(f"No course registered for {self.__student_id}")

        except RegistrationError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"An error occurred: {e}")
