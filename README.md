# ReciteQuran
This code is a Python program that allows users to recite Quranic verses and check their pronunciation using speech recognition. The program prompts the user to enter the surah (chapter) and the range of verses to recite, and then uses the recite_quran function to recite the specified verses.

The recite_quran function first reads the verses from an online Quran website using the read_verses_from_quran function. It then iterates over the verses and uses the Google Text-to-Speech API to convert each verse to speech and play it. The function then prompts the user to recite the verse and uses the PocketSphinx speech recognition library to record and recognize the user's voice. If the recognized text matches the original verse, the verse is displayed in green. If there is a discrepancy, the mistake is recorded in a dictionary and the verse is displayed in red.

The read_verses_from_quran function uses the Beautiful Soup library to scrape the specified verses from an online Quran website. It returns a list of the verses.

The main function prompts the user to enter the surah and the range of verses to recite, and then calls the recite_quran function to recite the verses. It then prints any mistakes made by the user and prompts the user to continue or exit the program.

The verses_per_surah list stores the number of verses in each surah. The program uses this list to validate the verse numbers entered by the user.
