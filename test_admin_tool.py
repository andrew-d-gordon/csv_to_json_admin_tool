# General imports
import unittest
import json

# Local Imports
from main import process_admin_data


def print_test_header(test_name: str = ""):
    print('\n=======================')
    print('Started Test: {0}'.format(test_name))


def print_test_finished(test_name: str = ""):
    print('Completed Test: {0}'.format(test_name))


# Serves to check the equality of two JSON files or dictionaries (by elements, not literal order)
def json_content_equal(a, b, aIsFile: bool = False, bIsFile: bool = False):
    # If a or b are files, open them
    a_f = b_f = None
    if aIsFile: a_f = open(a, 'r')
    if bIsFile: b_f = open(b, 'r')

    # Load json objects from files or literal arguments to vars for comparison
    json_obj_a = json.load(a_f) if aIsFile else a
    json_obj_b = json.load(b_f) if bIsFile else b

    # Close files which were opened
    if aIsFile: a_f.close()
    if bIsFile: b_f.close()

    # Reference for this ordered func is here, clever solution to sort json objects recursively (Must be dicts to start)
    # https://stackoverflow.com/questions/25851183/how-to-compare-two-json-objects-with-the-same-elements-in-a-different-order-equa
    def ordered(obj):
        if isinstance(obj, dict):
            return sorted((key, ordered(val)) for key, val in obj.items())
        if isinstance(obj, list):
            return sorted(ordered(x) for x in obj)
        else:
            return obj

    # Compare both objects (should be dicts at this stage) as strings with keys sorted to check equality
    return ordered(json_obj_a) == ordered(json_obj_b)


