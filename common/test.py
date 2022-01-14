# Global values for Test or test input data
desired_columns_tests = ('id', 'course_id', 'weight')  # Referenced when parsing school data csv input


# Class to hold data pertinent of a test as per the spec, can return dictionary version of itself
class Test:
    def __init__(self, test_id: int = None, course_id: int = None, weight: int = None):
        self.id = test_id
        self.course_id = course_id
        self.weight = weight

    def test_as_dict(self):
        return {'id': self.test_id, 'course_id': self.course_id, 'weight': self.weight}
