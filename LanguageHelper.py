from collections import Counter
from typing import Dict, List


class LanguageHelper:
    """
    Helper class for letter frequency analysis and language determination
    for encrypted texts.
    """
    EXPECTED_IC: Dict[str, float] = {
        'english': 0.0667,
        'portuguese': 0.0745
    }

    ALPHABET_FREQUENCIES: Dict[str, Dict[str, float]] = {
        'english': dict(a=8.167, b=1.492, c=2.782, d=4.253, e=12.702, f=2.228, g=2.015, h=6.094, i=6.966, j=0.153,
                        k=0.772, l=4.025, m=2.406, n=6.749, o=7.507, p=1.929, q=0.095, r=5.987, s=6.327, t=9.056,
                        u=2.758, v=0.978, w=2.360, x=0.150, y=1.974, z=0.074),
        'portuguese': dict(a=14.63, b=1.04, c=3.88, d=4.99, e=12.57, f=1.02, g=1.30, h=1.28, i=6.18, j=0.40, k=0.02,
                           l=2.78, m=4.74, n=5.05, o=10.73, p=2.52, q=1.20, r=6.53, s=7.81, t=4.34, u=4.63, v=1.67,
                           w=0.01, x=0.21, y=0.01, z=0.47)
    }

    def __init__(self, text: str):
        """
        Initializes the LanguageHelper with the encrypted text.

        Args:
            text (str): The encrypted text to be analyzed.
        """
        self.text: str = text

    @staticmethod
    def calculate_frequency(text: str) -> Dict[str, float]:
        """
        Calculates the letter frequency in the given text.

        Args:
            text (str): The text for which to calculate letter frequency.

        Returns:
            Dict[str, float]: A dictionary with the frequency of each letter in the text.
        """
        text = text.replace(" ", "").upper()
        frequency = Counter(text)
        total_letters = sum(frequency.values())

        return {letter: (count / total_letters) * 100 for letter, count in frequency.items() if letter.isalpha()}

    @staticmethod
    def calculate_modified_chi_square(observed: Dict[str, float], expected: Dict[str, float]) -> float:
        """
        Calculates the modified chi-square statistic between observed and expected frequencies.

        Args:
            observed (Dict[str, float]): Observed letter frequencies in the text.
            expected (Dict[str, float]): Expected letter frequencies for a language.

        Returns:
            float: The value of the modified chi-square statistic.
        """
        return sum(
            ((observed.get(letter, 0) - expected.get(letter, 0)) ** 3) / expected.get(letter, 1)
            for letter in observed
        )

    def determine_language(self) -> str:
        """
        Determines the probable language of the text based on letter frequencies.

        Returns:
            str: The most probable language of the text ('english' or 'portuguese').
        """
        observed_frequency = self.calculate_frequency(self.text)
        chi_squares = {
            lang: self.calculate_modified_chi_square(observed_frequency, freq)
            for lang, freq in self.ALPHABET_FREQUENCIES.items()
        }
        return min(chi_squares, key=chi_squares.get)

    @classmethod
    def find_key_length_ic(cls, ciphered_text: str, expected_ic: float) -> int:
        """
        Finds the most likely key length using the Index of Coincidence (IC) method.

        Args:
            ciphered_text (str): Encrypted text to analyze.
            expected_ic (float): Expected Index of Coincidence for the language.

        Returns:
            int: The most probable key length.
        """
        max_key_length = 20
        best_length = 1
        smallest_difference = float('inf')

        for length in range(1, max_key_length + 1):
            segments = cls.generate_segments(ciphered_text, length)
            average_ic = sum(cls.index_of_coincidence(segment) for segment in segments) / length
            difference = abs(expected_ic - average_ic)

            if difference * 1.015 < smallest_difference:  # Tolerance factor for comparison
                smallest_difference = difference
                best_length = length

        return best_length

    @staticmethod
    def generate_segments(text: str, length: int) -> List[str]:
        """
        Generates text segments for the given length.

        Args:
            text (str): The encrypted text.
            length (int): The length of the segments.

        Returns:
            List[str]: A list of text segments.
        """
        return [''.join(text[i::length]) for i in range(length)]

    @staticmethod
    def index_of_coincidence(segment: str) -> float:
        """
        Calculates the Index of Coincidence (IC) for a text segment.

        Args:
            segment (str): The text segment for which to calculate the IC.

        Returns:
            float: The value of the Index of Coincidence.
        """
        n = len(segment)
        if n <= 1:  # Avoid division by zero if the segment is too short
            return 0.0

        freqs = Counter(segment)
        ic = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))
        return round(ic, 3)
