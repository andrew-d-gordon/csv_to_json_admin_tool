# General Imports
import sys

# Local Imports
from common.handle_errors import set_error_json_writer, handle_error
from common.parse_school_csvs import generate_school_data_row_lists
from common.JSONWriter import JSONWriter
from common.course import Course
from common.student import Student
from common.test import Test

# Global values pertinent to driver code for admin data tool
json_writer = JSONWriter()


# Generate JSON Output Dictionary to be written to output file
def generate_school_data_json_object(students: dict, courses: dict):
    """
    Generate school data json object attempts to create a dictionary that has a key of students with a value list that
    contains each student present in the input. The student list entries should be sorted increasing order by id and
    will contain a student's info, their total course average, as well as the courses they are taking (list). The course
    list will have entries containing information regarding the course, as well as the course average that student has.

    Per specification, output should structured as such:
        {
            "students": [
                {
                    "id": ...,
                    "name": ...,
                    "totalAverage": ...,
                    "courses": [
                        {
                            "id": ...,
                            "name": ...,
                            "teacher": ...,
                            "courseAverage": ...
                        },
                        ...
                    ]
                },
                ...
            ]
        }

    :param students: Contains data of students including courses, course averages, and total average
    :param courses: Contains data of courses such as ids, course names, and teacher names
    :return: a JSON dict containing a list of students, their courses and grades, as well as score averages
    """

    # Save sorted id order of students, ensures order by id in output
    student_id_order = sorted(students.keys())

    json_sd_output = {"students": []}  # This dict will hold output json data
    for s_id in student_id_order:
        student_obj = students[s_id]
        student_entry = {  # Create skeleton student entry with course list placeholder
            "id": student_obj.id,
            "name": student_obj.name,
            "totalAverage": student_obj.total_average,
            "courses": []
        }

        # Fill out courses list for student
        course_id_order = sorted(student_obj.course_averages)
        for course in course_id_order:
            course_entry = {  # Create course entry dict pulling info from courses dict and curr student object
                "id": course,
                "name": courses[course].name,
                "teacher": courses[course].teacher,
                "courseAverage": student_obj.course_averages[course]
            }

            student_entry["courses"].append(course_entry)

        # Add completed student entry to output
        json_sd_output["students"].append(student_entry)

    return json_sd_output


# Compute student averages (course averages, then total average)
def compute_student_averages(student_data: dict):
    """
    :param student_data: Dictionary containing all students (as objects, keys are student ids)
    :return: None, serves to compute course averages and total average for student
    """
    # Compute course averages for each student
    for s in student_data:
        student_data[s].compute_course_averages()

    # With course averages computed, now compute total average for each student
    for s in student_data:
        student_data[s].compute_total_average()


# Add test weights for courses to ensure they add up to desired amount
def check_course_test_weights(course_data: dict, test_data: dict):
    """
    :param course_data: Dictionary containing all courses (as objects, keys are courses ids)
    :param test_data: Dictionary containing all tests (as objects, keys are test ids)
    :return: None, serves to add test weights for each course, ensures amount adds up to 100 (else error)
    """
    for test in test_data:
        course_id_for_test = test_data[test].course_id
        # Add weight to respective course, allows for validation of test weight totals for courses
        course_data[course_id_for_test].add_test_weight(test_data[test].weight)


# Associate course participation and test results for said course, for each student
def associate_student_courses(student_data: dict, test_data: dict):
    """
    :param student_data: Dictionary containing all students (as objects, keys are student ids)
    :param test_data: Dictionary containing all tests (as objects, keys are test ids)
    :return: None, serves to find courses students have taken and associates their test scores for that course (id)
    """
    for s in student_data:
        student = student_data[s]
        # Correlate what courses a student is involved in from marks and tests data
        for test in student.marks:
            course_id_for_test = test_data[test].course_id  # Grab course id
            try:  # Add test, mark and test weight for student's list of tests, marks and weights for a given course
                student.courses[course_id_for_test].append((test, student.marks[test], test_data[test].weight))
            except KeyError:  # Init list to hold tuples of tests, marks and weights for a student in given course
                student.courses[course_id_for_test] = [(test, student.marks[test], test_data[test].weight)]


# Associate mark data to students marks dictionary (keys: test_id, value: marks aka test score)
def associate_student_marks(student_data: dict, marks_rows: list):
    """
    :param student_data: Dictionary containing all students (as objects, keys are student ids)
    :param marks_rows: List containing rows parsed from marks input file
    :return: None, serves to parse rows in marks and save off test information to student's marks dict (test results)
    """
    for r in marks_rows:
        try:  # Try to associate test and student test score (mark) with student
            student_id = int(r['student_id'])
            test_id = int(r['test_id'])
            student = student_data[student_id]
            student.marks[test_id] = int(r['mark'])  # Convert student marks for test (test score) to integer
        except KeyError:  # If no such student exists in the database, through an error due to bad entry in marks
            handle_error(f'No such student with id {r["student_id"]} exists. Found in marks with row: {r}')


