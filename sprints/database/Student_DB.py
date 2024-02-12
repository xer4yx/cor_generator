import mysql.connector
from sprints.exceptions.CustomExceptions import *


class StudentDB:
    def __init__(self, host="localhost", user="root", password="Vertig@6925", database="educ_database"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def delete_student(self, student_number: str):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = "DELETE FROM student WHERE student_number = %s"
                data_cursor.execute(query, (student_number,))

            connection.commit()
            return True

        except DataDeletionException as e:
            print(f"{e.__class__.__name__}: {e}")
            return False

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def insert_student(self,
                       fname: str,
                       lname: str,
                       student_no: str,
                       college: str,
                       program: str,
                       yr_lvl: int,
                       is_registered: bool = True,
                       is_enrolled: bool = False) -> bool:
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = "INSERT INTO student VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                data_cursor = data_cursor.execute(query, (fname, lname, student_no, college, program, yr_lvl,
                                                          is_registered, is_enrolled))

            connection.commit()
            return True

        except DataInsertionException as e:
            print(f"{e.__class__.__name__}: {e}")
            return False

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def update_student_info(self,
                            student_no: str,
                            fname: str = None,
                            lname: str = None,
                            college: str = None,
                            program: str = None,
                            year: int = None,
                            is_registered: bool = None,
                            is_enrolled: bool = None):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                update_columns = [(col, val) for col, val in [('first_name', fname), ('last_name', lname),
                                                              ('college', college), ('program', program),
                                                              ('year_lvl', year), ('is_registered', is_registered),
                                                              ('is_enrolled', is_enrolled)] if val is not None]

                query = (f"UPDATE student SET SET {', '.join([f'{col} = %s' for col, val in update_columns])}"
                         f"WHERE student_number = %s")
                data_cursor = data_cursor.execute(query, [val for col, val in update_columns] + [student_no])

            connection.commit()
            return True

        except DataUpdateException as e:
            print(f"{e.__class__.__name__}: {e}")
            return False

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def get_student_num_all(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = "SELECT student_number FROM student"
                data_cursor.execute(query)
                result = data_cursor.fetchall()
                return [student_number[0].strip() for student_number in result]
        except DataSelectionException as e:
            print(f"{e.__class__.__name__}: {e}")

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def get_student_info(self, student_number):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = "SELECT * FROM student WHERE student_number = %s"
                data_cursor.execute(query, student_number)
                result = data_cursor.fetchone()

                return result
        except DataSelectionException as e:
            print(f"{e.__class__.__name__}: {e}")

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()
