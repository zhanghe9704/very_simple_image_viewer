import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class PictureViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Picture Viewer")

        # Setting up the frame for navigation buttons
        frame = tk.Frame(self.root)
        frame.pack(side=tk.BOTTOM, pady=5)

        # Buttons for control
        btn_open = tk.Button(frame, text="Open", command=self.open_image)
        btn_open.pack(side=tk.LEFT, padx=10)

        # The label that holds the image
        self.img_label = tk.Label(self.root)
        self.img_label.pack()

        # To keep track of the image list and the current index
        self.images = []
        self.current_image_index = 0

        # Binding key and mouse events
        self.root.bind("<MouseWheel>", self.scroll_image)
        self.root.bind("<Next>", self.scroll_image)  # Page Down
        self.root.bind("<Prior>", self.scroll_image)  # Page Up

    def open_image(self):
        """Open an image file for viewing and load all images in the folder."""
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if path:
            directory = os.path.dirname(path)
            self.images = [os.path.join(directory, f) for f in os.listdir(directory)
                           if os.path.isfile(os.path.join(directory, f)) and f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
            files = [f for f in os.listdir(directory)
                           if os.path.isfile(os.path.join(directory, f)) and f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
            # self.current_image_index = self.images.index(path)
            self.current_image_index = files.index(os.path.basename(path))
            self.display_image()

    def display_image(self):
        """Display the current image from images list."""
        if self.images:
            image_path = self.images[self.current_image_index]
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            self.img_label.config(image=photo)
            self.img_label.image = photo  # keep a reference!

    def scroll_image(self, event):
        """Handle scroll or page up/down key event to navigate images."""
        if not self.images:
            return

        if event.delta > 0 or event.keysym == 'Prior':
            self.current_image_index = (self.current_image_index - 1) % len(self.images)
        else:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
        
        self.display_image()

if __name__ == "__main__":
    root = tk.Tk()
    viewer = PictureViewer(root)
    root.mainloop()
