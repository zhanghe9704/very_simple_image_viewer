import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class PictureViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Picture Viewer")
        self.last_width = self.root.winfo_width()
        self.last_height = self.root.winfo_height()
        
        # # Label to display the file name
        # self.file_name_label = tk.Label(self.root, text="", font=("Helvetica", 16))
        # self.file_name_label.pack(side=tk.TOP, pady=5)

        # Setting up the frame for navigation buttons
        frame = tk.Frame(self.root)
        frame.pack(side=tk.BOTTOM, pady=5)

        # Buttons for control
        self.btn_open = tk.Button(frame, text="Open", command=self.open_image)
        self.btn_open.pack(side=tk.LEFT, padx=10)

        # The label that holds the image
        self.img_label = tk.Label(self.root)
        self.img_label.pack()

        # To keep track of the image list and the current index
        self.images = []
        self.current_image_index = 0
        self.image= None
        
        # Bind the configure event to dynamically resize the image
        self.root.bind("<Configure>", self.resize_image)
        self.current_photo_image = None  # To hold the PhotoImage object

        # Binding key and mouse events
        self.root.bind("<MouseWheel>", self.scroll_image)
        self.root.bind("<Next>", self.scroll_image)  # Page Down
        self.root.bind("<Prior>", self.scroll_image)  # Page Up
        self.img_label.bind("<Double-1>", self.open_image)
        self.root.bind("<Double-Button-3>", self.show_original_size)
        
        self.resized = False

    def open_image(self, event=None):
        """Open an image file for viewing and load all images in the folder."""
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if path:
            directory = os.path.dirname(path)
            self.images = [os.path.join(directory, f) for f in os.listdir(directory)
                           if os.path.isfile(os.path.join(directory, f)) and f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
            files = [f for f in os.listdir(directory)
                           if os.path.isfile(os.path.join(directory, f)) and f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
            self.current_image_index = files.index(os.path.basename(path))
            self.display_image()
            

    def display_image(self):
        """Display the current image from images list."""
        if self.images:
            image_path = self.images[self.current_image_index]
            image = Image.open(image_path)
 
            self.image = image
            # self.original_width, self.original_height = self.image.size

            if self.resized:
                self.resize_image()
                self.btn_open.pack_forget()
                return
                       
            photo = ImageTk.PhotoImage(image)
            self.img_label.config(image=photo)
            self.img_label.image = photo  # keep a reference!
            self.current_photo_image =  photo

            
            # Hide the open button
            self.btn_open.pack_forget()
            
            # # Update the file name label
            # file_name = os.path.basename(image_path)
            # self.file_name_label.config(text=file_name)
            
            
    def resize_image(self, event=None):
        """Resize the image to fit the current canvas size, maintaining aspect ratio."""
        if not self.image:
            return
        
        self.root.update_idletasks()
        
        original_width, original_height = self.image.size
        # Get dimensions directly from the root window
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        
        # if root_width != self.last_width or root_height != self.last_height:     
        label_width = root_width - 4
        label_height = root_height - 36 -4
        if label_height < 0:
            label_height = 0
            
        # Calculate the appropriate size maintaining aspect ratio
        ratio = min(label_width / original_width, label_height / original_height)
        new_width = round(original_width * ratio)
        new_height = round(original_height * ratio)
        d_w = round(0.01*original_width)
        d_h = round(0.01*original_height)
        
        # if new_width == original_width and new_height == original_height:
        if abs(new_width-original_width)<d_w and abs(new_height-original_height)<d_h:
            self.resized = False
        else:
            self.resized = True
            
        if not self.resized:
            image = self.image
            photo = ImageTk.PhotoImage(image)
            self.img_label.config(image=photo)
            self.img_label.image = photo  # keep a reference!
            self.current_photo_image =  photo
            return

        # Resize the image using Pillow
        resized_image = self.image.resize((new_width, new_height), Image.LANCZOS)

        # Convert the PIL image to PhotoImage and display it
        self.current_photo_image = ImageTk.PhotoImage(resized_image)
        self.img_label.config(image=self.current_photo_image)
        
            
            
    def scroll_image(self, event):
        """Handle scroll or page up/down key event to navigate images."""
        if not self.images:
            return
    
        # Determine the scroll direction
        if event.delta > 0 or event.keysym == 'Prior':  # Scroll up or Page Up
            if self.current_image_index > 0:
                self.current_image_index -= 1
                self.display_image()
        else:  # Scroll down or Page Down
            if self.current_image_index < len(self.images) - 1:
                self.current_image_index += 1
                self.display_image()
                
    def show_original_size(self, event):
        """Display the current image in its original size."""
        if hasattr(self, "image"):
            image_width, image_height = self.image.size
            frame_width = image_width + 4
            frame_height = image_height + 36 + 4
            self.root.geometry(f"{frame_width}x{frame_height}")

                
if __name__ == "__main__":
    root = tk.Tk()
    viewer = PictureViewer(root)
    root.mainloop()
