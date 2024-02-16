from main.student import Student
from main.admin import Admin
from sprints.datasecurity import Security

if __name__ == '__main__':
    privileges = Admin()
    privileges.add_user('admin')