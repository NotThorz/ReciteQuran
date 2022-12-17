import pocketsphinx
import requests
import os
from bs4 import BeautifulSoup
from gtts import gTTS

# A dictionary to store the mistakes made by the user
mistakes = {}
# Number of verses in each Surah .
verses_per_surah = [7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52, 99, 128, 111, 110, 98, 135, 112, 78, 118, 64, 77, 227, 93, 88, 69, 60, 34, 30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53, 89, 59, 37, 35, 38, 29, 18, 45,
                    60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11, 11, 18, 12, 12, 30, 52, 52, 44, 28, 28, 20, 56, 40, 31, 50, 40, 46, 42, 29, 19, 36, 25, 22, 17, 19, 26, 30, 20, 15, 21, 11, 8, 8, 19, 5, 8, 8, 11, 11, 8, 3, 9, 5, 4, 7, 3, 6, 3, 5, 4, 5, 6]


def recite_quran(surah, start_verse, end_verse):
    # Read the verses from the Quran
    verses = read_verses_from_quran(surah, start_verse, end_verse)

    # Recite each verse
    for verse_num, verse in enumerate(verses, start=start_verse):
        print(f"Reciting verse {verse_num}: {verse}")

        # Convert the verse to speech and play it
        tts = gTTS(verse, lang='ar')
        tts.save("verse.mp3")
        os.system("mpg321 verse.mp3")
        os.remove("verse.mp3")

        # Prompt the user to recite the verse
        print("Start reciting now... Say 'stop' when you are done.")

        # Set up the speech recognition module
        recognizer = pocketsphinx.Decoder()
        recognizer.set_kws("stop", 1e-30)
        microphone = pocketsphinx.AudioFile()
        microphone.open("/dev/stdin")

        # Start recording the user's voice
        # Wait for the user to say "stop" before moving on to the next verse
        while True:
            phrase = microphone.get_audio()
            audio = recognizer.decode(phrase)
            if recognizer.hyp() == "stop":
                break

        # Stop recording and recognize the spoken text
        try:
            # Set the search mode to keyword spotting mode
            recognizer.set_search("stop")
            # Start the search
            recognizer.start_utt()
            # Feed the audio to the search
            recognizer.process_raw(audio, False, False)
            # End the search
            recognizer.end_utt()
            # Get the hypothesis
            recited_verse = recognizer.hyp().hypstr
            print("You recited:")
            print(recited_verse)

            # Check if the recited verse is correct
            if verse == recited_verse:
                # Display the verse in green
                print(f"\033[92m{recited_verse}\033[0m")
            else:
                # Record the mistake and display the verse in red
                mistakes[verse_num] = (verse, recited_verse)
                print(f"\033[91m{recited_verse}\033[0m")
        except pocketsphinx.UnknownValueError:
            print("Sorry, I could not understand what you said")
        finally:
            # Close the microphone to release resources
            microphone.close()


def read_verses_from_quran(surah, start_verse, end_verse):
    """
    Reads the specified verses from an online Quran website.

    Parameters:
    surah (int): The surah number.
    start_verse (int): The starting verse number.
    end_verse (int): The ending verse number.

    Returns:
    list: A list of the verses.
    """

    # Validate the surah number
    if not (1 <= surah <= 114):
        raise ValueError(
            "Invalid surah number. Surah numbers must be between 1 and 114.")

    # Validate the verse numbers
    num_verses = verses_per_surah[surah - 1]
    if not (1 <= start_verse <= num_verses) or not (1 <= end_verse <= num_verses):
        raise ValueError(
            f"Invalid verse number. Verse numbers must be between 1 and {num_verses} for surah {surah}.")

    # Use Beautiful Soup to scrape the verses from an online Quran website
    url = f"https://quran.com/{surah}:{start_verse}-{end_verse}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    verse_elements = soup.find_all(class_="quran")
    verses = [element.text for element in verse_elements]
    return verses


def main():
    while True:
        # Prompt the user to enter the surah and the range of verses to recite
        surah = int(input("Enter the surah: "))
        start_verse = int(input("Enter the starting verse: "))
        end_verse = int(input("Enter the ending verse: "))
        # Recite the verses
        recite_quran(surah, start_verse, end_verse)

        # Print the mistakes made by the user
        if mistakes:
            print("Mistakes made:")
            for verse_num, (correct_verse, incorrect_verse) in mistakes.items():
                print(
                    f"Verse {verse_num}: {incorrect_verse} (correct verse: {correct_verse})")
        else:
            print("No mistakes made!")

        # Prompt the user to reset the program or re-recite the same verses
        choice = input(
            "Enter 'r' to reset the program or 'c' to continue reciting the same verses: ")
        if choice == 'r':
            # Reset the mistakes dictionary
            mistakes = {}
        elif choice == 'c':
            # Clear the mistakes dictionary for the current set of verses
            mistakes.clear()
        else:
            print("Invalid choice. Exiting program.")
            break


if __name__ == "__main__":
    main()
