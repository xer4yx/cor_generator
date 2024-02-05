import mysql.connector
from sprints.exceptions.CustomExceptions import *


class CourseDB:
    def __init__(self, host="localhost", user="root", password="Vertig@6925", database="educ_database"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def add_course(self,
                   course_code: str,
                   title: str,
                   section: str,
                   units: str,
                   days: str,
                   time: str,
                   room: str = None):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = ("INSERT INTO courses (course_code, title, section, units, days, time, room) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s)")

        except DataInsertionException as e:
            print(f"{e.__class__.__name__}: {e}")

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def delete_course(self, course: str, section: str):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = "DELETE FROM courses WHERE course = %s AND section = %s"
                data_cursor.execute(query, (course, section))

            connection.commit()
            return True

        except DataDeletionException as e:
            print(f"{e.__class__.__name__}: {e}")

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def update_course(self,
                      course_code: str,
                      title: str = None,
                      section: str = None,
                      units: str = None,
                      days: str = None,
                      time: str = None,
                      room: str = None):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                update_columns = [(col, val) for col, val in [('title', title), ('section', section), ('units', units),
                                                    ('days', days), ('time', time), ('room', room)] if val is not None]

                query = (f"UPDATE courses SET {', '.join([f'{col} = %s' for col, val in update_columns])} "
                         f"WHERE course_code = %s AND section = %s")
                data_cursor.execute(query, [val for col, val in update_columns] + [course_code] + [section])

            connection.commit()
            return True

        except DataUpdateException as e:
            print(f"{e.__class__.__name__}: {e}")
            return False

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()
