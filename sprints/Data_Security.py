import bcrypt as bc
from sprints.exceptions.CustomExceptions import CredentialException


class Security:
    @staticmethod
    def generate_salt(rounds=12, prefix=b"2b") -> bytes:
        return bc.gensalt(rounds=rounds, prefix=prefix)

    @staticmethod
    def hash_string(password) -> tuple:
        salt = Security.generate_salt()
        hashed_password = bc.hashpw(password, salt)
        return salt, hashed_password

    @staticmethod
    def check_password(password: bytes, hashed: bytes, salt: bytes) -> bool:
        return hashed == bc.hashpw(password, salt)

    @staticmethod
    def check_credentials(student_number, password):
        def get_db():
            from sprints.database.User_DB import UserDB
            return UserDB()

        try:
            udb = get_db()
            data = udb.select_user(student_number)
            if student_number in data['student_number']:
                if Security.check_password(password.encode('utf-8'),
                                           data['password'].encode('utf-8'),
                                           data['salt'].encode('utf-8')):
                    print("Password is correct")
                else:
                    raise CredentialException("Password is wrong")
            else:
                raise CredentialException("Invalid Credentials!")

        except CredentialException as e:
            print(e)
