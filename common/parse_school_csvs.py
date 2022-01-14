# General imports
import sys
import csv

# Local imports
from common.handle_errors import handle_error
from common.course import desired_columns_courses
from common.student import desired_columns_students
from common.test import desired_columns_tests
from common.mark import desired_columns_marks

# Global values related to parsing input csv data
# Tuple with columns expected for each input file, used to error check columns in input
input_columns = (
    desired_columns_courses,    # Courses, file_count=0
    desired_columns_students,   # Students, file_count=1
    desired_columns_tests,      # Tests, file_count=2
    desired_columns_marks       # Marks, file_count=3
)
bad_columns_msg = 'Columns in input file {0} are insufficient. It does not contain necessary column: {1}.'


# Validate input file row, column's which are cross checked determined by list of columns at input_columns[file_count]
def validate_input_rows(file_count: int, file_name: str, csv_row: dict):
    """
    :param file_name: name of input csv file which provides csv_row
    :param csv_row: example row from input csv
    :param file_count: file count specifying which input file's rows are being validated
    :return: Nothing, throws error and halts execution if invalid/insufficient columns are provided
    """
    for c in input_columns[file_count]:
        try:  # See if csv_row parsed from input file at file_name has necessary args for it's position in sys args.
            v = csv_row[c]
        except KeyError:  # Desired column name not found in provided csv row, input csv file has invalid rows
            handle_error(bad_columns_msg.format(file_name, c))


# Parse Input Files
def generate_school_data_row_lists(input_files: list[str]):
    """
    :param input_files: list with input csv files as strings ordered as follows: courses, students, tests, and marks
    :return: list with relevant dictionaries for inputs ordered as follows: courses, students, tests and marks
    """

    # print('Generating lists of rows for school data files corresponding to: courses, students, tests, and marks')
    input_files_rows = []  # Serves to hold parsed rows from input files provided (ordered synonymous with input_files)
    file_count = 0  # Serves as a pointer to what file in input_files is being parsed
    for f in input_files:
        try:  # Try to read input file
            csv_file = open(f, mode='r')
            csv_as_rows = list(csv.DictReader(csv_file))  # Retrieve data from csv as list with rows as dicts

            for r in csv_as_rows:
                # Validate rows for input file (uses first row as sample)
                validate_input_rows(file_count, f, r)
                # Strip extra spaces from beginning and end of row entries (e.g. " Mrs. P  " -> "Mrs. P")
                for k in r:
                    r[k] = r[k].strip()

            # Add valid, parsed rows from input file f to input_files_rows
            input_files_rows.append(csv_as_rows)

            # Close file after reading is finished
            csv_file.close()

        except FileNotFoundError:  # If file at f path is not found, throw error
            handle_error(f'There was an error opening input file with path: {f}')

        file_count += 1  # Shift file pointer forward

    return input_files_rows
