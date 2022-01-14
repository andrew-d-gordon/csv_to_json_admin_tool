# General imports
import sys

# Local imports
from common.JSONWriter import JSONWriter

# Global values for error handling
out_writer = JSONWriter()  # Serves to hold writer object which can be set by set_error_JSONWriter


# Serves to set json writer object to use when writing output
def set_error_json_writer(json_writer: JSONWriter = None):
    global out_writer
    out_writer = json_writer


# Serves to write an "error" JSON object to an output file with a variable error message. Exits -1 on completion.
def handle_error(error_message: str):
    print(error_message)  # Print error message prior to writing it to output file
    if out_writer.output_file is None:
        print('No output file specified for JSONWriter in handle_errors.py. '
              'Use set_error_json_writer to provide valid JSONWriter.')
    error_json = {"error": error_message}  # Create error json object
    out_writer.write_json_to_output_file(error_json)  # Send object to be written to output file
    sys.exit(-1)  # Exit with error
