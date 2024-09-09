import itertools
import os
from multiprocessing import Pool, cpu_count
from typing import Dict, Optional, Callable
import logging

from LanguageHelper import LanguageHelper
from VigenereCipher import VigenereCipher

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Decryptor:
    def __init__(self, file_path: str, gui_callback: Optional[Callable] = None):
        """
        Initializes the Decryptor with the file path and an optional GUI callback.

        Args:
            file_path (str): Path to the encrypted file.
            gui_callback (Callable, optional): Callback function for GUI updates.
        """
        self.file_path: str = file_path
        self.gui_callback: Optional[Callable] = gui_callback
        self.ciphered_text: str = self.read_ciphered_text()
        self.languages: list = ['portuguese', 'english']
        self.language_helper: Optional[LanguageHelper] = None
        self.decryption_key: Optional[str] = None  # Stores the decryption key
        self.stop_decryption: bool = False  # Flag to control stopping the decryption process

    def read_ciphered_text(self) -> str:
        """
        Reads the encrypted text from a file.

        Returns:
            str: The file content in lowercase.
        """
        try:
            with open(self.file_path, 'r') as file:
                content = file.read().lower()
                logging.debug(f"Read {len(content)} characters from the file.")
                return content
        except FileNotFoundError:
            logging.error("File not found. Please check the path.")
            return ""

    def decrypt_text(self) -> None:
        """
        Main function to decrypt the encrypted text.
        """
        logging.debug("Determining probable language...")
        self.language_helper = LanguageHelper(self.ciphered_text)
        probable_language = self.language_helper.determine_language()
        logging.debug(f"Probable language determined: {probable_language}")

        if probable_language not in self.languages:
            logging.warning(f"Language '{probable_language}' not recognized, using default list.")

        if probable_language != self.languages[0]:
            self.languages.reverse()

        for language in self.languages:
            if self.stop_decryption:
                logging.info("Decryption process stopped by the user.")
                break

            logging.debug(f"Trying language: {language}")
            expected_ic = LanguageHelper.EXPECTED_IC[language]
            alphabet_frequency = LanguageHelper.ALPHABET_FREQUENCIES[language]
            key_length = LanguageHelper.find_key_length_ic(self.ciphered_text, expected_ic)
            logging.debug(f"Found key length: {key_length}")

            if not self.decrypt_text_language_discovered(language, alphabet_frequency, key_length):
                logging.info("Decryption process stopped by the user.")
                break

    def decrypt_text_language_discovered(self, language: str, alphabet_frequency: Dict[str, float], key_length: int) -> bool:
        """
        Performs the decryption process once the language is discovered.

        Args:
            language (str): The detected language.
            alphabet_frequency (Dict[str, float]): Letter frequency in the language.
            key_length (int): Estimated key length.

        Returns:
            bool: True if decryption continues, False if interrupted.
        """
        logging.debug(f"Starting decryption for language: {language} with key length: {key_length}")

        quick_key = VigenereCipher.calculate_optimized_key_quick(self.ciphered_text, key_length, 'e')
        logging.debug(f"Quick key calculated: {quick_key}")
        self.decryption_key = quick_key

        if not self.handle_decryption_process(quick_key):
            logging.info("Decryption stopped after quick key attempt.")
            return False

        if self.gui_callback:
            logging.info("Starting slow method processing...")

        max_attempts = 50

        # Multiprocessing for decryption attempts
        frequencies = [(alphabet_frequency, key_length) for _ in range(max_attempts)]
        with Pool(processes=cpu_count()) as pool:
            results = pool.starmap(attempt_decryption, frequencies)

        # Process results
        for result in results:
            if self.stop_decryption:
                logging.info("Decryption stopped due to user intervention.")
                break
            if result:
                self.decryption_key = result
                self.handle_decryption_process(result)

        return True

    def handle_decryption_process(self, key: str) -> bool:
        """
        Handles the decryption process, including user interaction for key letter replacement.

        Args:
            key (str): Key used for decryption.

        Returns:
            bool: True if decryption is successful, False otherwise.
        """
        logging.debug(f"Decrypting with key: {key}")
        cipher = VigenereCipher(key=key)
        decrypted_text = cipher.decrypt(self.ciphered_text)

        if self.gui_callback:
            logging.debug(f"Current key: {key}")
            logging.debug(f"Decrypted text (first 40 characters): {decrypted_text[:40]}")

        logging.info("Decryption successfully handled.")
        return True

    def replace_letter_in_key(self, key: str, pos: int, new_letter: str) -> str:
        """
        Replaces a letter in the decryption key.

        Args:
            key (str): The original key.
            pos (int): The position of the letter to be replaced.
            new_letter (str): The new letter to replace.

        Returns:
            str: The new key with the letter replaced.
        """
        key_list = list(key)
        key_list[pos] = new_letter.lower()
        return ''.join(key_list)

    @staticmethod
    def frequency_generator(frequencies: Dict[str, float], n_top_letters: int):
        """
        Generates all possible permutations of the top N most frequent letters.

        Args:
            frequencies (Dict[str, float]): Letter frequencies.
            n_top_letters (int): Number of most frequent letters to consider.

        Yields:
            Dict[str, float]: New frequency distribution after permutation.
        """
        most_frequent_letters = sorted(frequencies, key=frequencies.get, reverse=True)[:n_top_letters]
        permutations = itertools.permutations(most_frequent_letters)

        for permutation in permutations:
            new_frequency = frequencies.copy()
            for i, letter in enumerate(most_frequent_letters):
                new_frequency[letter] = frequencies[permutation[i]]
            yield new_frequency


def attempt_decryption(alphabet_frequency: Dict[str, float], key_length: int) -> str:
    """
    Attempts decryption with a given frequency combination.

    Args:
        alphabet_frequency (Dict[str, float]): Letter frequencies of the alphabet.
        key_length (int): Key length.

    Returns:
        str: Calculated optimized key.
    """
    logging.debug("Trying frequency combination.")
    slow_key = VigenereCipher.calculate_optimized_key("", key_length, alphabet_frequency)
    logging.debug(f"Slow key calculated: {slow_key}")
    return slow_key
