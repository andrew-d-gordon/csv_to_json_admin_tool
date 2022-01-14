# csv_to_json_admin_tool
Python Library for parsing CSV Data and building desired Json Objects to output files.

Additional information on use case and current implementation can be found in [spec.md](docs/spec.md) and 
[design.md](docs/design.md)

You can find documentation on my implementation and unit testing within the `docs/` folder.

The primary commands to run from command line are as described in the spec. I also implemented a file called 
`test_admin_tool.py` to utilize the `unittest` library for more intensive testing. That can simply be run with
`python test_admin_tool.py`. Each test file and respective outputs is available in the `tests/` dir.

No external libraries were used so no need to `pip install -r requirements.txt`. To see other code which I produced for 
use in main.py check out `common/` folder. This folder contains classes I used for various objects, parsing input,
handling errors and writing to output files. 

The code was tested on Python 3.9 and 3.10 environments.

Here are some example commands you can run using test files from the spec and my own (outputs end up in 
`tests/test_outputs`):

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

**Use**:
This project should not be utilized in relation to solving the same coding challenge on Hatchways. This is my, Andrew 
Gordon's, implementation of this project in relation to a company assessment. 
