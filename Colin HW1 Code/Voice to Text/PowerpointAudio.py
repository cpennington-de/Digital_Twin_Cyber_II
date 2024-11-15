#simple speach to text. Not very good but works regardless of network location.


import speech_recognition as sr

def record_and_transcribe():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Recording... Speak now.")
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        text = recognizer.recognize_sphinx(audio)
        print(f"Recognized Text: {text}")

        with open("transcription.txt", "w") as file:
            file.write(text)
        print("Text has been saved to 'transcription.txt'.")

    except sr.UnknownValueError:
        print("Sphinx could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Sphinx; {e}")

if __name__ == "__main__":
    record_and_transcribe()
