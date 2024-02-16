from main.Student import Student
from main.Admin import Admin
from sprints.Data_Security import Security

if __name__ == '__main__':
    privileges = Admin()
    privileges.add_user('admin')