# Function to generate a dictionary of objects from rows of input data (type can be set to Course, Student, or Test)
def generate_data_dict(input_rows: list, isCourse: bool = False, isStudent: bool = False, isTest: bool = False):
    """
    :param input_rows: Contains each row in csv file containing course data
    :param isCourse: boolean to determine whether rows being processed are course data
    :param isStudent: boolean to determine whether rows being processed are student data
    :param isTest: boolean to determine whether rows being processed are test data
    :return: a dictionary of objects with keys as the data id of the row (type determined by boolean arguments)
    """
    data = {}
    for r in input_rows:
        data_id = int(r['id'])  # Convert object (row) id to integer
        try:  # Check for duplicates, if object with duplicate id is received, produce error
            v = data[data_id]
            handle_error(f'Duplicate found with id {data_id}. Found with row: {r}')
        except KeyError:  # Unique object
            if isCourse:
                data[data_id] = Course(data_id, r['name'], r['teacher'])
            elif isStudent:
                data[data_id] = Student(data_id, r['name'])
            elif isTest:
                data[data_id] = Test(data_id, int(r['course_id']), int(r['weight']))

    return data


# Serves to process data from input files and convert them to json
def process_admin_data(courses_file: str, students_file: str, tests_file: str, marks_file: str, output_file: str):
    """
    This is the main driver function for this library. It is separated from the main start below so one can write unit
    test cases from other files and directly call this function. Such a file that makes use of this is the unit test
    file for this library called docs/test_admin_tool.py.

    :param courses_file: Contains path to courses csv file
    :param students_file: Contains path to students csv file
    :param tests_file: Contains path to tests csv file
    :param marks_file: Contains path to marks csv file
    :param output_file: Contains path to desired output file
    :return: Nothing, this function cues the parsing of input data, correlation between inputs, generating output JSON
    """

    # Set JSONWriter object output file path, validates permission to use output file as well
    json_writer.set_json_writer_output_file(output_file)
    # Send created json writer to be used for writing error messages in handle_errors.py
    set_error_json_writer(json_writer)

    # Generate row lists for courses, students, tests, and marks
    courses_rows, students_rows, tests_rows, marks_rows = generate_school_data_row_lists([courses_file,
                                                                                          students_file,
                                                                                          tests_file,
                                                                                          marks_file])

    # After lists of rows for each input file have been generated, we generate dicts to hold courses, students and tests
    # Generating Course, Student and Test data dict to hold objects representing rows in respective input files
    course_data = generate_data_dict(courses_rows, isCourse=True)
    student_data = generate_data_dict(students_rows, isStudent=True)
    test_data = generate_data_dict(tests_rows, isTest=True)

    # We can parse marks to correlate tests with students, and by proxy correlate student to courses they are in
    associate_student_marks(student_data, marks_rows)

    # Fill out student's courses dictionary with courses and respective tests, test weights, and student's test marks
    associate_student_courses(student_data, test_data)

    # We can validate the courses by guaranteeing the weights of tests in a class add up to desired amount (default 100)
    check_course_test_weights(course_data, test_data)

    # Compute averages for students in student_data
    compute_student_averages(student_data)

    # Generate school data json object for output
    json_output = generate_school_data_json_object(student_data, course_data)

    # Write school data json object to output file
    json_writer.write_json_to_output_file(json_output)

    # Print successful finish and exit
    print(f'Execution finished successfully, output can be viewed at {output_file}')
    sys.exit(0)


# Supply File Path Arguments of Input to main
def supply_arguments():
    """
    :return: paths to output file and necessary csv inputs: courses, students, tests, and marks
    """
    # Validate number of arguments to be 5 filenames (strings: input filenames + output filename)
    args = sys.argv
    num_args = len(args) - 1  # -1 to negate entry for main.py (at sys.argv[0]) in length
    if num_args < 5:  # Not enough file names specified
        handle_error('Too few file names specified in command line arguments.')
    elif num_args > 5:  # Too many file names specified
        handle_error('Too many file names specified in command line arguments.')

    return args[1:]


# Example run of main.py
# python main.py courses.csv students.csv tests.csv marks.csv output.json
if __name__ == '__main__':
    print("Starting admin tool from main...")
    # Retrieve command line arguments and store necessary file paths (args validated in supply_arguments), create writer
    courses_file_path, students_file_path, tests_file_path, marks_file_path, output_file_path = supply_arguments()

    # Send file paths from supplied arguments to process_admin_data
    process_admin_data(courses_file_path, students_file_path, tests_file_path, marks_file_path, output_file_path)

    sys.exit(0)
