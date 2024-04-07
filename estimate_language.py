def calculate_frequency(text):
    # Removes spaces and converts to uppercase
    text = text.replace(" ", "").upper()
    frequency = {}

    # Counts the frequency of each letter
    for letter in text:
        if letter.isalpha():  # Checks if it's a letter
            frequency[letter] = frequency.get(letter, 0) + 1

    # Calculates the total number of letters to normalize the frequency
    total_letters = sum(frequency.values())

    # Normalizes the frequency to a percentage
    for letter in frequency:
        frequency[letter] = (frequency[letter] / total_letters) * 100

    return frequency


def calculate_modified_chi_square(observed, expected):
    chi_square = 0
    for letter in observed:
        if letter in expected:
            # Calculates the chi-square using the third power
            chi_square += ((observed.get(letter, 0) - expected.get(letter, 0)) ** 3) / expected.get(letter, 1)

    return chi_square


def determine_language(ciphered_text, expected_english_frequency, expected_portuguese_frequency):
    # Calculates the letter frequency in the ciphered text
    observed_frequency = calculate_frequency(ciphered_text)

    # Calculates the modified chi-square for English and Portuguese
    chi_square_english = calculate_modified_chi_square(observed_frequency, expected_english_frequency)
    chi_square_portuguese = calculate_modified_chi_square(observed_frequency, expected_portuguese_frequency)

    # Determines the language based on the lower chi-square value
    return "portuguese" if chi_square_portuguese < chi_square_english else "english"
