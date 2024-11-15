#Much better speech to text program due to google audio
#Does not seem to work on University network. Seems like they are blocking it

import pyaudio
import speech_recognition as sr
import threading

# Initialize recognizer
recognizer = sr.Recognizer()
transcript = ""  # Variable to hold the ongoing transcript

# This function will handle the audio capture and transcription
def listen_and_transcribe():
    global transcript
    with sr.Microphone() as source:
        print("Listening... Press Ctrl+C to stop.")
        while True:
            try:
                # Listen for audio
                audio = recognizer.listen(source)
                # Recognize the speech in the audio
                text = recognizer.recognize_google(audio)
                
                # Update the transcript
                transcript += " " + text
                print(f"Transcribed: {transcript.strip()}")
                
            except sr.UnknownValueError:
                # If the speech was not understood
                continue  # Skip to the next loop iteration
            except sr.RequestError as e:
                # If there was an error with the recognizer service
                print(f"Could not request results from Google Speech Recognition service; {e}")

# Run the transcription in a separate thread
def main():
    transcription_thread = threading.Thread(target=listen_and_transcribe)
    transcription_thread.start()

    try:
        # Wait for user input to stop the program
        input("Press Enter to stop the transcription...\n")
    except KeyboardInterrupt:
        print("\nStopping transcription...")
        print("Final Transcript:")
        print(transcript.strip())  # Print the entire transcript when stopping

if __name__ == "__main__":
    main()
