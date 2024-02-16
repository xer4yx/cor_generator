import mysql.connector
from sprints.exceptions.customexceptions import *


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

    def delete_student_course(self, student_id, course_section=None):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                if course_section is not None:
                    query = "DELETE FROM student_course WHERE student_id = %s AND course_section = %s"
                    data_cursor.execute(query, (student_id, course_section))
                else:
                    query = "DELETE FROM student_course WHERE student_id = %s"
                    data_cursor.execute(query, (student_id,))

            connection.commit()
            return True

        except DataDeletionException as e:
            print(f"{e.__class__.__name__}: {e}")
            return False

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def delete_all_student_courses(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = "DELETE FROM student_course"
                data_cursor.execute(query)

            connection.commit()
            return True

        except DataDeletionException as e:
            print(f"{e.__class__.__name__}: {e}")
            return False

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def select_student_courses(self, student_id: str):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = "SELECT * FROM student_course WHERE student_id = %s"
                data_cursor.execute(query, (student_id,))
                results = data_cursor.fetchall()
                return results

        except mysql.connector.Error as e:
            print(f"Error selecting student courses: {e}")
            return []

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()
