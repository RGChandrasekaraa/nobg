# Extended Background Remover Application using Tkinter and OpenCV
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import logging
from threading import Thread
import io
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        root.title("NoBg - Background Remover App")
        self.setup_ui(root)
        self.processed_image = None
        self.original_image = None

    def setup_ui(self, root):
        # Create main frames
        self.create_control_frame(root)
        self.create_image_frame(root)
        self.create_status_frame(root)

    def create_control_frame(self, root):
        control_frame = tk.Frame(root, width=200)
        control_frame.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(control_frame, text="Control Panel", font=("Arial", 14)).pack(pady=10)
        self.upload_button = ttk.Button(control_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=5)

        self.clear_button = ttk.Button(control_frame, text="Clear", command=self.clear_images)
        self.clear_button.pack(pady=5)

        self.save_button = ttk.Button(control_frame, text="Save Image", command=self.save_image, state="disabled")
        self.save_button.pack(pady=5)

    def create_image_frame(self, root):
        image_frame = tk.Frame(root)
        image_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        ttk.Label(image_frame, text="Image Display", font=("Arial", 14)).pack(pady=10)
        self.original_image_label = ttk.Label(image_frame)
        self.original_image_label.pack(pady=10)

        self.processed_image_label = ttk.Label(image_frame)
        self.processed_image_label.pack(pady=10)

    def create_status_frame(self, root):
        status_frame = tk.Frame(root, relief=tk.SUNKEN, bd=1)
        status_frame.pack(side="bottom", fill="x")
        self.status_label = ttk.Label(status_frame, text="Welcome to Background Remover App", relief=tk.SUNKEN, anchor="w")
        self.status_label.pack(side="left")

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            logging.info(f"Image uploaded: {file_path}")
            self.display_original_image(file_path)
            self.status_label.config(text="Processing...")
            thread = Thread(target=lambda: self.process_and_display_image(file_path), daemon=True)
            thread.start()

    def display_original_image(self, file_path):
        try:
            self.original_image = Image.open(file_path)
            self.original_image.thumbnail((350, 350))
            photo = ImageTk.PhotoImage(self.original_image)
            self.original_image_label.config(image=photo)
            self.original_image_label.image = photo
            logging.info("Original image displayed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {e}")
            logging.error(f"Failed to open image: {e}")

    def process_and_display_image(self, file_path):
        try:
            image = cv2.imread(file_path)
            image = cv2.resize(image, (350, 350))

            mask = self.remove_background_with_opencv(image)
            processed_image = self.apply_mask(image, mask)

            processed_image_pil = Image.fromarray(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))
            photo = ImageTk.PhotoImage(processed_image_pil)
            self.processed_image_label.config(image=photo)
            self.processed_image_label.image = photo
            self.processed_image = processed_image_pil

            self.status_label.config(text="Done!")
            self.save_button['state'] = 'normal'
            logging.info("Image processed and displayed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {e}")
            logging.error(f"Failed to process image: {e}")

    def remove_background_with_opencv(self, image):
        # Placeholder for deep learning model processing
        mask = np.zeros(image.shape[:2], dtype="uint8")  # Example mask
        return mask

    def apply_mask(self, image, mask):
        background = np.zeros_like(image)
        foreground = np.where(mask[..., None], image, background)
        return foreground

    def save_image(self):
        if self.processed_image:
            file_type_options = [("JPEG files", "*.jpg"), ("PNG files", "*.png")]
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=file_type_options)
            if file_path:
                try:
                    self.processed_image.save(file_path)
                    messagebox.showinfo("Image Saved", f"Image successfully saved to {file_path}")
                    logging.info(f"Image saved: {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save image: {e}")
                    logging.error(f"Failed to save image: {e}")
            else:
                logging.info("Save image operation cancelled.")
        else:
            messagebox.showwarning("No Image", "No processed image to save.")
            logging.warning("No processed image to save.")

    def clear_images(self):
        self.original_image_label.config(image='')
        self.processed_image_label.config(image='')
        self.status_label.config(text="Ready")
        self.save_button['state'] = 'disabled'
        self.processed_image = None
        self.original_image = None
        logging.info("Images and status cleared")

def main():
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
