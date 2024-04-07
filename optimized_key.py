from collections import Counter


def calculate_optimized_key_quick(ciphered_text, key_length, most_frequent_letter_language):
    optimized_key = ''
    for i in range(key_length):
        # Extracts the segment of the text corresponding to the same position in the key
        segment = ciphered_text[i::key_length]

        # Counts the frequency of letters in the segment
        counter = Counter(segment)

        # Finds the most frequent letter in the segment
        most_frequent_letter = max(counter, key=counter.get)

        # Calculates the shift from the most frequent letter to the most frequent letter in the language
        shift = ord(most_frequent_letter) - ord(most_frequent_letter_language)

        # Corrects the shift to be within the range of 0-25 and adds it to the key
        optimized_key += chr((shift + 26) % 26 + ord('a'))

    return optimized_key


def calculate_optimized_key(ciphered_text, key_length, language_frequency):
    optimized_key = ''

    for i in range(key_length):
        segment = ciphered_text[i::key_length]
        counter = Counter(segment)

        best_deviation = float('inf')
        best_letter = ''

        # Compares each possible letter with the frequency of letters in the segment
        for key_letter in language_frequency:
            total_deviation = 0

            # Calculates the deviation between observed and expected frequency
            for letter, freq in counter.items():
                shifted_letter = chr((ord(letter) - ord(key_letter)) % 26 + ord('a'))
                total_deviation += abs(language_frequency.get(shifted_letter, 0) - freq)

            # Selects the letter that minimizes the total deviation
            if total_deviation < best_deviation:
                best_deviation = total_deviation
                best_letter = key_letter

        optimized_key += best_letter

    return optimized_key


# Example of optimized functions usage
ciphered_text = "example ciphered text for testing"
key_length = 3
most_frequent_letter_language = 'e'
language_frequency = {'e': 0.12702, 't': 0.09056, 'a': 0.08167}  # example frequencies

# Calling the optimized functions
quick_key = calculate_optimized_key_quick(ciphered_text, key_length, most_frequent_letter_language)
slow_key = calculate_optimized_key(ciphered_text, key_length, language_frequency)

var = quick_key, slow_key
