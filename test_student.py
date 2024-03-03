from student import Student


def create_student():
    st = Student("Иван Иванов", "subjects.csv")
    st.add_grade("Математика", 4)
    st.add_test_score("Математика", 85)
    st.add_grade("История", 5)
    st.add_test_score("История", 92)
    return st


def test_employee_full_name():
    st = Student("Иван Иванов", "subjects.csv")
    assert st.name == "Иван Иванов"


def test_get_average_grade():
    st = create_student()
    average_grade = st.get_average_grade()
    assert average_grade == 4.5


def test_average_test_score():
    st = create_student()
    average_test_score = st.get_average_test_score("Математика")
    assert average_test_score == 85.0


def test_str():
    st = create_student()
    assert str(st) == 'Студент: Иван Иванов\nПредметы: Математика, История'
