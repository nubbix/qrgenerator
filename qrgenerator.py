#This is a simple QR Code Generator made by Tom Knudsen 2024
#Version 1.0.2

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import qrcode
import tkinter.simpledialog
import tkinter.messagebox
import pyperclip

#This will initialisize the app, set root geometry and define functions. 
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

        # Image widget to display QR code
        self.qr_image_label = tk.Label(self.root, text="QR Code will be displayed here.")
        self.qr_image_label.grid(row=0, column=2, padx=10, pady=10, rowspan=5)

        # Status label
        self.status_label = tk.Label(self.root, text="Status: Ready")
        self.status_label.grid(row=5, column=0, columnspan=3, pady=10)

        # Original Image
        self.qr_image = None
#This will clear all fields in the window, including the image. 
    def clear_field(self):
        self.text_entry.delete("1.0", tk.END)
        self.qr_image_label.config(image=None, text="QR Code will be displayed here.")
        self.qr_image_label.image = None  # Set image to None to clear it
        self.qr_image = None
        self.update_status("Status: Cleared")



#This will generate the actual qr code
    def generate_qr_code(self):
        data = self.text_entry.get("1.0", tk.END).strip()

        if data:
            try:
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")

                # Resize the QR code image for display
                img_display = img.resize(self.qr_preview_size)

                # Save the original Image
                self.qr_image = img

                # Convert to PhotoImage for display
                img_tk = ImageTk.PhotoImage(img_display)
                self.qr_image_label.config(image=img_tk, text="")
                self.qr_image_label.image = img_tk

                self.update_status("Status: QR Code generated successfully!")

                # Create a new Image object for saving with the specified size (640x480)
                resized_img = Image.new("RGB", (640, 480), "white")
                resized_img.paste(img, ((640 - img.width) // 2, (480 - img.height) // 2))
                # resized_img.save("output.png")  # You can change the filename and path as needed

            except Exception as e:
                self.update_status(f"Status: An error occurred - {e}")
        else:
            self.update_status("Status: Please enter data before generating a QR Code.")

#saves the image to disk as png
    def save_qr_code(self):
        if self.qr_image:
            try:
                file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
                if file_path:
                    self.qr_image.save(file_path)
                    self.update_status("Status: QR Code saved successfully!")
            except Exception as e:
                self.update_status(f"Status: Error saving QR Code - {e}")
        else:
            self.update_status("Status: Generate a QR Code first before trying to save.")

    def paste_text(self):
        try:
            text_to_paste = self.root.clipboard_get()
            self.text_entry.insert(tk.END, text_to_paste)
            self.update_status("Status: Pasted text successfully.")
        except tk.TclError:
            self.update_status("Status: Clipboard is empty or does not contain text.")

    def update_status(self, message):
        self.status_label.config(text=message)

#initialize the loop
if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()
