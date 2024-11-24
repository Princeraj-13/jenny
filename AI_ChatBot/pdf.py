import os
import json
from groq import Groq
from dotenv import load_dotenv
import pyautogui
from fpdf import FPDF
import datetime
import platform  # Import platform module to check the OS

load_dotenv()

# File to store conversation history
history_file = 'conversation_history.json'
pdf_folder = 'pdf'  # Specify the folder where PDFs will be saved

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

# Function to create a PDF file with the generated response
def create_pdf(response_text):
    # Ensure the pdf folder exists
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add a cell with the response text
    pdf.multi_cell(0, 10, response_text)
    
    # Create a unique filename using the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = os.path.join(pdf_folder, f"response_{timestamp}.pdf")  # Save in pdf folder
    
    # Save the PDF file
    pdf.output(pdf_filename)
    print(f"PDF saved as {pdf_filename}")

    # Open the PDF file with the default viewer
    open_pdf(pdf_filename)

def open_pdf(pdf_filename):
    # Check the operating system and open the PDF file accordingly
    if platform.system() == "Windows":
        os.startfile(pdf_filename)  # For Windows
    elif platform.system() == "Darwin":
        os.system(f"open {pdf_filename}")  # For macOS
    else:
        os.system(f"xdg-open {pdf_filename}")  # For Linux

def generate_pdf(query):
    # Initialize the client with your API key
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Define the system prompt
    system_prompt = "Your name is Jenny, A cutting edge Artificial voice assistant, developed by Prince Raj. act like genius and very smart voice assistant who knows almost everything in every topic. you are kind, humble and respected teacher voice assistant and you never make feel bored to the users with your long response. and you always call everyone by saying sir "

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

        # Create a PDF file with the response text
        create_pdf(response_text)

        return (query, response_text)
    else:
        return None

if __name__ == "__main__":
    result = generate_pdf("esaay on cow")
    if result:
        print(result)