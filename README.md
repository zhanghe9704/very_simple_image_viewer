# A Very Simple Image Viewer

Developed together with ChatGPT-4



*Codes are provided as is. No guarantee for anything. It is my first program with a GUI and has been tested only on my own PC.* 

## Features

1.  Open and show an image ("*.jpg *.jpeg *.png *.bmp *.gif") in a window. 
2. Use PageUp/PageDown key or the scroller on mouse to browse the images inside a folder. 
3. Resize the image as you change the size of the window while maintaining the ratio. 
4. Double click the left key on mouse will open a windows in the current folder to choose an image to show. 
5. Double click the right key on mouse will show the current image in its original size. 

## How to use

- Can be compiled into an executable file using pyinstaller. I used the following command to compile it to an executable file in Windows 11. 

  ```shell
  pyinstaller --onefile --windowed image_viewer.py
  ```

- Or you can run it with Python in command line:

  ```shell
  python image_viewer.py
  ```

## Known issues

- Sometimes, when the window is maximized, clicking the "resize" icon on the top right corner does not resize the window to the previous size. Sometimes it works as it should. 
- Can not open an image by double clicking the image even when you have already tell Windows to open images with this program. (This is probably an easy fix. I'll work on it when I feel like.)



