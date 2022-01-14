# Project Specification: School Data CSVs to JSON, Telivy

**Project Description**:

You’re a Jr. Dev working at a company that has just been granted a contract for building
a teacher’s admin tool for the local high school! Different teams have been assembled
to take on different parts of the app, your team will be working on the dashboard for the
school principal.

One specific feature your client wanted was to be able to quickly generate and visualize
report cards from .csv files containing the student courses and grades. The front-end
developers in your team are already working on displaying the reports, but they don’t
know how to parse .csv files and would rather be working with JSON data that is already
processed. This is where you come in.

Your manager needs you to build a tool that reads these .csv files, parses them,
calculates the students’ final grades and generates the report as a structured JSON file
that can easily be consumed by the front-end.

**Inputs**:

_courses.csv_: File contains courses that a student is taking. Each Course has a unique id, a name, and a teacher.

_students.csv_: File contains all existing students in database. Each student has a unique id and a name.

_tests.csv_: File contains all tests for each course in courses.csv file. File has three columns:
 - id: the unique test id
 - course_id: course id that this test belongs to
 - weight: worth of test for specific course. e.g. if test is worth 50, it is worth 50% of final grade for the course
   - Sum of all weights of every test in a particular course should add up to 100, else output should be an error

_marks.csv_: File contains all the marks each student has received for every test they have taken. File has three columns:
 - test_id: the test's id
 - student_id: the student's id
 - mark: The percentage grade the student received for the test (out of 100)
   - Notes: Not every student is enrolled in all courses - a student is considered to be enrolled in a course if they  have taken at least one test for that course.

**Output**:

A JSON File with a list of student's (ordered increasing by id) and their respective id's, names, avg grade as  well as courses and their relevant info. An example output is available in tests/Example1/output.json
More notes on output:
 - The data is contained within an object with a “students” key
 - The students are ordered by id (the courses don’t have to be ordered)
 - The ids and grades are numbers
 - Grades are rounded to two digits
 - The totalAverage is the average of all the courses the student is enrolled in
 - The student’s courseAverage in each course is determined by the mark they get in each test, and how much each test is
worth
 - Not all data from the .csv files appears in the report.

**Validation**: 

Validate output is valid JSON with https://jsonlint.com/

**Testing**:

Making use of unit tests in test_admin_tool.py or by running main.py with desired .csv input files as args + output file
Use instructions from command line and example:

`{path-to-courses-file} {path-to-students-file} {path-to-tests-file} {path-to-marks-file} {path-to-output-file}`

`“python main.py tests/Example1/courses.csv tests/Example1/students.csv tests/Example1/tests.csv tests/Example1/marks.csv 
tests/test_outputs/output.json”`
