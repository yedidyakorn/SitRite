import tkinter as tk
from PIL import ImageTk, Image

list_photo = ["1.PNG", "2.PNG", "3.PNG", "4.PNG", "5.PNG", "6.jpeg"]
count = 0


def next(panel):
    global count
    if count < len(list_photo) - 2:
        count = count + 1
        path = list_photo[count]
        img = ImageTk.PhotoImage(Image.open(path))
        panel.configure(image=img)
        panel.image = img  # keep a reference!
    elif count < len(list_photo) - 1:
        btn_text.set("Done")
        count = count + 1
        path = list_photo[count]
        img = ImageTk.PhotoImage(Image.open(path))
        panel.configure(image=img)
        panel.image = img  # keep a reference!
    else:
        window.destroy()


def prev(panel):
    global count
    if count > 0:
        btn_text.set("Next")
        count = count - 1
        path = list_photo[count]
        img = ImageTk.PhotoImage(Image.open(path))
        panel.configure(image=img)
        panel.image = img  # keep a reference!


# Create main window
window = tk.Tk()
##tk.Grid.rowconfigure(window, 0, weight=1)
##tk.Grid.columnconfigure(window, 0, weight=1)
##frame = tk.Frame(window)
##frame.grid(row=0, column=0, sticky="nsew")

# divide window into two sections. One for image. One for buttons
top = tk.Frame(window)
top.pack(side="top")
bottom = tk.Frame(window)
bottom.pack(side="bottom")

# place image
path = "1.PNG"
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(window, image=img)
panel.image = img  # keep a reference!
panel.pack(side="top", fill="both", expand="yes")

# place buttons
prev_button = tk.Button(window, text="Previous", width=10, height=2, command=lambda: prev(panel))
prev_button.pack(in_=bottom, side="left")
btn_text = tk.StringVar()
btn_text.set("Next")
next_button = tk.Button(window, textvariable=btn_text, width=10, height=2, command=lambda: next(panel))
next_button.pack(in_=bottom, side="right")

# Start the GUI
window.mainloop()
