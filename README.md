# Vigenere Cipher Decryption Tool

## Overview

The Vigenere Cipher Decryption Tool is a Python-based application that allows users to decrypt text encrypted using the Vigenere cipher. The tool leverages a graphical user interface (GUI) built with Tkinter to make it user-friendly. The decryption process is enhanced with various algorithms to determine the probable key length and optimize the decryption key based on the letter frequencies in different languages.

## Detailed Explanation of Code

### 1. **`DecryptionApp` Class**

The `DecryptionApp` class represents the main GUI application. It handles user interactions, file selection, and controls the decryption process.

- **Initialization (`__init__` method):**  
  Sets up the initial configuration of the application, including the window size, title, and background color. Initializes different screens, such as the welcome screen, file selection screen, and decryption screen.

- **GUI Components:**
  - **`self.welcome_screen`**: A frame displayed at the start, containing a welcome message and a "Start" button to initiate the decryption process.
  - **`self.file_selection_frame`**: A hidden frame initially, used for selecting the encrypted file.
  - **`self.select_file_btn`**: A button to open a file dialog for selecting a file to decrypt.

- **Method Descriptions:**
  - **`add_hover_effect` & `animate_button_hover`**: Adds visual feedback (color change) when hovering over buttons.
  - **`show_file_selection_screen`**: Hides the welcome screen and displays the file selection screen.
  - **`select_file`**: Opens a file dialog to allow the user to select a file. If decryption is in progress, it shows a warning.
  - **`confirm_decryption_start`**: Asks the user whether to start decryption immediately after a file is loaded.
  - **`ask_for_next_action`**: Prompts the user to choose between selecting another file or exiting the program.
  - **`start_decryption_thread`**: Initializes and starts a new thread for the decryption process to keep the GUI responsive.
  - **`decrypt_text_thread`**: Handles the decryption process in a separate thread to avoid blocking the main thread.
  - **`show_decryption_screen`**: Displays the main decryption screen with options to change the key, choose another file, or exit.
  - **`toggle_change_key`**: Shows or hides the panel that allows the user to change the decryption key manually.
  - **`display_file_content`**: Updates the GUI with the content of the decrypted file and key information.
  - **`select_new_file`**: Allows the user to select a new file for decryption.
  - **`prompt_save_before_action`**: Asks the user if they want to save the decrypted content before performing another action.
  - **`exit_program`**: Saves the current decryption and exits the application.
  - **`update_gui_callback` & `_update_gui_safe`**: Updates the GUI with messages or status changes from the decryption process.

### 2. **`Decryptor` Class**

The `Decryptor` class is responsible for the core logic of decrypting a Vigenere cipher. It determines the probable language of the text, calculates the key length, and optimizes the key for decryption.

- **Initialization (`__init__` method):**  
  Loads the encrypted text from the selected file, initializes language data, and prepares for decryption.

- **Main Methods:**
  - **`decrypt_text`**: The main method that determines the probable language of the text and attempts to decrypt it using different strategies.
  - **`decrypt_text_language_discovered`**: Continues the decryption process once the probable language and key length are determined.
  - **`handle_decryption_process`**: Manages the decryption process, updates the GUI, and allows user interaction for changing the key.
  - **`replace_letter_in_key`**: Allows manual replacement of letters in the decryption key.
  - **`frequency_generator`**: Generates all possible permutations of the top N most frequent letters for frequency analysis.

### 3. **`VigenereCipher` Class**

The `VigenereCipher` class handles the core decryption algorithm of the Vigenere cipher. It provides methods for decrypting text using a given key, optimizing the key based on letter frequency, and calculating shifts for different letters.

- **Initialization (`__init__` method):**  
  Validates the provided key and initializes the cipher.

- **Core Methods:**
  - **`decrypt`**: Decrypts the given text using the Vigenere cipher with the current key.
  - **`extract_segments`**: Extracts segments of the text based on the key length.
  - **`calculate_optimized_key_quick`**: Quickly calculates an optimized key for the cipher using the most frequent letters.
  - **`calculate_optimized_key`**: Calculates a more precise key using letter frequencies and chi-square analysis.

### 4. **`LanguageHelper` Class**

The `LanguageHelper` class provides helper methods for analyzing letter frequencies and determining the language of the text. It calculates the frequency of letters, the modified chi-square statistic, and the Index of Coincidence (IC) for language analysis.

## How to Execute

### Prerequisites

- Python 3.7 or higher
- Required libraries:
  - `tkinter` (comes pre-installed with Python)
  - `threading`
  - `itertools`
  - `multiprocessing`
  - `collections`

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-repo/vigenere-decryption-tool.git
   cd vigenere-decryption-tool
   ```

2. **Run the Application:**

   Execute the following command in your terminal or command prompt:

   ```bash
   python main.py
   ```

### Usage

1. **Launch the Tool:**  
   After running the application, you will see a welcome screen.

2. **Start the Decryption Process:**  
   Click the "Start" button to begin.

3. **Select an Encrypted File:**  
   Choose the file you want to decrypt using the "Select File" button.

4. **Confirm Decryption:**  
   Confirm that you want to start the decryption process.

5. **Change Key (Optional):**  
   If needed, change the decryption key using the "Change Key" button.

6. **Save Results:**  
   Save the decrypted file when prompted.

7. **Exit the Tool:**  
   Click "Exit" to close the application.
