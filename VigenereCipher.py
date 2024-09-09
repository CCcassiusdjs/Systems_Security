from collections import Counter
from typing import Dict


class VigenereCipher:
    """
    Class for decryption using the Vigenère cipher.
    """

    def __init__(self, key: str):
        """
        Initializes the VigenereCipher instance with a specific key.

        Args:
            key (str): The key for decryption.
        """
        self.key: str = key
        self.validate_key()

    def validate_key(self) -> None:
        """
        Validates that the key is set and not empty.

        Raises:
            ValueError: If the key is not set or is empty.
        """
        if not self.key:
            raise ValueError("Decryption key is not set or is empty.")
        print(f"[DEBUG] Validated key: {self.key}")

    def decrypt(self, ciphered_text: str) -> str:
        """
        Decrypts the provided text using the Vigenère cipher with the current key.

        Args:
            ciphered_text (str): The ciphered text to be decrypted.

        Returns:
            str: The decrypted text.
        """
        self.validate_key()  # Ensures the key is valid before decryption

        decrypted_text = []
        key_length = len(self.key)
        print(f"[DEBUG] Starting decryption with key of length {key_length}")

        for i, char in enumerate(ciphered_text):
            if char.isalpha():  # Only decrypts letters
                key_char = self.key[i % key_length].lower()  # Uses the current key character
                shift = ord(key_char) - ord('a')  # Calculates the shift based on the key character

                if char.islower():
                    decrypted_char = chr((ord(char) - shift - ord('a')) % 26 + ord('a'))
                else:
                    decrypted_char = chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
                decrypted_text.append(decrypted_char)
            else:
                # Keeps non-alphabetic characters unchanged
                decrypted_text.append(char)

        print(f"[DEBUG] Finished decryption. Total decrypted characters: {len(decrypted_text)}")
        return ''.join(decrypted_text)

    @staticmethod
    def extract_segments(ciphered_text: str, key_length: int) -> Dict[int, str]:
        """
        Extracts segments of the text based on the key length.

        Args:
            ciphered_text (str): The ciphered text to be segmented.
            key_length (int): The length of the key.

        Returns:
            Dict[int, str]: A dictionary with text segments based on the key length.
        """
        return {i: ciphered_text[i::key_length] for i in range(key_length)}

    @staticmethod
    def get_most_frequent_char(counter: Counter) -> str:
        """
        Returns the most frequent character from the counter.

        Args:
            counter (Counter): A counter of character frequencies.

        Returns:
            str: The most frequent character.
        """
        return max(counter, key=counter.get)

    @staticmethod
    def calculate_shift(char1: str, char2: str) -> int:
        """
        Calculates the shift required to align char1 with char2.

        Args:
            char1 (str): The first character.
            char2 (str): The second character.

        Returns:
            int: The value of the required shift.
        """
        return (ord(char1) - ord(char2) + 26) % 26

    @classmethod
    def calculate_optimized_key_quick(cls, ciphered_text: str, key_length: int, most_frequent_letter: str) -> str:
        """
        Quickly calculates an optimized key for the Vigenère cipher.

        Args:
            ciphered_text (str): The ciphered text.
            key_length (int): The length of the key.
            most_frequent_letter (str): The most frequent letter to align.

        Returns:
            str: The calculated optimized key.

        Raises:
            ValueError: If the key length is less than or equal to zero.
        """
        if key_length <= 0:
            raise ValueError("Key length must be greater than zero.")

        optimized_key = ''
        segments = cls.extract_segments(ciphered_text, key_length)

        for segment in segments.values():
            counter = Counter(segment)
            most_frequent_char = cls.get_most_frequent_char(counter)
            shift = cls.calculate_shift(most_frequent_char, most_frequent_letter)
            optimized_key += chr(shift + ord('a'))

        return optimized_key

    @classmethod
    def calculate_optimized_key(cls, ciphered_text: str, key_length: int, language_frequency: Dict[str, float]) -> str:
        """
        Calculates an optimized key for the Vigenère cipher using letter frequencies.

        Args:
            ciphered_text (str): The ciphered text.
            key_length (int): The length of the key.
            language_frequency (Dict[str, float]): Expected letter frequencies for the language.

        Returns:
            str: The calculated optimized key.

        Raises:
            ValueError: If the key length is less than or equal to zero.
        """
        if key_length <= 0:
            raise ValueError("Key length must be greater than zero.")

        optimized_key = ''
        segments = cls.extract_segments(ciphered_text, key_length)

        for segment in segments.values():
            counter = Counter(segment)
            best_deviation = float('inf')
            best_letter = ''

            # If the segment length is zero, continue to the next one
            if len(segment) == 0:
                continue

            # Try all letters from 'a' to 'z' to find the best matching shift
            for key_letter in range(26):
                shifted_frequency = {}
                total_deviation = 0

                # Calculate the shifted frequencies for each letter in the segment
                for letter, count in counter.items():
                    shifted_letter = chr((ord(letter) - key_letter - ord('a')) % 26 + ord('a'))
                    shifted_frequency[shifted_letter] = shifted_frequency.get(shifted_letter, 0) + count

                # Compare the observed frequencies with the expected frequencies for the language
                for letter, freq in language_frequency.items():
                    observed = shifted_frequency.get(letter, 0) / len(segment) * 100
                    total_deviation += abs(freq - observed)

                # Select the letter with the smallest deviation
                if total_deviation < best_deviation:
                    best_deviation = total_deviation
                    best_letter = chr(key_letter + ord('a'))

            optimized_key += best_letter

        return optimized_key
