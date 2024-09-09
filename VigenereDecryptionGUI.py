import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
from typing import Callable, Optional
from Decryptor import Decryptor
from VigenereCipher import VigenereCipher


class DecryptionApp:
    def __init__(self, root: tk.Tk) -> None:
        """
        Initializes the Vigenere Cipher Decryption application.

        Args:
            root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Vigenere Cipher Decryption Tool")
        self.root.geometry("600x400")
        self.root.configure(bg="#282C34")

        # Welcome screen setup
        self.welcome_screen = tk.Frame(self.root, bg="#282C34")
        self.welcome_screen.pack(fill=tk.BOTH, expand=True)

        self.welcome_label = tk.Label(
            self.welcome_screen,
            text="Welcome to the Vigenere Cipher Decryption Tool",
            bg="#282C34",
            fg="white",
            font=("Helvetica", 14, "bold"),
        )
        self.welcome_label.pack(pady=20)

        self.start_button = tk.Button(
            self.welcome_screen,
            text="Start",
            command=self.show_file_selection_screen,
            bg="#61AFEF",
            fg="white",
            font=("Helvetica", 12, "bold"),
            bd=0,
            width=10,
        )
        self.start_button.pack(pady=20)

        self.add_hover_effect(self.start_button)

        # File selection screen setup (initially hidden)
        self.file_selection_frame = tk.Frame(self.root, bg="#282C34")

        self.select_file_btn = tk.Button(
            self.file_selection_frame,
            text="📂 Select File",
            command=self.select_file,
            bg="#61AFEF",
            fg="white",
            font=("Helvetica", 12, "bold"),
            bd=0,
        )
        self.select_file_btn.pack(pady=5)

        self.add_hover_effect(self.select_file_btn)  # Adds hover effect to the button

        # Initialize necessary variables and attributes
        self.file_path: Optional[str] = None
        self.current_key: Optional[str] = None
        self.decryptor: Optional[Decryptor] = None
        self.encrypted_text_area: Optional[ScrolledText] = None
        self.decrypted_text_area: Optional[ScrolledText] = None
        self.decrypt_thread: Optional[threading.Thread] = None
        self.decryption_screen: Optional[tk.Toplevel] = None
        self.is_decrypting = threading.Event()  # Controls the decryption state
        self.change_key_frame: Optional[tk.Frame] = None

    def add_hover_effect(self, button: tk.Button) -> None:
        """Adds hover effect to the button."""
        button.bind("<Enter>", lambda e: self.animate_button_hover(button, enter=True))
        button.bind("<Leave>", lambda e: self.animate_button_hover(button, enter=False))

    def animate_button_hover(self, button: tk.Button, enter: bool = True) -> None:
        """Animates the button on mouse hover."""
        bg_color = "#98C379" if enter else "#61AFEF"
        fg_color = "black" if enter else "white"
        button.configure(bg=bg_color, fg=fg_color)

    def show_file_selection_screen(self) -> None:
        """Displays the file selection screen."""
        self.welcome_screen.pack_forget()  # Hides the welcome screen
        self.file_selection_frame.pack(padx=10, pady=10)  # Displays the file selection screen

    def select_file(self) -> None:
        """Allows the user to select a file to decrypt."""
        if self.is_decrypting.is_set():  # Checks if decryption is in progress
            messagebox.showinfo("Info", "Please wait for the current decryption to complete.")
            return

        # Displays save popup before opening the file explorer
        if self.decrypted_text_area and self.decrypted_text_area.get(1.0, tk.END).strip():
            self.prompt_save_before_action(self._select_file)
        else:
            self._select_file()

    def _select_file(self) -> None:
        """Auxiliary function to open the file explorer."""
        self.file_path = filedialog.askopenfilename(
            initialdir=".",
            title="Select File",
            filetypes=(("Text files", "*.txt"), ("all files", "*.*")),
        )
        if self.file_path:
            # Initialize the decryptor before any use
            self.decryptor = Decryptor(self.file_path, gui_callback=self.update_gui_callback)

            # Displays the popup to confirm the action
            self.confirm_decryption_start()

    def confirm_decryption_start(self) -> None:
        """Displays a popup to confirm if the user wants to start decryption."""
        response = messagebox.askyesnocancel(
            "Start Decryption", "The text has been loaded. Do you want to start the decryption now?"
        )
        if response is True:
            # User chose "Yes", starts decryption
            self.show_decryption_screen()
            self.start_decryption_thread()
        elif response is False:
            # User chose "No", asks if they want to choose another file or exit
            self.ask_for_next_action()
        else:
            # User chose "Cancel", exits the program
            self.exit_program()

    def ask_for_next_action(self) -> None:
        """Asks the user if they want to choose another file or exit the program."""
        response = messagebox.askyesno("Choose Another File", "Do you want to choose another file?")
        if response:
            # User chose to select another file
            self.select_file()
        else:
            # User chose to exit
            self.exit_program()

    def start_decryption_thread(self) -> None:
        """Starts the decryption thread ensuring that only one is active."""
        if self.is_decrypting.is_set():  # Checks if decryption is in progress
            messagebox.showinfo("Info", "A decryption is already in progress. Please wait.")
            return

        self.is_decrypting.set()  # Signals that decryption is in progress

        # Ensures that the previous thread (if exists) is properly terminated
        if self.decrypt_thread and self.decrypt_thread.is_alive():
            self.decrypt_thread.join()  # Waits for the previous thread to finish

        self.decrypt_thread = threading.Thread(target=self.decrypt_text_thread, daemon=True)
        self.decrypt_thread.start()

    def decrypt_text_thread(self) -> None:
        """Thread function to decrypt the text."""
        try:
            self.update_gui_callback("🔒 Decryption in progress...")
            self.decryptor.decrypt_text()
            # Updates the interface after decryption
            self.update_gui_callback("🔓 Decryption complete.")
            self.display_file_content()
        finally:
            self.is_decrypting.clear()  # Signals that decryption has been completed or interrupted

    def show_decryption_screen(self) -> None:
        """Displays the screen with the file content and manipulation options."""
        # Closes the file selection screen
        self.file_selection_frame.pack_forget()

        # Closes the previous decryption screen if it exists
        if self.decryption_screen and self.decryption_screen.winfo_exists():
            self.decryption_screen.destroy()

        # New result display screen setup
        self.decryption_screen = tk.Toplevel(self.root, bg="#282C34")
        self.decryption_screen.title("Decryption Results")

        # Frame to organize the text areas side by side
        text_frames = tk.Frame(self.decryption_screen, bg="#282C34")
        text_frames.pack(pady=10)

        # Frame for the ciphered text
        encrypted_frame = tk.Frame(text_frames, bg="#282C34")
        encrypted_frame.pack(side=tk.LEFT, padx=5)

        # Label for the ciphered text
        tk.Label(encrypted_frame, text="📝 Ciphered Text", bg="#282C34", fg="white", font=("Helvetica", 12)).pack()
        self.encrypted_text_area = ScrolledText(
            encrypted_frame, wrap=tk.WORD, width=40, height=20, bg="#1E2127", fg="white"
        )
        self.encrypted_text_area.pack()

        # Frame for the decrypted text
        decrypted_frame = tk.Frame(text_frames, bg="#282C34")
        decrypted_frame.pack(side=tk.LEFT, padx=5)

        # Label for the decrypted text
        tk.Label(decrypted_frame, text="📝 Decrypted Text", bg="#282C34", fg="white", font=("Helvetica", 12)).pack()
        self.decrypted_text_area = ScrolledText(
            decrypted_frame, wrap=tk.WORD, width=40, height=20, bg="#1E2127", fg="white"
        )
        self.decrypted_text_area.pack()

        # Displaying information about the key and calculation results
        self.key_label = tk.Label(self.decryption_screen, text="🔑 Key Size: --", bg="#282C34", fg="white")
        self.key_label.pack()

        self.decryption_key_label = tk.Label(self.decryption_screen, text="🔑 Decryption Key: --", bg="#282C34", fg="white")
        self.decryption_key_label.pack()

        self.result_label = tk.Label(self.decryption_screen, text="🛠️ Results: --", bg="#282C34", fg="white")
        self.result_label.pack()

        # Action buttons
        self.change_key_btn = tk.Button(
            self.decryption_screen,
            text="🔄 Change Key",
            command=self.toggle_change_key,
            bg="#61AFEF",
            fg="white",
            font=("Helvetica", 10),
            bd=0,
        )
        self.change_key_btn.pack(pady=5)
        self.add_hover_effect(self.change_key_btn)  # Adds hover effect

        self.select_new_file_btn = tk.Button(
            self.decryption_screen,
            text="📁 Select Another File",
            command=self.select_new_file,
            bg="#61AFEF",
            fg="white",
            font=("Helvetica", 10),
            bd=0,
        )
        self.select_new_file_btn.pack(pady=5)
        self.add_hover_effect(self.select_new_file_btn)  # Adds hover effect

        self.exit_btn = tk.Button(
            self.decryption_screen,
            text="❌ Exit",
            command=self.exit_program,
            bg="#61AFEF",
            fg="white",
            font=("Helvetica", 10),
            bd=0,
        )
        self.exit_btn.pack(pady=5)
        self.add_hover_effect(self.exit_btn)  # Adds hover effect

        # Ensures the file content is displayed after initializing the screen
        self.display_file_content()

    def toggle_change_key(self) -> None:
        """Expands or collapses the key change panel."""
        if self.change_key_frame:
            # If the panel is already present, remove it
            self.change_key_frame.destroy()
            self.change_key_frame = None
        else:
            # Otherwise, create and display the key change panel
            self.change_key_frame = tk.Frame(self.decryption_screen, bg="#282C34")
            self.change_key_frame.pack(pady=5)

            tk.Label(self.change_key_frame, text="🔑 Enter new key:", bg="#282C34", fg="white").pack(pady=5)
            key_entry = tk.Entry(self.change_key_frame, bg="#1E2127", fg="white")
            key_entry.pack(pady=5)

            def apply_new_key() -> None:
                new_key = key_entry.get()
                if new_key:
                    self.current_key = new_key
                    self.decryptor.decryption_key = new_key
                    threading.Thread(
                        target=self.decryptor.handle_decryption_process, args=(new_key,), daemon=True
                    ).start()
                    self.display_file_content()
                    self.toggle_change_key()  # Collapse the panel after applying the new key

            apply_btn = tk.Button(
                self.change_key_frame,
                text="✅ Apply",
                command=apply_new_key,
                bg="#61AFEF",
                fg="white",
                bd=0,
            )
            apply_btn.pack(pady=10)

    def display_file_content(self) -> None:
        """Displays the content of the selected file and calculation results."""
        if self.file_path and self.decryptor:  # Checks if the file and decryptor are initialized
            with open(self.file_path, 'r') as file:
                file_content = file.read(10000)  # Reads only the first 10,000 characters

            # Clears and updates the encrypted text area
            self.encrypted_text_area.delete(1.0, tk.END)
            self.encrypted_text_area.insert(tk.END, file_content)

            # If the decryption key is known, decrypts the text
            if self.decryptor.decryption_key:
                key_length = len(self.decryptor.decryption_key)
                decrypted_text = VigenereCipher(self.decryptor.decryption_key).decrypt(file_content[:10000])
            else:
                key_length = '--'
                decrypted_text = "DECIPHERING..."

            # Clears and updates the decrypted text area
            self.decrypted_text_area.delete(1.0, tk.END)
            self.decrypted_text_area.insert(tk.END, decrypted_text)

            # Updates the key information and calculation results
            decryption_key = self.decryptor.decryption_key if self.decryptor.decryption_key else '--'
            self.key_label.config(text=f"🔑 Key Size: {key_length}")
            self.decryption_key_label.config(text=f"🔑 Decryption Key: {decryption_key}")
            self.result_label.config(text="🔓 Results: Decryption complete.", fg='green')

    def select_new_file(self) -> None:
        """Allows the user to select a new file to decrypt."""
        if self.is_decrypting.is_set():
            messagebox.showinfo("Info", "Please wait for the current decryption to complete.")
            return

        # Displays save popup before opening the file explorer
        if self.decrypted_text_area and self.decrypted_text_area.get(1.0, tk.END).strip():
            self.prompt_save_before_action(self._select_file)
        else:
            self._select_file()

    def prompt_save_before_action(self, callback: Callable[[], None]) -> None:
        """Displays a popup asking if the user wants to save the file before performing another action."""
        if messagebox.askyesno("Save File", "Do you want to save the current decryption?"):
            output_dir = "output"
            # Ensures the output directory exists
            os.makedirs(output_dir, exist_ok=True)

            if self.decryptor and self.decryptor.decryption_key:
                # Creates a path for the output file
                output_path = os.path.join(output_dir, "decrypted_output.txt")

                # Gets the current decrypted text
                decrypted_text = self.decrypted_text_area.get(1.0, tk.END)

                # Saves the decrypted text to the output file
                with open(output_path, 'w') as file:
                    file.write(decrypted_text)

                messagebox.showinfo("Success", f"File saved to {output_path}")

        callback()

    def exit_program(self) -> None:
        """Saves the data if necessary and exits the program."""
        self.prompt_save_before_action(self.root.quit)

    def update_gui_callback(self, message: str) -> None:
        """Callback function to update the GUI from the decryptor."""
        # Use a flag to ensure repetitive updates are limited
        if "complete" in message.lower():
            self.root.after(0, self._update_gui_safe, message)
        elif "progress" in message.lower():
            pass
        else:
            self.root.after(0, self._update_gui_safe, message)

    def _update_gui_safe(self, message: str) -> None:
        """Updates the GUI safely from the main thread."""
        if "Decryption:" in message:
            decrypted_text = message.split("Decryption: ")[-1]
            self.decrypted_text_area.delete(1.0, tk.END)
            self.decrypted_text_area.insert(tk.END, decrypted_text)
            self.key_label.config(text=f"🔑 Key Size: {len(self.decryptor.decryption_key)}")
            self.decryption_key_label.config(text=f"🔑 Decryption Key: {self.decryptor.decryption_key}")
        else:
            if "complete" in message.lower():
                self.result_label.config(text="🔓 Results: Decryption complete.", fg='green')
            else:
                self.result_label.config(text=message, fg='red')
        self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = DecryptionApp(root)
    root.mainloop()
