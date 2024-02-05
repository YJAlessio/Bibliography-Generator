import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
from datetime import date
import pyperclip

class MLACreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MLA Format Creator")

        self.create_widgets()

    def create_widgets(self):
        # Entry for user to enter website URL
        ttk.Label(self.root, text="Website URL:").pack(pady=10, side=tk.LEFT)
        self.url_entry = ttk.Entry(self.root, width=40)
        self.url_entry.pack(pady=10, side=tk.LEFT)

        # Button to generate MLA format
        ttk.Button(self.root, text="Generate MLA Format", command=self.generate_mla_format).pack(pady=10, side=tk.LEFT)

        # Button to paste text from clipboard
        ttk.Button(self.root, text="Paste from Clipboard", command=self.paste_from_clipboard).pack(pady=10, side=tk.RIGHT)

    def generate_mla_format(self):
        url = self.url_entry.get()

        if not url:
            tk.messagebox.showwarning("Warning", "Please enter a website URL.")
            return

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extracting metadata
            title = soup.title.string.strip() if soup.title else ""
            author_tag = soup.find('meta', {'name': 'author'}) or soup.find('meta', {'property': 'og:author'})
            author = author_tag['content'].strip() if author_tag else ""
            publication_date_tag = soup.find('meta', {'name': 'date'}) or soup.find('meta', {'property': 'og:publish_date'})
            publication_date = publication_date_tag['content'].strip() if publication_date_tag else ""

            # Creating MLA format with the accessed date at the end
            mla_format = f"{author}. \"{title}.” {publication_date}, {url}. Accessed {date.today().strftime('%B %d, %Y')}."

            # Copying MLA format to clipboard
            pyperclip.copy(mla_format)

            # Displaying the generated MLA format and copy confirmation
            messagebox.showinfo("MLA Format", f"{mla_format}\n\nCitation copied to clipboard.")

            # Saving to log.txt
            with open("log.txt", "a") as file:
                file.write(mla_format + "\n")
                file.write("-" * 50 + "\n")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error: {str(e)}")

    def paste_from_clipboard(self):
        clipboard_text = pyperclip.paste()
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, clipboard_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = MLACreatorApp(root)
    root.mainloop()
