
import openai
from dotenv import load_dotenv
import os, sys
import argparse

# Local imports
from prompts import *

# CONSTANTS
OPENAI_TOKEN = None

# INITIAL SETUP
load_dotenv()

OPENAI_TOKEN = os.environ.get('OPENAI_TOKEN')

if OPENAI_TOKEN is None:
    sys.exit("Could not find OPENAI API key. Please set OPENAI_TOKEN in .env file.")

openai.api_key = OPENAI_TOKEN

def main(filename, description):
    # INITIAL PLOT #
    print("Creating initial plot")
    code = initial_assistant(filename, description)
    
    # GET VERIFICATION #
    verification_attempts = 1
    while True:
        print(f"Verifying plot attempt {verification_attempts}")
        new_code = verification_assistant(filename, description, code)
        if new_code == code:
            print("Plot verified")
            break

        code = new_code
        verification_attempts += 1

        if verification_attempts > 3:
            print("Plot cannot be verified")
            break
    
    # RUN PLOT #
    error = None
    try:
        exec(code)
    except Exception as e:
        error = str(e)
    
    error_attempts = 1
    while error is not None:
        print(f"Fixing plot attempt {error_attempts}")
        new_code = error_assistant(filename, description, code, error)
        code = new_code
        try:
            exec(code)
            error = None
        except Exception as e:
            error = str(e)
        
        if error is None:
            print("Plot fixed")
            break
    
        error_attempts += 1
        if error_attempts > 3:
            print("Plot cannot be fixed")
            break

    if error is not None:
        print("Code cannot be fixed")
        return


# MAIN FUNCTION
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                    prog="chatGPT",
                    description="chatGPT will create a plot of your data based on your description.",
                    epilog="Tom Kite 2023")
    parser.add_argument("filename", help="The filename of the data you want to plot", type=str, nargs=1)
    parser.add_argument("description", help="A description of the plot you want to create", type=str, nargs="+")
    #parser.add_argument("-v", "--verbose", help="Prints out extra information", action="store_true", dest="verbose")

    #args = sys.argv
    args = parser.parse_args(sys.argv[1:])
    filename = args.filename[0]
    description = " ".join(args.description)

    main(filename, description)


