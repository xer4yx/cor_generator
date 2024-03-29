import mysql.connector
from typing import List, Dict, Union, Sequence
from sprints.exceptions.customexceptions import *


class CourseDB:
    def __init__(self, host="localhost", user="root", password="Vertig@6925", database="educ_database"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def insert_single(self,
                      course_code: str,
                      title: str,
                      section: str,
                      units: int,
                      days: str,
                      time: str,
                      year: int,
                      term: int,
                      room: str = None) -> bool:
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = ("INSERT INTO course (course_code, title, section, units, days, time, room, year, term) "
                         "VALUES (%s, %s, %s, %s, %s, %s, IFNULL(%s, DEFAULT(room)), %s, %s)")
                data_cursor.execute(query, (course_code, title, section, units, days, time, room, year, term))

            connection.commit()
            return True

        except DataInsertionException as e:
            print(f"{e.__class__.__name__}: {e}")
            return False

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def insert_by_batch(self, courses: List[Dict[str, Union[str, int]]]) -> bool:
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = ("INSERT INTO course (course_code, title, section, units, days, time, room, year, term) "
                         "VALUES (%s, %s, %s, %s, %s, %s, IFNULL(%s, DEFAULT(room)), %s, %s)")
                for course in courses:
                    data_cursor.execute(query, (
                        course['course_code'], course['title'], course['section'], course['units'],
                        course['days'], course['time'], course['room'], course['year'], course['term']
                    ))

            connection.commit()
            return True

        except DataInsertionException as e:
            print(f"{e.__class__.__name__}: {e}")
            return False

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
                      room: str = None,
                      year: int = None,
                      term: int = None) -> bool:
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                update_columns = [(col, val) for col, val in [('title', title), ('section', section), ('units', units),
                                                              ('days', days), ('time', time), ('room', room),
                                                              ('year', year), ('term', term)] if val is not None]

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

    def delete_single_row(self, course: str, section: str) -> bool:
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = "DELETE FROM course WHERE course_code = %s AND section = %s"
                data_cursor.execute(query, (course, section))

            connection.commit()
            return True

        except DataDeletionException as e:
            print(f"{e.__class__.__name__}: {e}")
            return False

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def delete_all_row(self) -> bool:
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = "DELETE FROM course"
                data_cursor.execute(query)

            connection.commit()
            return True

        except DataDeletionException as e:
            print(f"{e.__class__.__name__}: {e}")
            return False

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def select_by_section(self, course: str, section: str) -> Sequence:
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = "SELECT * FROM course WHERE course_code = %s AND section = %s"
                data_cursor.execute(query, (course, section))
                result = data_cursor.fetchall()

                return result

        except DataSelectionException as e:
            print(f"{e.__class__.__name__}: {e}")

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def select_by_year(self, year: int) -> Sequence:
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = "SELECT * FROM course WHERE year = %s"
                data_cursor.execute(query, (year,))
                result = data_cursor.fetchall()

                return result

        except DataSelectionException as e:
            print(f"{e.__class__.__name__}: {e}")
            return []

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def select_all_row(self) -> Sequence:
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = "SELECT DISTINCT course_code, title, units, year, term FROM course ORDER BY year, term"
                data_cursor.execute(query)
                result = data_cursor.fetchall()

                return result

        except DataSelectionException as e:
            print(f"{e.__class__.__name__}: {e}")
            return []

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()
