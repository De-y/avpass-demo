#1. Create a tkinter window with a gif being displayed, located at c:/Users/accur/OneDrive/Documents/Github/Kosciuszko-UNO/libraries/Kosciuszko/ad54de93081323c9a0f07d02abae8c49_4599926581997439003.gif

import tkinter as tk
from PIL import Image, ImageTk
from itertools import count

class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


root = tk.Tk()
root.title("Jumpy Dumpty")
root.iconbitmap("c:/Users/accur/OneDrive/Documents/Github/Kosciuszko-UNO/libraries/Kosciuszko/ico.ico")
lbl = ImageLabel(root)
lbl.pack()
lbl.load('c:/Users/accur/OneDrive/Documents/Github/Kosciuszko-UNO/libraries/Kosciuszko/ad54de93081323c9a0f07d02abae8c49_4599926581997439003.gif')
root.mainloop()
