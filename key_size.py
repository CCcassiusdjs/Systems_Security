from collections import Counter


def index_of_coincidence(segment):
    n = len(segment)  # Number of characters in the segment
    freqs = Counter(segment)  # Counts the frequency of each letter

    # Calculates the IoC based on the frequency of each letter
    ic = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))
    return ic.__round__(3)


def find_key_length_ic(ciphered_text, EXPECTED_IC):
    max_key_length = 20  # Limit for the key length

    best_length = 1
    smallest_difference = float('inf')

    # Tests each possible key length up to the limit
    for length in range(1, max_key_length + 1):
        # Divides the ciphered text into segments based on the key length
        segments = [''.join(ciphered_text[i::length]) for i in range(length)]

        # Calculates the average IoC for all segments
        average_ic = sum(index_of_coincidence(segment) for segment in segments) / length

        # Calculates the difference between the average IoC and the expected IoC
        difference = abs(EXPECTED_IC - average_ic)

        # Adds a 1.5% improvement threshold to choose a new best length
        if difference * 1.015 < smallest_difference:
            smallest_difference = difference
            best_length = length

    return best_length
