from sprints.exceptions.customexceptions import *
from sprints.datasecurity import Security
from sprints.database.coursedb import CourseDB
from sprints.database.studentdb import StudentDB
from sprints.database.userdb import UserDB
from sprints.database.stcrdb import StCrDB


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
            self.__username, self.__password, self.__salt = (self.__user_data['student_number'],
                                                             self.__user_data['password'],
                                                             self.__user_data['salt'])
        else:
            self.__username, self.__password, self.__salt = None, None, None

        if self.__student_data:
            (self.__fname, self.__lname, self.__student_id, self.__college, self.__program,
             self.__year_lvl, self.__is_registered, self.__is_enrolled, self.__is_admin) = self.__student_data
        else:
            (self.__fname, self.__lname, self.__student_id, self.__college, self.__program, self.__year_lvl,
             self.__is_registered, self.__is_enrolled) = None, None, None, None, None, None, None, None

        self.__course_data_by_yr = self.__crdb.select_by_year(self.__year_lvl)
        self.__course_data_all = self.__crdb.select_all_row()

        if self.__course_data_by_yr:
            (self.__course_id, self.__title, self.__section, self.__units,
             self.__days, self.__time, self.__room, self.__year, self.__term) = zip(*self.__course_data_by_yr)
        else:
            (self.__course_id, self.__title, self.__section, self.__units, self.__days, self.__time,
             self.__room, self.__year, self.__term) = None, None, None, None, None, None, None, None, None

        if self.__course_data_all:
            (self.__all_course_id, self.__all_title, self.__all_units,
             self.__all_year, self.__all_term) = zip(*self.__course_data_all)
        else:
            (self.__all_course_id, self.__all_title, self.__all_units,
             self.__all_year, self.__all_term) = None, None, None, None, None

        if self.__stcr_data:
            (self.__c_id, self.__s_id, self.__c_title, self.__c_year, self.__c_term, self.__c_section,
             self.__c_units, self.__c_days, self.__c_time, self.__c_room) = zip(*self.__stcr_data)
        else:
            (self.__c_id, self.__s_id, self.__c_title, self.__c_year, self.__c_term, self.__c_section, self.__c_units,
             self.__c_days, self.__c_time, self.__c_room) = None, None, None, None, None, None, None, None, None, None

    def view_curriculum(self):
        try:
            if None not in (self.__all_course_id, self.__all_title, self.__all_units,
                            self.__all_year, self.__all_term):

                courses = {}
                for course_id, title, units, year, term in zip(
                        self.__all_course_id, self.__all_title, self.__all_units,
                        self.__all_year, self.__all_term
                ):
                    if (year, term) not in courses:
                        courses[(year, term)] = []
                    courses[(year, term)].append((course_id, title, units))

                for (year, term), courses in sorted(courses.items()):
                    print(f"Year: {year}, Term: {term}")
                    for course in courses:
                        course_id, title, units = course
                        print(f"{course_id} - {title} ({units} units)")
                    print()
            else:
                raise NullException("No courses offered.")

        except NullException as e:
            print(e)

    def view_available_course(self):
        try:
            if None not in (self.__course_id, self.__title, self.__section, self.__units,
                            self.__days, self.__time, self.__room, self.__year, self.__term):

                courses_by_section = {}
                for course_id, title, section, units, days, time, room, year, term in zip(
                        self.__course_id, self.__title, self.__section, self.__units,
                        self.__days, self.__time, self.__room, self.__year, self.__term
                ):
                    if section not in courses_by_section:
                        courses_by_section[section] = []
                    courses_by_section[section].append((course_id, title, units, days, time, room, year, term))

                for section, courses in courses_by_section.items():
                    print(f"Section: {section}")
                    for course in courses:
                        course_id, title, units, days, time, room, year, term = course
                        print(f"{course_id} - {title} ({units} units) - {days} - {time} - {room}")
                    print()
            else:
                print(f"No courses offered for {self.__student_id}")

        except ValueError as ve:
            print(ve)

    def view_selected_course(self):
        try:
            if None not in (self.__c_id, self.__c_title, self.__c_year, self.__c_term, self.__c_section,
                            self.__c_units, self.__c_days, self.__c_time, self.__c_room):
                for course_id, title, year, term, section, units, days, time, room in zip(
                        self.__c_id, self.__c_title, self.__c_year, self.__c_term, self.__c_section, self.__c_units,
                        self.__c_days, self.__c_time, self.__c_room):
                    print(f"""
                    {course_id} - {title} ({units} units) - {days} - {time} - {room}""")

            else:
                raise NullException("No courses selected")

        except NullException as e:
            print(e)

    def choose_course(self):
        try:
            if None not in (self.__course_id, self.__title, self.__section, self.__units,
                            self.__days, self.__time, self.__room, self.__year, self.__term):
                section_input = str(input("Enter the section you want to enroll in: "))
                year_level_input = int(input("Enter your current year level: "))

                available_courses = []
                for course_id, title, section, units, days, time, room, year, term in zip(
                        self.__course_id, self.__title, self.__section, self.__units,
                        self.__days, self.__time, self.__room, self.__year, self.__term
                ):
                    if section == section_input and year == year_level_input:
                        available_courses.append((course_id, title, year, term, section, units, days, time, room))

                if available_courses:
                    for course in available_courses:
                        if self.__stcrdb.add_student_course(self.__student_id, *course):
                            print(f"Enrolled in course {course[0]}.")
                        else:
                            print("Failed to enroll in the course. Please try again later.")
                else:
                    print(f"No courses available for section {section_input} and year level {year_level_input}.")
            else:
                print(f"No courses offered for {self.__student_id}")

            data = self.__stcrdb.select_student_courses(self.__student_id)
            if data:
                (self.__c_id, self.__s_id, self.__c_title, self.__c_year, self.__c_term, self.__c_section,
                 self.__c_units, self.__c_days, self.__c_time, self.__c_room) = zip(*data)

        except ValueError as ve:
            print(ve)

    def delete_selected_course(self):
        try:
            choice = str(input("""
            Do you want to remove your selected courses?
            [] Yes
            [] No
            
            Enter your choice: """))

            if choice == 'Yes':
                if self.__stcrdb.delete_student_course(self.__s_id[0], self.__c_section[0]):
                    (self.__c_id, self.__s_id, self.__c_title, self.__c_year, self.__c_term, self.__c_section,
                     self.__c_units, self.__c_days, self.__c_time, self.__c_room) = (None, None, None, None, None, None,
                                                                                     None, None, None, None)
                    print(f"Student data for section {self.__c_section} has been deleted.")
                else:
                    print("Error occurred during deletion.")
            else:
                return

        except ValueError as e:
            print(e)

    def change_password(self):
        try:
            old_password = input("Enter old password: ").encode()
            new_password = input("Enter new password: ").encode()
            salt, hashed_new = Security.hash_string(new_password)

            if not Security.check_password(old_password, self.__password.encode(), self.__salt.encode()):
                raise CredentialException("Wrong password")

            self.__udb.update_user(self.__username, hashed_new, salt)
            self.__password = hashed_new

        except CredentialException as e:
            print(e)

    def generate_cor(self):
        try:
            if self.__is_registered is not False:
                registration_status = "Registered"
            else:
                raise RegistrationException()

            if self.__is_enrolled is not False:
                enrollment_status = "Enrolled"
            else:
                enrollment_status = "COR invalid. Student is not yet enrolled."

            print(f"""
                {registration_status}
                {enrollment_status}
                STUDENT NO: {self.__student_id}\t\t\t\t\t\t\t\t\t\t\tCOLLEGE: {self.__college} - {self.__program}
                NAME: {self.__fname} {self.__lname}\t\t\t\t\t\t\t\t\t\t\t\tYEAR: {self.__year_lvl}
                | Courses |\t\t\tTitle\t\t\t|\tSection\t|\tUnits\t|\tDays\t|\t\tTime\t\t|\tRoom\t|""")

            if None not in (self.__c_id, self.__c_title, self.__c_year, self.__c_term, self.__c_section,
                            self.__c_units, self.__c_days, self.__c_time, self.__c_room):
                fee = 0
                misc = 8933
                id_val_fee = 75
                for course_id, title, year, term, section, units, days, time, room in zip(
                        self.__c_id, self.__c_title,
                        self.__c_year, self.__c_term, self.__c_section,
                        self.__c_units, self.__c_days, self.__c_time,
                        self.__c_room):
                    fee += units
                    print(f"""
                    {course_id} - {title} ({units} units) - {section} - {days} - {time} - {room}""")
                print(f"""
                Tuition Fee: Php {fee * 1902}
                Miscellaneous Fee: Php {misc}
                ID Validation Fee: Php {id_val_fee}
                TOTAL ASSESSMENT: Php {(fee * 1902) + misc + id_val_fee}""")

            else:
                print(f"No course registered for {self.__student_id}")

        except RegistrationException as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def profile_menu(self):
        choice = int(input("""
        COR GENERATOR PROFILE MENU
        [1] Change Password
        [2] Return to Main Menu
        
        Enter your choice: """))

        match choice:
            case 1:
                self.change_password()

            case 2:
                return

            case _:
                print("Invalid choice. Try again.")

    def course_offer_menu(self):
        choice = int(input("""
        COR GENERATOR COURSE OFFER
        [1] View Curriculum
        [2] View Available Courses
        [3] View Selected Block
        [4] Return to Main Menu
        
        Enter your choice: """))

        match choice:
            case 1:
                self.view_curriculum()

            case 2:
                self.view_available_course()

            case 3:
                self.view_selected_course()

            case 4:
                return

            case _:
                print("Invalid choice. Try again.")

    def manage_course_menu(self):
        choice = int(input("""
        COR GENERATOR COURSE MANAGEMENT
        [1] Choose Course
        [2] Delete Selected Course
        [3] Return to Main Menu
        
        Enter your choice: """))

        match choice:
            case 1:
                self.choose_course()

            case 2:
                self.delete_selected_course()

            case 3:
                return

            case _:
                print("Invalid Choice. Try again.")

    def student_menu(self):
        while True:
            choice = int(input(f"""
            COR GENERATOR - Student
            [1] Profile Settings
            [2] Course Offering
            [3] Manage Course
            [4] Generate COR
            [5] Logout
            
            Enter your choice: """))

            match choice:
                case 1:
                    self.profile_menu()

                case 2:
                    self.course_offer_menu()

                case 3:
                    self.manage_course_menu()

                case 4:
                    self.generate_cor()

                case 5:
                    break

                case _:
                    print("Invalid choice. Try again.")
