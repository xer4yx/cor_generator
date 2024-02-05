from main.Data_Security import Security
from sprints.database.User_DB import UserDB

if __name__ == '__main__':
    username = str('admin')
    password = str('password123')
    udb = UserDB()
    Security.check_credentials(username, password)
