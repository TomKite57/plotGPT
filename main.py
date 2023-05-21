
import openai
from dotenv import load_dotenv
import os, sys
import argparse

# CONSTANTS
OPENAI_TOKEN = None
MODEL = "gpt-3.5-turbo"
TEMPERATURE = 1.0

# FUNCTIONS
def wrap_message(user, message):
    if user not in ["system", "user", "assistant"]:
        raise ValueError("user must be one of 'system', 'user', or 'assistant'")
    return {"role": user, "content": message}

def conversation_api_call(messages):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=TEMPERATURE,
    )
    return response

def file_exists(filename):
    return os.path.isfile(filename)

def create_system_message(filename):
    #desc = f"""You must produce a short python script which produces a plot from the file {filename} according to the user description. You must use matplotlib, and end the script with 'plt.show()'. Your code will not be seen by the user, only executed. Return code ONLY, no text."""
    desc = f"""Complete the following program to produce a plot according to the user description. Return code ONLY, no text.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
df = pd.read_csv('{filename}')

# YOUR CODE HERE

plt.show()"""
    return desc

# INITIAL SETUP
load_dotenv()

OPENAI_TOKEN = os.environ.get('OPENAI_TOKEN')

if OPENAI_TOKEN is None:
    sys.exit("Could not find OPENAI API key. Please set OPENAI_TOKEN in .env file.")

openai.api_key = OPENAI_TOKEN

# MAIN FUNCTION
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                    prog="chatGPT",
                    description="chatGPT will create a plot of your data based on your description.",
                    epilog="Tom Kite 2023")
    parser.add_argument("filename", help="The filename of the data you want to plot", type=str, nargs=1)
    parser.add_argument("description", help="A description of the plot you want to create", type=str, nargs="+")
    parser.add_argument("-d", "--data", help="A description of the data you want to plot", required=False, type=str, nargs="+", dest="data_description", default=None)
    parser.add_argument("-v", "--verbose", help="Prints out extra information", action="store_true", dest="verbose")

    #args = sys.argv
    args = parser.parse_args(sys.argv[1:])
    filename = args.filename[0]
    description = " ".join(args.description)
    data_description = " ".join(args.data_description) if args.data_description is not None else None
    verbose = args.verbose

    # Conversation object
    conversation = []

    # System message
    system = create_system_message(filename)
    wrapped_system = wrap_message("system", system)
    conversation.append(wrapped_system)

    # Data description
    if data_description is not None:
        wrapped_data_description = wrap_message("user", f"Description of data: {data_description}")
        conversation.append(wrapped_data_description)

    # User description
    wrapped_description = wrap_message("user", f"Desciption of plot: {description}")
    conversation.append(wrapped_description)

    if (verbose):
        print(f"System: {system}")
        print(f"Filename: {filename}")
        print(f"Plot description: {description}")
        print(f"Data description: {data_description}")

    response_json = conversation_api_call(conversation)
    response = response_json["choices"][0]["message"]["content"]

    response = response.strip("```python")
    response = response.strip("```")

    if (verbose):
        print(f"Plotting code:\n\n{response}\n\n")

    exec(response)


