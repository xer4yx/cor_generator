import os
from sprints.Data_Security import Security
from sprints.database.Student_DB import StudentDB
from main.Admin import Admin
from main.Student import Student
from sprints.exceptions.CustomExceptions import CredentialException


def login_page():
    try:
        os.system('cls')
        print('COR GENERATOR LOGIN')
        user = str(input("Student Number: "))
        password = str(input("Password: "))
        if Security.check_credentials(user, password):
            if True in StudentDB.get_admin_status(student_number=user):
                host = Admin()
                host.admin_menu()
            else:
                client = Student(user)
                client.student_menu()
        else:
            print("Invalid Credentials")
    except Exception as e:
        print(e)


def run():
    os.system('cls')
    choice = int(input("""
            COR GENERATOR
            [1] Login Page
            [2] Exit Program

            Enter your choice: """))

    match choice:
        case 1:
            login_page()

        case 2:
            exit()

        case _:
            print("Invalid choice. Try again.")


if __name__ == '__main__':
    while True:
        run()
