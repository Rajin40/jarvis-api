import os
import json
import re
from transformers import pipeline
from datetime import datetime

# Load the GPT-2 model for text generation
generator = pipeline("text-generation", model="gpt2")

# Define the folders where files will be saved
folders = {
    "python": "Python_code",  # Folder for Python code
    "mail": "Email",          # Folder for email/text output
    "json": "Store"           # Folder for JSON files
}

# Create folders if they don't exist
for folder in folders.values():
    os.makedirs(folder, exist_ok=True)

# Counter to generate unique file names
task_counter = 1

def ask_gpt2(prompt):
    """
    Function to query the GPT-2 model for task completion.
    """
    try:
        # Generate a response using GPT-2
        response = generator(prompt, max_length=150, num_return_sequences=1)
        answer = response[0]['generated_text'].strip()
        return answer
    except Exception as e:
        return f"Error: {e}"

def extract_python_code(text):
    """
    Function to extract Python code from the GPT-2 response.
    """
    # Use regex to find code blocks
    code_blocks = re.findall(r'```python(.*?)```', text, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    
    # Fallback: Look for lines that look like code
    lines = text.split("\n")
    code_lines = [line for line in lines if line.startswith(("def ", "import ", "    ", "from ", "class "))]
    return "\n".join(code_lines)

def save_to_file(folder, filename, content):
    """
    Function to save content to a file in the specified folder.
    """
    try:
        file_path = os.path.join(folder, filename)
        with open(file_path, "w") as file:
            file.write(content)
        print(f"Output saved to {file_path}")
    except Exception as e:
        print(f"Error saving to file: {e}")

def jervis_assistant(user_input):
    """
    Function to handle user input and fetch solutions from GPT-2.
    """
    global task_counter
    user_input = user_input.lower()  # Normalize input to lowercase

    if "work to do" in user_input or "do this" in user_input:
        # Extract the task description
        task_description = user_input.replace("work to do", "").replace("do this", "").strip()

        if not task_description:
            return "Jervis: Please specify a task."

        print(f"Jervis: Fetching solution for '{task_description}'...")
        
        # Modify the prompt to explicitly ask for Python code
        prompt = f"Write a complete Python script for: {task_description}. Provide only the raw Python code inside ```python``` blocks, no explanations."
        solution = ask_gpt2(prompt)
        
        # Extract only the Python code from the response
        python_code = extract_python_code(solution)
        output = f"Task: {task_description}\n\nSolution:\n{python_code}"

        # Generate a unique file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        python_filename = f"task_{task_counter}.py"
        text_filename = f"task_{task_counter}.txt"
        json_filename = f"task_{task_counter}.json"
        task_counter += 1

        # Save the output to the appropriate folder
        if "python" in task_description or "code" in task_description:
            save_to_file(folders["python"], python_filename, python_code)  # Save as Python file
        else:
            save_to_file(folders["mail"], text_filename, output)  # Save as text file

        # Save the output to JSON
        json_data = {
            "task": task_description,
            "solution": python_code,
            "timestamp": timestamp
        }
        save_to_file(folders["json"], json_filename, json.dumps(json_data, indent=4))

        return f"\nJervis (Solution):\n{python_code}"

    elif "exit" in user_input or "stop" in user_input:
        return "Jervis: Goodbye!"

    else:
        return "Jervis: I didn't understand. Can you repeat?"

# Main loop to run Jervis
if __name__ == "__main__":
    print("Jervis AI Assistant is ready. Type 'exit' or 'stop' to quit.")
    while True:
        user_input = input("You: ").strip()
        response = jervis_assistant(user_input)
        print(response)
        if "Goodbye" in response:
            break