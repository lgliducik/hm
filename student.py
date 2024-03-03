import csv
import functools
import argparse
import logging

logging.basicConfig(filename='logger.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger()


class Validate:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.name, value)

    def validate(self, value):
        if not value.istitle() or not functools.reduce(lambda a, b: a * b, [i.isalpha() for i in value.split()]):
            logger.error("ФИО должно состоять только из букв и начинаться с заглавной буквы")
            raise ValueError('ФИО должно состоять только из букв и начинаться с заглавной буквы')


class Student:
    name = Validate()

    def load_subjects(self, subjects_file):
        with open(subjects_file, encoding="utf8", newline='\n') as csvfile:
            subjects_reader = csv.reader(csvfile, delimiter=' ', quotechar=',')
            for row in subjects_reader:
                self.subjects = {subject: {'test_score': [], 'grade': []} for subject in row[0].split(',')}

    def __init__(self, name, subjects_file):
        self.name = name
        self.subjects = {}
        self.load_subjects(subjects_file)

    def __setattr__(self, name, value):
        if name == "name":
            if not value.istitle() or not functools.reduce(lambda a, b: a * b, [i.isalpha() for i in value.split()]):
                logger.error("ФИО должно состоять только из букв и начинаться с заглавной буквы")
                raise ValueError('ФИО должно состоять только из букв и начинаться с заглавной буквы')
        object.__setattr__(self, name, value)

    def __getattr__(self, name):
        if name == "name":
            return f"{self.name}"
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __str__(self):
        subj = list(filter(lambda x: len(self.subjects[x]['grade']) > 0, self.subjects.keys()))
        return f'Студент: {self.name}\nПредметы: {", ".join(subj)}'

    def add_grade(self, subject, grade):
        if 5 >= grade >= 2:
            if subject in self.subjects.keys():
                self.subjects[subject]['grade'].append(grade)
            else:
                logger.error(f'Предмет {subject} не найден')
                raise ValueError(f'Предмет {subject} не найден')
        else:
            logger.warning("Оценка должна быть целым числом от 2 до 5")

    def add_test_score(self, subject, test_score):
        if 100 >= test_score > 0:
            self.subjects[subject]['test_score'].append(test_score)
        else:
            logger.warning("Результат теста должен быть целым числом от 0 до 100")

    def get_average_test_score(self, subject):
        if subject in self.subjects.keys():
            size = len(self.subjects[subject]['test_score'])
            if size > 0:
                return sum(self.subjects[subject]['test_score'])/size
        else:
            logger.error(f'Предмет {subject} не найден')
            raise ValueError(f'Предмет {subject} не найден')

    def get_average_grade(self):
        marks = []
        for subject in self.subjects.keys():
            size = len(self.subjects[subject]['grade'])
            if size > 0:
                marks.append(sum(self.subjects[subject]['grade']) / size)
        new_lst = list(filter(lambda x: x is not None, marks))
        size = len(new_lst)
        if size > 0:
            return sum(new_lst)/size


def main():
    parser = argparse.ArgumentParser(description='My first argument parser')
    parser.add_argument('file_name', metavar='N', type=str, nargs='*', help='press some filename')
    args = parser.parse_args()
    logger.info(f'В скрипт передано: {args}')
    if args.file_name:
        file_name_csv = args.file_name[0]
        logger.info(f'Переданное имя файла: {args.file_name[0]}')
    else:
        file_name_csv = "subjects.csv"
        logger.info(f'Аргументы не переданы(имя файла по умолчанию): {file_name_csv}')

    student = Student("Иван Иванов", file_name_csv)
    # python ./student.py subjects.csv

    student.add_grade("Математика", 4)
    student.add_test_score("Математика", 85)

    student.add_grade("История", 5)
    student.add_test_score("История", 92)

    average_grade = student.get_average_grade()
    logger.info(f"Средний балл: {average_grade}")

    average_test_score = student.get_average_test_score("Математика")
    logger.info(f"Средний результат по тестам по математике: {average_test_score}")

    logger.info(student)


if __name__ == "__main__":
    main()
