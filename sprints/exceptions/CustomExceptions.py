import mysql.connector


class RegistrationError(Exception):
    def __init__(self, message="You are not yet registered!"):
        self.message = message
        super().__init__(self.message)


class CredentialError(Exception):
    def __init__(self, message="Invalid Username or Password"):
        self.message = message
        super().__init__(self.message)


class NullError(TypeError):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class DataInsertionException(mysql.connector.Error):
    def __init__(self, message="An error occurred while inserting data"):
        self.message = message
        super().__init__(self.message)


class DataDeletionException(mysql.connector.Error):
    def __init__(self, message="An error occurred while deleting data"):
        self.message = message
        super().__init__(self.message)


class DataUpdateException(mysql.connector.Error):
    def __init__(self, message="An error occurred while updating data"):
        self.message = message
        super().__init__(self.message)


class DataSelectionException(mysql.connector.Error):
    def __init__(self, message="An error occurred while selecting data"):
        self.message = message
        super().__init__(self.message)
