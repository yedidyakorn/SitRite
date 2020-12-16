from tkinter import *


root = Tk()

photo = PhotoImage(file="1.PNG")
label = Label(root, image=photo)
label.pack()

btn = Button(root, text="NEXT", font=("Verdana", 20), bg="White")
btn.pack(pady=25)

root.mainloop()