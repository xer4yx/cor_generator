import bcrypt as bc


class Security:
    @staticmethod
    def generate_salt(rounds=12, prefix=b"2b") -> bytes:
        return bc.gensalt(rounds=rounds, prefix=prefix)

    @staticmethod
    def hash_string(password) -> bytes:
        hashed_password = bc.hashpw(password, Security.generate_salt())
        return hashed_password

    @staticmethod
    def check_password(password: bytes, hashed: bytes) -> bool:
        if bc.checkpw(password, hashed):
            print("Password is correct")
            return True
        else:
            raise

    @staticmethod
    def check_credentials(student_number, password):
        def get_db():
            from sprints.database.User_DB import UserDB
            return UserDB()

        udb = get_db()
        data = udb.select_user(student_number)
        if student_number in data['student_number']:
            Security.check_password(password.encode('utf-8'), data['password'].encode('utf-8'))
        else:
            print("Invalid Credentials!")
