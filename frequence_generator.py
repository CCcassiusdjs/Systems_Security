import itertools


def frequency_generator(frequencies, n_top_letters):
    # Sort the letters by frequency and get the top N most frequent
    most_frequent_letters = sorted(frequencies, key=frequencies.get, reverse=True)[:n_top_letters]

    # Generate all possible permutations of these letters
    permutations = itertools.permutations(most_frequent_letters)

    # Iterate over each permutation to create a new frequency dictionary
    for permutation in permutations:
        new_frequency = frequencies.copy()  # Copies the original frequency dictionary

        # Assign the frequencies of the permuted letters
        for i, letter in enumerate(most_frequent_letters):
            new_frequency[letter] = frequencies[permutation[i]]

        yield new_frequency  # Returns the new frequency dictionary
