#QR Code Generator by Tom Knudsen 2024
#This is a simple tkinter program to generate a qr code


import tkinter as tk
from tkinter import messagebox
import qrcode

#Class to initialize the application and creating widgets. 
class QRCodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("350x200")

        self.create_widgets()

    def create_widgets(self):
        # Text input field
        self.text_entry = tk.Text(self.root, height=10, width=30)
        self.text_entry.grid(row=0, column=0, padx=10, pady=10, rowspan=4)

        # Buttons
        clear_button = tk.Button(self.root, text="Clear Field", command=self.clear_field)
        clear_button.grid(row=0, column=1, padx=10, pady=10)

        generate_button = tk.Button(self.root, text="Generate", command=self.generate_qr_code)
        generate_button.grid(row=1, column=1, padx=10, pady=10)

        exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy)
        exit_button.grid(row=2, column=1, padx=10, pady=10)
#Function to clear the label fields. 
    def clear_field(self):
        self.text_entry.delete("1.0", tk.END)
#Function to generate qr code
    def generate_qr_code(self):
        data = self.text_entry.get("1.0", tk.END).strip()

        if data:
            try:
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")

                img.save("qrcode.png")
                messagebox.showinfo("Success", "QR Code generated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Warning", "Please enter data before generating a QR Code.")

#Run the window
if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()


