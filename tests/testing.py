from main.student import Student
from main.admin import Admin
from sprints.datasecurity import Security
import time
import random


def _generate_student_id():
    return time.strftime("%Y%m") + str(random.randint(101, 999))

if __name__ == '__main__':
    # privileges = Admin()
    # privileges.add_user('admin')
    print(_generate_student_id())
