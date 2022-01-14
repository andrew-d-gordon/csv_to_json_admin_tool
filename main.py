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


# Serves to process data from input files and convert them to json
def process_admin_data(courses_file: str, students_file: str, tests_file: str, marks_file: str, output_file: str):

    # Set JSONWriter object output file path, validates permission to use output file as well
    json_writer.set_json_writer_output_file(output_file)
    # Send created json writer to be used for writing error messages in handle_errors.py
    set_error_json_writer(json_writer)

    # Generate row lists for courses, students, tests, and marks
    courses_rows, students_rows, tests_rows, marks_rows = generate_school_data_row_lists([courses_file,
                                                                                          students_file,
                                                                                          tests_file,
                                                                                          marks_file])

    # print(f'Lists of rows for courses, students, tests, and marks:\n'
    #       f'{courses_rows}\n{students_rows}\n{tests_rows}\n{marks_rows}')

    # After lists of rows for each input file have been generated, we generate dicts to hold courses, students and tests
    # Generating course data dict to hold course objects (one for each course parsed from input file)
    course_data = {}
    for r in courses_rows:
        course_id = int(r['id'])  # Convert course id to integer
        try:  # Check for duplicates, if course with duplicate id is received, produce error
            v = course_data[course_id]
            handle_error(f'Duplicate course found with id {course_id}. Found in course_data with row: {r}')
        except KeyError:  # Unique course
            course_data[course_id] = Course(course_id, r['name'], r['teacher'])

    # Generating student data dict to hold student objects (one for each student parsed from input file)
    student_data = {}
    for r in students_rows:
        student_id = int(r['id'])  # Convert student id to integer
        try:  # Check for duplicates, if student with duplicate id is received, produce error
            v = student_data[student_id]
            handle_error(f'Duplicate student found with id {student_id}. Found in student_data with row: {r}')
        except KeyError:  # Unique student
            student_data[student_id] = Student(student_id, r['name'])

    # Generating test data list to hold test objects (one for each student parsed from input file)
    # After this step, we can validate the courses by guaranteeing the weights of tests in a class add up to 100
    test_data = {}
    for r in tests_rows:
        test_id = int(r['id'])  # Convert test id to integer
        try:  # Check for duplicates, if test with duplicate id is received, produce error
            v = test_data[test_id]
            handle_error(f'Duplicate test found with id {test_id}. Found in test_data with row: {r}')
        except KeyError:  # Unique test
            test_data[test_id] = Test(test_id, int(r['course_id']), int(r['weight']))

    # We can parse marks to correlate tests with students, and by proxy correlate student to courses they are in
    for r in marks_rows:
        try:  # Try to associate test and student test score (mark) with student
            student_id = int(r['student_id'])
            test_id = int(r['test_id'])
            student = student_data[student_id]
            student.marks[test_id] = int(r['mark'])  # Convert mark to integer
        except KeyError:  # If no such student exists in the database, through an error due to bad entry in marks
            handle_error(f'No such student with id {r["student_id"]} exists. Found in marks with row: {r}')

    # Fill out student's courses dictionary with courses and respective tests, test weights, and student's test marks
    for s in student_data:
        student = student_data[s]
        # Correlate what courses a student is involved in from marks and tests data
        for test in student.marks:
            course_id_for_test = test_data[test].course_id  # Grab course id
            try:  # Add test, mark and test weight for student's list of tests, marks and weights for a given course
                student.courses[course_id_for_test].append((test, student.marks[test], test_data[test].weight))
            except KeyError:  # Init list to hold tuples of tests, marks and weights for a student in given course
                student.courses[course_id_for_test] = [(test, student.marks[test], test_data[test].weight)]

    # Attribute tests to courses by counting the test weights, if a courses total weight exceeds 100, error thrown
    for test in test_data:
        course_id_for_test = test_data[test].course_id
        # Add weight to respective course, allows for validation of test weight totals for courses
        course_data[course_id_for_test].add_test_weight(test_data[test].weight)

    # Compute course averages for each student
    for s in student_data:
        # print(f"Student {s} courses and test scores: {student_data[s].courses}")
        student_data[s].compute_course_averages()

    # With course averages computed, now compute total average for each student
    for s in student_data:
        student_data[s].compute_total_average()

    # Generate school data json object for output
    json_output = generate_school_data_json_object(student_data, course_data)

    # Write school data json object to output file
    json_writer.write_json_to_output_file(json_output)

    # Exit successfully
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
# Main Driver
if __name__ == '__main__':
    print("Starting admin tool...")
    # Retrieve command line arguments and store necessary file paths (args validated in supply_arguments), create writer
    courses_file_path, students_file_path, tests_file_path, marks_file_path, output_file_path = supply_arguments()

    # Send file paths from supplied arguments to process_admin_data
    process_admin_data(courses_file_path, students_file_path, tests_file_path, marks_file_path, output_file_path)
