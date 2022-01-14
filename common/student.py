# Public values related to Student or student input data
desired_columns_students = ('id', 'name')  # Referenced when parsing school data csv input


# Class to hold data pertinent to a student as per the spec, can return dictionary version of itself
class Student:
    def __init__(self, student_id: int = None, name: str = None):
        self.id = student_id
        self.name = name
        self.total_average = 0.0  # To be computed from all weighted average of each course average
        self.courses = {}  # Filled out after init, will hold a students set of courses and test scores for the course
        self.course_averages = {}  # Filled out after init, will hold keys as course_ids and values as course averages
        self.marks = {}  # Filled out after init, keys are test_id and values are marks on said test for this student

    # # Turn student into a dictionary object
    def student_as_dict(self):
        return {'id': self.student_id, 'name': self.name, 'totalAverage': self.total_average, 'courses': self.courses}

    # Generate course average for a student given courses with tests and marks for a student
    def compute_course_averages(self):
        total_points = 0
        for c in self.courses:
            course_tests = self.courses[c]
            tests_taken = len(course_tests)
            course_average = 0.0  # Will hold value determined by the mark they get in each test and test's weight
            for test in course_tests:  # Iterate through tests and scores for student in course c, find course average
                # test contains: (test_id (int), student marks on test (int), test weight (int))
                course_average += test[1] * test[2]/100  # Add student_marks multiplied by (test_weight / 100) to avg

            self.course_averages[c] = round(course_average, 2)  # Store course average for course, rounded to 2 decimals

        print("Student with id and course averages:", self.id, self.course_averages)

    # Generate total average for a student given courses with a course average for the student
    def compute_total_average(self):
        courses_taken = 0
        total_marks = 0
        for course_id in self.course_averages:
            total_marks += self.course_averages[course_id]
            courses_taken += 1

        self.total_average = round(total_marks / courses_taken, 2)
