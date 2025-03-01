import speech_recognition as sr
import subprocess
def get_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        return ""
def generate_response(prompt):
    """Generates a response using the Ollama model."""
    try:
        result = subprocess.run(["ollama", "run", "deepseek-r1:1.5b", prompt], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error generating response: {e}")
    try:
        subprocess.run([f'echo "{result}" | ./piper --model ryan.onnx --output-raw | aplay -r 22050 -f S16_LE -t raw -'], shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error speaking text: {e}")

def speak(text):
    """Converts text to speech and speaks it out using Piper."""
    subprocess.run([f'echo "{text}" | ./piper --model ryan.onnx --output-raw | aplay -r 22050 -f S16_LE -t raw -'], shell=True, check=True)

def main():
    while True:
        user_input = get_input()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        response = (generate_response(user_input)).strip()
        response= response.replace("\n", " ").replace("<think>", " ").replace("</think>", " ").replace("*", " ").replace("#", " ")
        print("Assistant:", response)
        speak(response)

if __name__ == "__main__":
    main()
