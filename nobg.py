import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from rembg import remove
from threading import Thread
import io

class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Remover")
        self.root.geometry("1000x600")

        # Left frame for controls
        control_frame = tk.Frame(root, width=200)
        control_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.upload_button = tk.Button(control_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=5)

        self.clear_button = tk.Button(control_frame, text="Clear", command=self.clear_images)
        self.clear_button.pack(pady=5)

        self.status_label = tk.Label(control_frame, text="")
        self.status_label.pack(pady=5)

        self.save_button = tk.Button(control_frame, text="Save Processed Image", command=self.save_image, state="disabled")
        self.save_button.pack(pady=5)

        # Right frame for images
        image_frame = tk.Frame(root)
        image_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        self.original_image_label = tk.Label(image_frame)
        self.original_image_label.pack(pady=10)

        self.processed_image_label = tk.Label(image_frame)
        self.processed_image_label.pack(pady=10)

        self.processed_image = None

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.display_original_image(file_path)
            self.status_label.config(text="Processing...")
            thread = Thread(target=self.process_and_display_image, args=(file_path,))
            thread.start()

    def display_original_image(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((350, 350))
        photo = ImageTk.PhotoImage(image)
        self.original_image_label.config(image=photo)
        self.original_image_label.image = photo

    def process_and_display_image(self, file_path):
        with open(file_path, 'rb') as file:
            input_data = file.read()

        output_data = remove(input_data)
        self.processed_image = Image.open(io.BytesIO(output_data))
        self.processed_image.thumbnail((350, 350))

        photo = ImageTk.PhotoImage(self.processed_image)
        self.processed_image_label.config(image=photo)
        self.processed_image_label.image = photo

        self.status_label.config(text="Done!")
        self.save_button['state'] = 'normal'

    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.processed_image.save(file_path)
                messagebox.showinfo("Image Saved", f"Image successfully saved to {file_path}")
        else:
            messagebox.showwarning("No Image", "No processed image to save.")

    def clear_images(self):
        self.original_image_label.config(image='')
        self.processed_image_label.config(image='')
        self.status_label.config(text="")
        self.save_button['state'] = 'disabled'
        self.processed_image = None

def main():
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
