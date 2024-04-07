from pycipher import Vigenere
import estimate_language as di
import language_helpers as lh
import frequence_generator as gf
import optimized_key as cco
import key_size as etc
import read_ciphered_text as ltc

numberOfCombinations = 10


# Function to decrypt text using the Vigenère cipher.
def decrypt_with_vigenere(ciphered_text, key):
    # Initialize the Vigenere cipher with the key
    vigenere = Vigenere(key)
    # Return the decrypted text
    return vigenere.decipher(ciphered_text)


# Function to get user input for various choices.
def userChoice():
    # Provide options for the user
    options = ''' 
    1 - I found the ciphered message, end the program
    2 - I want to change language
    3 - end the program
    '''
    # Return the user's choice
    return input(options)


# Function to determine possible languages of the ciphered text.
def determineLanguageList(text):
    # Estimate the probable language of the text
    probableLanguage = di.determine_language(text, lh.english_frequency_top10, lh.portuguese_frequency_top10)
    # Define a list of languages to test
    languages = ['portuguese', 'english']
    # If the estimated language is not the first in the list, reverse the list
    if languages[0] != probableLanguage:
        languages.reverse()
    return languages


# Function to allow the user to replace a letter in the decryption key.
def replaceLetterInKey(key):
    print("Enter the position of the letter you want to replace and the new letter (separated by space):")
    # Get user input for position and new letter
    pos, new_letter = input().split()
    pos = int(pos)
    # Convert key to list to modify it
    key = list(key)
    # Replace the letter in the specified position
    key[pos] = new_letter
    # Return the modified key as a string
    return ''.join(key)


# Function to perform the decryption of the ciphered text.
def decryptTextLanguageDiscovered(ciphered_text, language, alphabetFrequency, key_length, user_interaction=True):
    print("Ciphered Text (first 40 characters):", ciphered_text[:40])

    # Perform quick decryption method first.
    key = cco.calculate_optimized_key_quick(ciphered_text, key_length, 'e')

    # Loop for user interaction if required.
    while True:
        decrypted_text = decrypt_with_vigenere(ciphered_text, key)
        print("\nCurrent Key:", key)
        print("Decrypted Text (first 40 characters):", decrypted_text[:40])

        # Check if user wants to change a letter in the key
        if user_interaction:
            choice = input("Do you want to replace a letter in the key? (y/n): ")
            if choice.lower() == 'y':
                key = replaceLetterInKey(key)
            else:
                break
        else:
            break

    # If quick method is insufficient, employ a slower, more thorough method.
    print("\nStarting Slow Method:")
    # Iterate over combinations of letter frequencies
    for combined_frequency in gf.frequency_generator(alphabetFrequency, numberOfCombinations):
        # Recalculate key with new frequency combination
        key = cco.calculate_optimized_key(ciphered_text, key_length, combined_frequency)
        while True:
            decrypted_text = decrypt_with_vigenere(ciphered_text, key)
            print("\nCurrent Key:", key)
            print("Key Length:", len(key))
            print("Decrypted Text (first 40 characters):", decrypted_text[:40])

            # Allow user to adjust key during slow method
            if user_interaction:
                choice = input("Do you want to replace a letter in the key? (y/n): ")
                if choice.lower() == 'y':
                    key = replaceLetterInKey(key)
                else:
                    break
            else:
                return True

        # Option to switch language or end the program
        if user_interaction:
            choice = userChoice()
            if choice in ['1', '3']:
                return False
            elif choice == '2':
                return True

    return True


# Main function to decrypt ciphered texts.
def decrypt_text(file_path, user_interaction=True):
    # Read ciphered text from the file
    ciphered_text = ltc.read_ciphered_text(file_path).lower()
    # Determine possible languages of the text
    languages = determineLanguageList(ciphered_text)

    # Try decryption for each language
    for language in languages:
        # Get the expected index of coincidence for the language
        EXPECTED_IC = lh.get_EXPECTED_IC(language)
        # Get the frequency distribution for the alphabet of the language
        alphabetFrequency = lh.alphabetsFrequencies[language]
        # Find the likely length of the key
        key_length = etc.find_key_length_ic(ciphered_text, EXPECTED_IC)

        # Perform decryption and check if language needs to be changed
        needToChangeLanguage = decryptTextLanguageDiscovered(ciphered_text, language, alphabetFrequency, key_length,
                                                             user_interaction)
        if needToChangeLanguage and user_interaction:
            languages.reverse()
            break

    return
