# General imports
import sys
import json


# A class which serves to create a custom json writer which can be used to write dictionary objects to output files
class JSONWriter:
    def __init__(self, output_file: str = None, indent_spaces: int = 2, sort_keys: bool = False, new_line: bool = True):
        self.output_file = output_file
        self.indent_spaces = indent_spaces
        self.sort_keys = sort_keys
        self.new_line = new_line

    # Serves to set output file for JSONWriter, ensures ability to open said file
    def set_json_writer_output_file(self, output_file):
        try:
            file = open(output_file, 'w')
            file.close()
            self.output_file = output_file
        except PermissionError:
            print('Cannot utilize desired output file due because of insufficient user permissions.')
            sys.exit(-1)

    # Serves to write students to json formatted as per the spec, example output in tests/Example1/output.json
    def write_json_to_output_file(self, json_data: dict):
        """
        :param json_data: json_data dict object to be written to file
        :return: None, serves to write json_data (dict) to an output file
        """

        with open(self.output_file, 'w') as output_file:  # Attempt to open output file and write json string in
            json.dump(json_data, output_file, indent=self.indent_spaces, sort_keys=self.sort_keys)
            if self.new_line:  # If new line at bottom of file desired, write it in
                output_file.write("\n")

        json_data.clear()  # Clear the dict
        output_file.close()  # Close the file

