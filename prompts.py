
import openai

# Local imports
from utils import *

def generate_initial_prompt(filename, description):
    return f"""\
You are an AI plotting tool. Create a plot using the following data and description formatted as JSON between triple backticks: \
\"\"\" \
{{\
    \"filename\": {filename}, \
    \"description\": {description} \
}}\
\"\"\" \
You must produce a short python script which produces a plot from the file according to the user description. You must use matplotlib, and end the script with 'plt.show()'. \
Return your code delimited by triple backticks, no text.
"""

def generate_verify_prompt(filename, description, code):
    return f"""You are an AI assistant to verify the quality of plotting scripts. Given the following user given filename, plot description, and plotting code \
\"\"\" \
{{\
    \"filename\": {filename}, \
    \"description\": {description} \
    \"code\": ```{code}``` \
}}\
\"\"\" \
verify that the code produces a plot that matches the description. \
Give your response delimited by triple backticks. \
If the code produces a plot that matches the description, return ```success```. \
If the code produces a plot that does not match the description, return a new code snippet. \
Do not return any other text.
"""

def generate_error_prompt(filename, description, code, error):
    return f"""You are an AI assistant to fix errors in plotting scripts. Given the following user given filename, plot description, plotting code and error message \
\"\"\" \
{{\
    \"filename\": {filename}, \
    \"description\": {description}, \
    \"code\": ```{code}```, \
    \"error\": {error} \
}}\
\"\"\" \
fix the code so that it produces a plot that matches the description. \
Give your response delimited by triple backticks. \
If you cannot fix the code, return ```failure```. \
If you can fix the code, return a new code snippet. \
Do not return any other text.
"""

def initial_assistant(filename, description):
    prompt = generate_initial_prompt(filename, description)
    conversation = [{"role": "system", "content": prompt}]
    response = conversation_api_call(conversation)
    code = response["choices"][0]["message"]["content"].strip("```python\n").strip("\n```")
    return code

def verification_assistant(filename, description, code):
    prompt = generate_verify_prompt(filename, description, code)
    conversation = [{"role": "system", "content": prompt}]
    response = conversation_api_call(conversation)
    new_code = response["choices"][0]["message"]["content"].strip("```python\n").strip("\n```")
    if new_code != "success":
        return new_code
    else:
        return code

def error_assistant(filename, description, code, error):
    prompt = generate_error_prompt(filename, description, code, error)
    conversation = [{"role": "system", "content": prompt}]
    response = conversation_api_call(conversation)
    new_code = response["choices"][0]["message"]["content"].strip("```python\n").strip("\n```")
    if new_code != "failure":
        return new_code
    else:
        return None