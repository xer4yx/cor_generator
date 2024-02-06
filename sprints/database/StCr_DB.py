import mysql.connector
from sprints.exceptions.CustomExceptions import *


class StCrDB:
    def __init__(self, host="localhost", user="root", password="Vertig@6925", database="educ_database"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def add_student_course(self,
                           student_id: str,
                           course_id: str,
                           course_title: str,
                           course_year: int,
                           course_term: int,
                           course_section: str,
                           course_units: int,
                           course_days: str,
                           course_time: str,
                           course_room: str = None) -> bool:
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = ("INSERT INTO student_course (course_id, student_id, course_title, course_year, "
                         "course_term, course_section, course_units, course_days, course_time, course_room) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                data_cursor.execute(query, (course_id, student_id, course_title, course_year, course_term,
                                            course_section, course_units, course_days, course_time, course_room))
            connection.commit()
            return True

        except DataInsertionException as e:
            print(f"{e.__class__.__name__}: {e}")
            return False

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def delete_student_course(self, student_id, course_section):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = "DELETE FROM student_course WHERE student_id = %s AND course_section = %s"
                data_cursor.execute(query, (student_id, course_section))

            connection.commit()
            return True

        except DataDeletionException as e:
            print(f"{e.__class__.__name__}: {e}")
            return False

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def update_student_course(self,
                              student_id: str,
                              course_id: str = None,
                              course_title: str = None,
                              course_year: int = None,
                              course_term: int = None,
                              course_section: str = None,
                              course_units: int = None,
                              course_days: str = None,
                              course_time: str = None,
                              course_room: str = None):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                update_columns = [(col, val) for col, val in [('course_id', course_id), ('course_title', course_title),
                                                              ('course_year', course_year), ('course_term', course_term),
                                                              ('course_section', course_section),
                                                              ('course_units', course_units),
                                                              ('course_days', course_days), ('course_time', course_time),
                                                              ('course_room', course_room)] if val is not None]
                query = (f"UPDATE courses SET {', '.join([f'{col} = %s' for col, val in update_columns])} "
                         f"WHERE student_id = %s")

        except DataUpdateException as e:
            print(f"{e.__class__.__name__}: {e}")
            return False

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def select_student_course(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                pass

        except DataSelectionException as e:
            print(f"{e.__class__.__name__}: {e}")
            return False

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()
