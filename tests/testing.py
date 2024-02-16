from main.Student import Student
from main.Admin import Admin
from sprints.Data_Security import Security

if __name__ == '__main__':
    privileges = Admin()
    # student.view_curriculum()
    # privileges.populate_tables()
    while True:
        choice = int(input("""
        COR GENERATOR TESTING
        [1] Student Menu
        [2] Exit Program
        
        Enter your choice: """))

        match choice:
            case 1:
                student = Student('202402101')
                student.student_menu()

            case 2:
                exit()
