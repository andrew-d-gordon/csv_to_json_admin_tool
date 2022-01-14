# General imports
import sys

# Local imports
from common.handle_errors import handle_error

# Global values for Course or course input data
desired_columns_courses = ('id', 'name', 'teacher')  # Referenced when parsing school data csv input
course_weight_total = 100


# Class to hold data pertinent to a course as per the spec, can return dictionary version of itself
class Course:
    def __init__(self, course_id: int = None, name: str = None, teacher: str = None):
        self.id = course_id
        self.name = name
        self.teacher = teacher
        self.course_average = 0.0  # Must be set via set course average function, fed with student id, tests and marks
        self.test_weights = 0  # To be a sum of test weights, incremented via add_test_weight

    # Turn course into a dictionary object
    def course_as_dict(self):
        return {'id': self.id, 'name': self.name, 'teacher': self.teacher, 'courseAverage': self.course_average}

    # Add weight to course test weight total, validate the current total (<=100)
    def add_test_weight(self, test_weight: int):
        self.test_weights += test_weight
        if self.test_weights > 100:
            handle_error(f'Invalid course weights. Course has id: {self.id}, weight total is not {course_weight_total}.'
                         f' Total: {self.test_weights}')
