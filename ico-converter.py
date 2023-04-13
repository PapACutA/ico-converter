"""ico-converter is a simple tool to generate ico files from images. 
A given Image will be put into a square format and centered within 
this format without distorting it. Than it will be resized to 
resolutions needed for an icon. The conversion itself is done by 
the Python Image Library (PIL).

Author: PapACutA
Created on April 12 2023
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk

class icoConverterApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # if bundled with pyinstaller, find new path to iconfile
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        # path to icon file
        iconfile = os.path.abspath(os.path.join(bundle_dir, 'converter.ico'))

        self.iconbitmap(iconfile)
        self.wm_title("ico Converter")
        self.resizable(False, False)

        self.img_list = []

        # Buttons
        btn_load = tk.Button(text="Open Image", command= lambda: self.openImage())
        btn_load.pack()
        self.btn_save = tk.Button(text="Save Icon", command= lambda: self.saveIcon())
        self.btn_save.pack()
        self.btn_save["state"] = "disabled"
        
        lbl_preview = tk.Label(text="Icon Preview:", anchor=tk.W)
        # self.lbl_preview.grid(row= 2, column= 1)
        lbl_preview.pack()
        sizes = [16, 24, 32 ,48, 64, 128, 256]
        lbl_sizes = []
        self.can = []
        self.img_preview = []
        for size in sizes:
            # Labels
            index = sizes.index(size)
            lbl_sizes.append(tk.Label(text=str(size)+" x "+str(size)))
            # lbl_sizes[index].grid(row= 3, column=7-index)
            lbl_sizes[index].pack()

            # Preview Images of the different sizes
            index = sizes.index(size)
            self.can.append(tk.Canvas(self, width=size+10, height=size+10))
            # self.can[index].grid(row= 4, column= 7-index)
            self.can[index].pack()
            index = sizes.index(size)
            self.img_pre = ImageTk.PhotoImage(Image.new('RGBA', (size, size)))
            self.img_preview.append(self.can[index].create_image(5,5,anchor=tk.NW, image=self.img_pre))

    def openImage(self):
        # load image
        img_path = filedialog.askopenfilename()

        # return if open file dialog is canceld
        if img_path == "":
            return
        
        try:
            img = Image.open(img_path)
        except Exception as ex:
            messagebox.showerror(title="Image could not be loaded!", message="An error occured while loading the image.")
            return
        
        # generate ico scales of the source image
        try:
            self.img_list.clear()
            self.img_list = self.scaleToIcon(img)
            img.close()
        except Exception as ex:
            messagebox.showerror(title="Image could not be converted!", message="An error occured while converting the image.")
            return
        
        # show preview
        try:
            self.new_pre = []
            for index in range(len(self.img_list)):
                self.new_pre.append(ImageTk.PhotoImage(self.img_list[index]))
                self.can[index].itemconfig(self.img_preview[index], image=self.new_pre[index])
        except Exception as ex:
            messagebox.showerror(title="Preview could not be generated!", message="An error occured while preparing the preview.")
            return
        
        self.btn_save["state"] = "normal"
        
    def saveIcon(self):
        if len(self.img_list) != 0:
            icon_path = filedialog.asksaveasfilename(filetypes=[("Icon", ".ico")], defaultextension=".ico", initialfile="icon.ico")
            
            # return if save file dialog is canceld
            if icon_path == "":
                return
            
            # create an empty image container for the icon
            im = Image.new('RGBA', (257, 257))

            try:
            # save icon from the resized images 
                im.save(icon_path, format='ico', append_images=self.img_list)
            except Exception as ex:
                messagebox.showerror(title="Icon could not be saved!", message="An error occured while saving the icon.")
                return
        else:
            messagebox.showerror(title="No Icon found!", message="Please first load an Image.")
            return

    # generate a squared version of the image and scale it to all needed icon resolutions
    def scaleToIcon(self, img):
        # get height and width from the source image
        height = img.height
        width = img.width

        # if picture is not squared, make it square
        if height != width:
            x = 0
            y = 0

            # decide which axis is bigger and calculate the center position
            if height > width:
                size = height
                x = int((height / 2) - (width / 2))
            elif height < width:
                size = width
                y = int((width / 2) - (height / 2))

            img_boxed = Image.new('RGBA', (size,size))

            img_boxed.paste(img, (x, y))

            img = img_boxed

        # scale image according to icon sizes
        sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

        img_list = []
        for size in sizes:
            img_list.append(img.resize(size))

        return img_list

# main
if __name__ == "__main__":
    app = icoConverterApp()
    app.mainloop()
    del app
