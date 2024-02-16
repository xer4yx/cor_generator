import mysql.connector


class RegistrationException(Exception):
    def __init__(self, message="You are not yet registered!"):
        super().__init__(message)


class CredentialException(Exception):
    def __init__(self, message="Invalid Username or Password"):
        super().__init__(message)


class NullException(TypeError):
    def __init__(self, message="NoneType not acceptable in this object"):
        super().__init__(message)


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
