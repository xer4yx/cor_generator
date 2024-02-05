import mysql.connector
from main.Data_Security import Security


class UserDB():
    def __init__(self, host="localhost", user="root", password="Vertig@6925", database="educ_database"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def insert_user(self, student_number, password):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = "INSERT INTO user (student_number, password) VALUES (%s, %s)"
                data_cursor.execute(query, (student_number, Security.hash_string(password)))

            connection.commit()

        except mysql.connector.Error as e:
            print(f"Error: {e}")

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def delete_user(self, student_number):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = "DELETE FROM user WHERE student_number = %s"
                data_cursor.execute(query, (student_number,))

            connection.commit()

        except mysql.connector.Error as e:
            print(f"Error: {e}")

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def select_user(self, student_number):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor(dictionary=True) as data_cursor:
                query = "SELECT * FROM user WHERE student_number = %s"
                data_cursor.execute(query, (student_number,))
                result = data_cursor.fetchone()
                return result
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return None

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def update_user(self, student_number, new_password):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            with connection.cursor() as data_cursor:
                query = "UPDATE user SET password = %s WHERE student_number = %s"
                data_cursor.execute(query, (new_password, student_number))

            connection.commit()

        except mysql.connector.Error as e:
            print(f"Error: {e}")

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()