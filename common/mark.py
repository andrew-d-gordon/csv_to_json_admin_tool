# Global values for Test or test input data
desired_columns_marks = ('test_id', 'student_id', 'mark')  # Referenced when parsing school data csv input


# Class to hold data pertinent of a test as per the spec, can return dictionary version of itself
class Mark:
    def __init__(self, test_id: int = None, student_id: int = None, mark: int = None):
        self.test_id = test_id
        self.student_id = student_id
        self.mark = mark

    def mark_as_dict(self):
        return {'test_id': self.test_id, 'student_id': self.student_id, 'mark': self.mark}
