from sprints.exceptions.CustomExceptions import *


class User:
    def __init__(self, name=None, studentNum=None, isRegistered=False, isEnrolled=False,
                 college=None, program=None, yearLvl=None):
        self.__name = name
        self.__studentNum = studentNum
        self.__isRegistered = isRegistered
        self.__isEnrolled = isEnrolled
        self.__college = college
        self.__program = program
        self.__yearLvl = yearLvl

    def generate_cor(self):
        try:
            if self.__isRegistered is not False:
                registration_status = "Registered"
                if self.__isEnrolled is not False:
                    enrollment_status = "Enrolled"
                else:
                    enrollment_status = "COR invalid. Student is not yet enrolled."

                print(f"""
                      {registration_status}
                      {enrollment_status}
                      {self.__studentNum}                   {self.__college} - {self.__program}
                      {self.__name}                         {self.__yearLvl}

                      | Courses | Title | Section | Units | Days | Time | Room |
                      """)
            else:
                raise RegistrationError()
        except RegistrationError as e:
            print(f"Error: {e}")

    def save_data(self):
        pass
