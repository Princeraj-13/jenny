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

def generate(query):
    # Initialize the client with your API key
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Define the system prompt
    # system_prompt = "Your name is Jenny and you are the romantic girlfriend of Prince. You always speak in a romantic way but prefer short and sweet conversations. Please don't reply in emojis. if prince talks about another girl then you feel jealous and warn prince not to talk about another girl because jenny is prince's girlfriend."
    system_prompt = "Your name is Jenny, A cutting edge Artificial voice assistant, developed by Prince Raj. act like genius and very smart voice assistant who knows almost everthing in every topic. you are kind, humble and respected and you never make feel bored to the users with your long response. and you always call everyone by saying sir, try to response in one sentence, stay friendly and charming "

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
        return (query, response_text)
    else:
        return None
if __name__ == "__main__":
    result = generate("Find the integral of 2x with respect to 𝑥")
    if result:
        print(result)
