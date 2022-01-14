# Design for School Data CSVs to JSON Python Project

As a note, more details regarding the high level function of this project are available in docs/spec.md, below will 
discuss programmatic components and design decisions.

**Components**:

 - Helper classes in `common/` are `course.py`, `student.py`, `test.py` and `mark.py`. These serve as ways to organize 
data for individual components as parsed by the input files. They also have helper functions serve to generate and 
validate attributes. This ranges from computing course average and total average for students, to ensuring that test 
weights for a given course add up to 100. An additional class is `JSONWriter.py`. It is a custom file writing object
which writes json objects out to a validated output file (validation of output file permissions is done in the class).
 - Helper files in `common/` via `parse_school_csvs.py` and `handle_errors.py`. The first retrieves input from the 
supplied csv file path args off command line. The second takes in an error message, creates a JSON version, writes it to
output, and then exits execution with code `-1`.

It certainly would be viable to not have classes for courses, students, tests, and marks. This project does not 
necessitate the use of classes, however having these classes and specifics to what data and types of data each type of
object should hold increases the re-usability and comprehension of the code. It is also nice to associate functions
relating to specific aspects of the input data with its class. For example, in `student.py`, there exists functions to
compute personal course averages and total course average which would be somewhat out of place if not together with 
student data related, code.

The `desired_column_[input_type]` variables present in each file (`course.py`, `student.py`, `test.py` and `mark.py`) 
provide a nice way of replacing literals that would be present in `parse_school_csv.py` error checking process.
While runtime and space complexity may be marginally larger as a result of these objects, I believe there is a valuable
trade off in understandability, re-usability, and organization. (This structure may want to be reconsidered if working
with large volumes of data in data streams or systems which have ever-changing data sets).
 
**Handling Errors**:

At any stage, if an error occurs, an error message is sent to global `JSONWriter` obj and a JSON object with a sole key
(being `"error"`) is given the error message as a value, is written to the output file, and ends execution by exiting 
with code `-1`. If the execution succeeds, the execution ends by exiting with code `0`.

**Control Flow**:

This project is driven by main.py, helper files and functions are provided within the root directory. It starts by 
collecting the command line arguments to find paths to the necessary input files (courses, students, tests, marks) and 
a desired output file.

Once file paths have been retrieved, work is done in `parse_school_csvs.py` to validate the input files contents and 
retrieve the data. It does this by generating a list for each input file with rows as dictionaries (keys are the
columns). Once these lists are generated, we utilize the helper classes within `course.py`, `student.py`, `test.py` to
create course objects, student objects and test objects. These objects are stored together in respective dictionaries, 
and can be accessed by their id (e.g. course_data[1] would retrieve the course object with id == 1). 

Once these dictionaries for courses, students, and tests have been generated, we can process the `marks` data to 
correlate  what scores a student got on tests, and by proxy which courses they are enrolled in. Each student object has 
an attribute called `courses` which is a dictionary that holds each course they took (keys = course_ids), as well as a 
list of each test the student took for that course (test_id, student marks for test, test weight).

Having this information, we can now calculate course average for a student in a given course, and once this is done for
each course a student took, we can calculate total average for that student (across all classes).

At this stage, we have all the information we need, so we work with `generate_school_data_json_object` in main.py to
create the final json dict object. This object is then sent to `main.py`'s JSONWriter in order to be written to the
output file path.

# Testing

An example run of `main.py` can be conducted with the tests in `test_admin_tool.py`, or from command line. 
`test_admin_tool.py` utilizes the `unittest` library for Python. The types of tests it runs ranges from empty inputs,
bad column names, duplicate entries, to working examples provided by the spec (for reference, the files in Example1 and 
Example2). It is able to verify that two JSON objects are equal, these can be from files and, or passed in dictionaries.
It not only checks for correct JSON objects (regardless of the order of items in the JSON dicts/files), it also ensures 
that the correct system exit code was provided (`-1` `for error, `0` for success).

If the `test_admin_tool.py` is not your cup of tea, you can also run its suite of tests by utilizing the below CLI
commands (from the source directory containing `main.py`):

**Tests which succeed**

- `python main.py tests/Example1/courses.csv tests/Example1/students.csv tests/Example1/tests.csv tests/Example1/marks.csv tests/test_outputs/outputExample1.json`
- `python main.py tests/Example2/courses.csv tests/Example2/students.csv tests/Example2/tests.csv tests/Example2/marks.csv tests/test_outputs/outputExample2.json`
- `python main.py tests/Example3ColsNoRows/courses.csv tests/Example3ColsNoRows/students.csv tests/Example3ColsNoRows/tests.csv tests/Example3ColsNoRows/marks.csv tests/test_outputs/outputExample3ColsNoRows.json`

**Tests which are meant to fail**

- `python main.py tests/Example4RowsNoCols/courses.csv tests/Example4RowsNoCols/students.csv tests/Example4RowsNoCols/tests.csv tests/Example4RowsNoCols/marks.csv tests/test_outputs/outputExample4RowsNoCols.json`
- `python main.py tests/Example5BadTestWeights/courses.csv tests/Example5BadTestWeights/students.csv tests/Example5BadTestWeights/tests.csv tests/Example5BadTestWeights/marks.csv tests/test_outputs/outputExample5BadTestWeights.json`
- `python main.py tests/Example6BadArguments/courses.csv tests/Example6BadArguments/students.csv tests/Example6BadArguments/tests.csv tests/Example6BadArguments/marks.csv tests/test_outputs/outputExample6BadArguments.json`
- `python main.py tests/Example7DuplicateStudents/courses.csv tests/Example7DuplicateStudents/students.csv tests/Example7DuplicateStudents/tests.csv tests/Example7DuplicateStudents/marks.csv tests/test_outputs/outputExample7DuplicateStudents.json`
- `python main.py tests/Example8DuplicateCourses/courses.csv tests/Example8DuplicateCourses/students.csv tests/Example8DuplicateCourses/tests.csv tests/Example8DuplicateCourses/marks.csv tests/test_outputs/outputExample8DuplicateCourses.json`
- `python main.py tests/Example9DuplicateTests/courses.csv tests/Example9DuplicateTests/students.csv tests/Example9DuplicateTests/tests.csv tests/Example9DuplicateTests/marks.csv tests/test_outputs/outputExample9DuplicateTests.json`
- `python main.py tests/Example0EmptyFiles/courses.csv tests/Example0EmptyFiles/students.csv tests/Example0EmptyFiles/tests.csv tests/Example0EmptyFiles/marks.csv tests/test_outputs/outputExample0EmptyFiles.json`