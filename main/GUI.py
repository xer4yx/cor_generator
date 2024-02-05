from User import User

import os

class Interface:

    @staticmethod
    def login_page():
        os.system('cls')
        print('FEU Institute of Technology')
        user = input("Student Number: ")
        password = input("Password: ")

    @staticmethod
    def signup_page():
        os.system('cls')

    @staticmethod
    def login_menu():
        os.system('cls')
        print(f"""
              FEU Institute of Technology
              [1] Login
              [2] Sign-up
              [3] Exit
              """)
        decision = input("Enter your choice: ")

        match decision:
            case '1':
                Interface.login_page()
            case '2':
                Interface.signup_page()
            case '3':
                exit()
            case _:
                pass

    @staticmethod
    def main_menu():
        os.system('cls')
        print(f"""
              FEU Institute of Technology
              [1] Generate COR
              [2] Sign-out
              """)

    @staticmethod
    def cor_menu():
        os.system('cls')
        print(f"""
              FEU Institute of Technology

              """)
        User.generate_cor()
