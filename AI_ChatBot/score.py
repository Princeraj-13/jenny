import os
import json
from groq import Groq
from dotenv import load_dotenv
import pyautogui
load_dotenv()

# File to store conversation history
history_file = 'conversation_history.json'

# Function to load conversation history
def load_history():
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            return json.load(file)
    return []

# Function to save conversation history
def save_history(history):
    with open(history_file, 'w') as file:
        json.dump(history, file, indent=4)

def score(query):
    # Initialize the client with your API key
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Define the system prompt
    system_prompt = "act like you are teacher and take test of student and the questions should be like mcq with options.By default ask 5 questions until the user command you the number of of questions. ask test question one by one, after telling the answer of 1st question go to 2nd question and repeat the same process until the question end. after all the target question ends, inform the obtained marks out of total marks with percentage. if the scored percentage is less than 50% then provide 20 more mcq questions for the student to practice and please don't make your response long, your response should be onto the point."

    # Load previous conversation history
    messages = load_history()

    # Include the system prompt if history is empty
    if not messages:
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    
    # Add the new user query to the conversation history
    messages.append({
        "role": "user",
        "content": query
    })

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=1,
        max_tokens=2024,
        top_p=1,
        stream=True,
        stop=None,
    )
    response_text = ""
    for chunk in completion:
        # Check if content is available in the chunk
        if chunk.choices and chunk.choices[0].delta.content:
            response_text += chunk.choices[0].delta.content
    
    if response_text:
        # Add the assistant's response to the conversation history
        messages.append({
            "role": "assistant",
            "content": response_text
        })
        save_history(messages)
        
        # Print the response
        print(response_text)
        
        # Write the response using pyautogui
        pyautogui.typewrite(response_text)
        
        return (query, response_text)
    else:
        return None

if __name__ == "__main__":
    result = score("where is the remaining questions?")
    if result:
        print(result)
        # pyautogui.typewrite(result)