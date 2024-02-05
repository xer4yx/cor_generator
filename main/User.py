from sprints.database.User_DB import UserDB
from sprints.exceptions.CustomExceptions import *


class User:
    @staticmethod
    def change_password(student_number, password, new_password):
        try:
            data = UserDB.select_user(student_number)

            if data.password != password:
                raise CredentialError("Wrong password")

            UserDB.update_user(student_number, new_password)

        except Exception as e:
            print(e)

