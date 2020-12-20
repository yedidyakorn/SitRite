import tkinter as tk
from PIL import ImageTk, Image

list_photo = ["image1.jfif", "image2.jfif", "image3.jfif"]
count = 0


def next(panel):
    global count
    if count < len(list_photo) - 1:
        count = count + 1
        path = list_photo[count]
        img = ImageTk.PhotoImage(Image.open(path))
        panel.configure(image=img)
        panel.image = img  # keep a reference!



def prev(panel):
    global count
    if count > 0:
        count = count - 1
        path = list_photo[count]
        img = ImageTk.PhotoImage(Image.open(path))
        panel.configure(image=img)
        panel.image = img  # keep a reference!


# Create main window
window = tk.Tk()
window.geometry("720x480")
window.config(background="#71A1AC")

# divide window into two sections. One for image. One for buttons
top = tk.Frame(window)
top.pack(side="top")
bottom = tk.Frame(window)
bottom.pack(side="bottom")

# place image
path = list_photo[0]
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(window, image=img)
panel.image = img  # keep a reference!
panel.pack(side="top", fill="both", expand="yes")

# place buttons
prev_button = tk.Button(window, text="Previous", width=10, height=2, command=lambda: prev(panel))
prev_button.pack(in_=bottom, side="left")
next_button = tk.Button(window, text="Next", width=10, height=2, command=lambda: next(panel))
next_button.pack(in_=bottom, side="right")

# Start the GUI
window.mainloop()
