#This is a very simple QR Code Genertor for making QR Codes
#By Tom Knudsen - 2024

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import qrcode
import tkinter.simpledialog
import tkinter.messagebox
import pyperclip

#Class app for QR Code Generator
class QRCodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("580x280")

        # Define the size for the QR code preview
        self.qr_preview_size = (150, 150)

        self.create_widgets()

    def create_widgets(self):
        # Text input field
        self.text_entry = tk.Text(self.root, height=10, width=30)
        self.text_entry.grid(row=0, column=0, padx=10, pady=10, rowspan=5)

        # Buttons
        clear_button = tk.Button(self.root, text="Clear Field", command=self.clear_field)
        clear_button.grid(row=0, column=1, padx=10, pady=10)

        generate_button = tk.Button(self.root, text="Generate", command=self.generate_qr_code)
        generate_button.grid(row=1, column=1, padx=10, pady=10)

        save_button = tk.Button(self.root, text="Save", command=self.save_qr_code)
        save_button.grid(row=2, column=1, padx=10, pady=10)

        paste_button = tk.Button(self.root, text="Paste", command=self.paste_text)
        paste_button.grid(row=3, column=1, padx=10, pady=10)

        exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy)
        exit_button.grid(row=4, column=1, padx=10, pady=10)

        # This will output an image to the window on the right side based on the text you input
        self.qr_image_label = tk.Label(self.root, text="QR Code will be displayed here.")
        self.qr_image_label.grid(row=0, column=2, padx=10, pady=10, rowspan=5)

        # Outputs the Status label to the window
        self.status_label = tk.Label(self.root, text="Status: Ready")
        self.status_label.grid(row=5, column=0, columnspan=3, pady=10)

#This will begin to generate the qr code
    def generate_qr_code(self):
        data = self.text_entry.get("1.0", tk.END).strip()

        if data:
            try:
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")

                # Resize the QR code image
                img = img.resize(self.qr_preview_size)

                # Display QR code on the right side
                img = ImageTk.PhotoImage(img)
                self.qr_image_label.config(image=img, text="")
                self.qr_image_label.image = img
                self.qr_image = img
                self.update_status("Status: QR Code generated successfully!")
            except Exception as e:
                self.update_status(f"Status: An error occurred - {e}")
        else:
            self.update_status("Status: Please enter data before generating a QR Code.")
#Function to save the qr code to disk in PNG format
    def save_qr_code(self):
        if hasattr(self, 'qr_image'):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.qr_image_label.image.write(file_path)
                self.update_status("Status: QR Code saved successfully!")
        else:
            self.update_status("Status: Generate a QR Code first before trying to save.")
#This function will again clear all fields. 
    def clear_field(self):
        self.text_entry.delete("1.0", tk.END)
        self.qr_image_label.config(image=None, text="QR Code will be displayed here.")
        if hasattr(self, 'qr_image'):
            self.qr_image_label.image = None
            self.qr_image_label.config(image=None)
            delattr(self, 'qr_image')
        self.update_status("Status: Cleared")
#This function will allow you to paste inn text into the input field. 
    def paste_text(self):
        try:
            text_to_paste = self.root.clipboard_get()
            self.text_entry.insert(tk.END, text_to_paste)
            self.update_status("Status: Pasted text successfully.")
        except tk.TclError:
            self.update_status("Status: Clipboard is empty or does not contain text.")

    def update_status(self, message):
        self.status_label.config(text=message)
#Initialization of the tkinter window
if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()
