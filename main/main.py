import os
from sprints.datasecurity import Security
from sprints.database.studentdb import StudentDB
from admin import Admin
from student import Student


def login_page():  # Interface for logging in
    try:
        os.system('cls')
        print('COR GENERATOR LOGIN')
        user = str(input("Student Number: "))
        password = str(input("Password: "))

        # This checks if user and password exists in the database
        if Security.check_credentials(user, password):

            # Checks the admin status of user. If True, it will go to admin menu, else to student menu
            if True in StudentDB.get_admin_status(student_number=user):
                host = Admin()
                host.admin_menu()
            else:
                client = Student(user)
                client.student_menu()

    except Exception as e:  # This catches exceptions in the check_credentials method
        print(e)


def run():  # Runs the whole program
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
