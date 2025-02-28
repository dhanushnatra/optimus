
import subprocess
def get_text_input():
    """Gets text input from the user."""
    return input("You: ")

def generate_response(prompt):
    """Generates a response using the Ollama model."""
    result = subprocess.run(["ollama", "run", "deepseek-r1:1.5b", prompt], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return result.stdout

def speak(text):
    """Converts text to speech and speaks it out using Piper."""
    subprocess.run([f'echo "{text}" | ./piper --model ryan.onnx --output-raw | aplay -r 22050 -f S16_LE -t raw -'], shell=True, check=True)

def main():
    while True:
        user_input = get_text_input()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        response = (generate_response(user_input)).strip()
        response= response.replace("\n", " ").replace("<think>", " ").replace("</think>", " ").replace("<|im_start|>", " ")
        print("Assistant:", response)
        speak(response)

if __name__ == "__main__":
    main()
