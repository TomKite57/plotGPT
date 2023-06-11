import openai

MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.0
        
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