class TestSchoolAdminTool(unittest.TestCase):
    def test_empty_files(self):
        test_name = 'Empty Files'
        print_test_header(test_name)

        input_files = ["tests/Example0EmptyFiles/courses.csv",  # Course data
                       "tests/Example0EmptyFiles/students.csv",  # Student data
                       "tests/Example0EmptyFiles/tests.csv",  # Test data
                       "tests/Example0EmptyFiles/marks.csv",  # Marks data
                       "tests/test_outputs/outputExample0EmptyFiles.json"]  # Desired output file

        # Set output json to compare against
        desired_output = {"error": "Input file: tests/Example0EmptyFiles/courses.csv, has no data in it."}

        # Run test, check output against desired output
        with self.assertRaises(SystemExit) as system_exit:
            process_admin_data(input_files[0], input_files[1], input_files[2], input_files[3], input_files[4])

        self.assertEqual(system_exit.exception.code, -1)
        self.assertTrue(json_content_equal("tests/test_outputs/outputExample0EmptyFiles.json",
                                           desired_output,
                                           True,
                                           False))

        print_test_finished(test_name)

    def test_example_1(self):
        test_name = 'Example 1 Test'
        print_test_header(test_name)

        input_files = ["tests/Example1/courses.csv",  # Course data
                       "tests/Example1/students.csv",  # Student data
                       "tests/Example1/tests.csv",  # Test data
                       "tests/Example1/marks.csv",  # Marks data
                       "tests/test_outputs/outputExample1.json"]  # Desired output file

        # Set output json to compare against
        desired_output = "tests/Example1/output.json"  # Desired output for example 1 input, provided by project spec

        # Run test, check output against desired output
        with self.assertRaises(SystemExit) as system_exit:
            process_admin_data(input_files[0], input_files[1], input_files[2], input_files[3], input_files[4])

        self.assertEqual(system_exit.exception.code, 0)
        self.assertTrue(json_content_equal("tests/test_outputs/outputExample1.json", desired_output, True, True))

        print_test_finished(test_name)

    def test_example_2(self):
        test_name = 'Example 2 Test'
        print_test_header(test_name)

        input_files = ["tests/Example2/courses.csv",  # Course data
                       "tests/Example2/students.csv",  # Student data
                       "tests/Example2/tests.csv",  # Test data
                       "tests/Example2/marks.csv",  # Marks data
                       "tests/test_outputs/outputExample2.json"]  # Desired output file

        # Set output json to compare against
        desired_output = "tests/Example2/output.json"  # Desired output for example 2 input, provided by project spec

        # Run test, check output against desired output
        with self.assertRaises(SystemExit) as system_exit:
            process_admin_data(input_files[0], input_files[1], input_files[2], input_files[3], input_files[4])

        self.assertEqual(system_exit.exception.code, 0)
        self.assertTrue(json_content_equal("tests/test_outputs/outputExample2.json", desired_output, True, True))

        print_test_finished(test_name)

    def test_cols_no_rows(self):
        test_name = 'Input has valid columns, but no row data'
        print_test_header(test_name)

        input_files = ["tests/Example3ColsNoRows/courses.csv",  # Course data
                       "tests/Example3ColsNoRows/students.csv",  # Student data
                       "tests/Example3ColsNoRows/tests.csv",  # Test data
                       "tests/Example3ColsNoRows/marks.csv",  # Marks data
                       "tests/test_outputs/outputExample3ColsNoRows.json"]  # Desired output file

        # Set output json to compare against
        # In my implementation, if the columns are valid, but no rows are specified, it will not error.
        # (i.e. input is valid but because no students exist in it, "students" in the output will be empty)
        desired_output = {"students": []}

        # Run test, check output against desired output
        with self.assertRaises(SystemExit) as system_exit:
            process_admin_data(input_files[0], input_files[1], input_files[2], input_files[3], input_files[4])

        self.assertEqual(system_exit.exception.code, 0)
        self.assertTrue(json_content_equal("tests/test_outputs/outputExample3ColsNoRows.json",
                                           desired_output,
                                           True,
                                           False))
        print_test_finished(test_name)

    def test_rows_no_cols(self):
        test_name = "Input has no column headers, but row data exists"
        print_test_header(test_name)

        input_files = ["tests/Example4RowsNoCols/courses.csv",  # Course data
                       "tests/Example4RowsNoCols/students.csv",  # Student data
                       "tests/Example4RowsNoCols/tests.csv",  # Test data
                       "tests/Example4RowsNoCols/marks.csv",  # Marks data
                       "tests/test_outputs/outputExample4RowsNoCols.json"]  # Desired output file

        # Set output json to compare against
        desired_output = {"error": "Columns in input file tests/Example4RowsNoCols/courses.csv are insufficient. "
                                   "It does not contain necessary column: id."}

        # Run test, check output against desired output
        with self.assertRaises(SystemExit) as system_exit:
            process_admin_data(input_files[0], input_files[1], input_files[2], input_files[3], input_files[4])

        self.assertEqual(system_exit.exception.code, -1)  # We expect system exit with -1 as code
        self.assertTrue(
            json_content_equal("tests/test_outputs/outputExample4RowsNoCols.json", desired_output, True, False))

        print_test_finished(test_name)

    def test_bad_test_weights(self):
        test_name = "Bad Test Weights"
        print_test_header(test_name)

        input_files = ["tests/Example5BadTestWeights/courses.csv",  # Course data
                       "tests/Example5BadTestWeights/students.csv",  # Student data
                       "tests/Example5BadTestWeights/tests.csv",  # Test data
                       "tests/Example5BadTestWeights/marks.csv",  # Marks data
                       "tests/test_outputs/outputExample5BadTestWeights.json"]  # Desired output file

        # Set output json to compare against
        desired_output = {"error": "Invalid course weights. Course has id: 1, weight total is not 100. Total: 110"}

        # Run test, check output against desired output
        with self.assertRaises(SystemExit) as system_exit:
            process_admin_data(input_files[0], input_files[1], input_files[2], input_files[3], input_files[4])

        self.assertEqual(system_exit.exception.code, -1)
        self.assertTrue(
            json_content_equal("tests/test_outputs/outputExample5BadTestWeights.json", desired_output, True, False))

        print_test_finished(test_name)

    def test_bad_arguments(self):
        test_name = "Bad Arguments"
        print_test_header(test_name)

        input_files = ["bad_file_path",  # Course data
                       "tests/Example6BadArguments/students.csv",  # Student data
                       "tests/Example6BadArguments/tests.csv",  # Test data
                       "tests/Example6BadArguments/marks.csv",  # Marks data
                       "tests/test_outputs/outputExample6BadArguments.json"]  # Desired output file

        # Set output json to compare against
        desired_output = {"error": "There was an error opening input file with path: bad_file_path"}

        # Run test, check output against desired output
        with self.assertRaises(SystemExit) as system_exit:
            process_admin_data(input_files[0], input_files[1], input_files[2], input_files[3], input_files[4])

        self.assertEqual(system_exit.exception.code, -1)
        self.assertTrue(
            json_content_equal("tests/test_outputs/outputExample6BadArguments.json", desired_output, True, False))

        print_test_finished(test_name)

    def test_duplicate_students(self):
        test_name = "Duplicate Students"
        print_test_header(test_name)

        input_files = ["tests/Example7DuplicateStudents/courses.csv",  # Course data
                       "tests/Example7DuplicateStudents/students.csv",  # Student data
                       "tests/Example7DuplicateStudents/tests.csv",  # Test data
                       "tests/Example7DuplicateStudents/marks.csv",  # Marks data
                       "tests/test_outputs/outputExample7DuplicateStudents.json"]  # Desired output file

        # Set output json to compare against
        desired_output = {"error": "Duplicate found with id 1. Found with row: {'id': '1', 'name': 'D'}"}

        # Run test, check output against desired output
        with self.assertRaises(SystemExit) as system_exit:
            process_admin_data(input_files[0], input_files[1], input_files[2], input_files[3], input_files[4])

        self.assertEqual(system_exit.exception.code, -1)
        self.assertTrue(
            json_content_equal("tests/test_outputs/outputExample7DuplicateStudents.json", desired_output, True, False))

        print_test_finished(test_name)

    def test_duplicate_courses(self):
        test_name = "Duplicate Courses"
        print_test_header(test_name)

        input_files = ["tests/Example8DuplicateCourses/courses.csv",  # Course data
                       "tests/Example8DuplicateCourses/students.csv",  # Student data
                       "tests/Example8DuplicateCourses/tests.csv",  # Test data
                       "tests/Example8DuplicateCourses/marks.csv",  # Marks data
                       "tests/test_outputs/outputExample8DuplicateCourses.json"]  # Desired output file

        # Set output json to compare against
        desired_output = {"error": "Duplicate found with id 1. Found with row: {'id': '1', 'name': 'Chemistry', "
                                   "'teacher': 'Mrs. E'}"}

        # Run test, check output against desired output
        with self.assertRaises(SystemExit) as system_exit:
            process_admin_data(input_files[0], input_files[1], input_files[2], input_files[3], input_files[4])

        self.assertEqual(system_exit.exception.code, -1)
        self.assertTrue(
            json_content_equal("tests/test_outputs/outputExample8DuplicateCourses.json", desired_output, True,
                               False))

        print_test_finished(test_name)

    def test_duplicate_tests(self):
        test_name = "Duplicate Tests"
        print_test_header(test_name)

        input_files = ["tests/Example9DuplicateTests/courses.csv",  # Course data
                       "tests/Example9DuplicateTests/students.csv",  # Student data
                       "tests/Example9DuplicateTests/tests.csv",  # Test data
                       "tests/Example9DuplicateTests/marks.csv",  # Marks data
                       "tests/test_outputs/outputExample9DuplicateTests.json"]  # Desired output file

        # Set output json to compare against
        desired_output = {"error": "Duplicate found with id 1. Found with row: {'id': '1', 'course_id': '2', 'weight': "
                                   "'10'}"}

        # Run test, check output against desired output
        with self.assertRaises(SystemExit) as system_exit:
            process_admin_data(input_files[0], input_files[1], input_files[2], input_files[3], input_files[4])

        self.assertEqual(system_exit.exception.code, -1)
        self.assertTrue(
            json_content_equal("tests/test_outputs/outputExample9DuplicateTests.json", desired_output, True,
                               False))

        print_test_finished(test_name)


if __name__ == '__main__':
    unittest.main()
