from tkinter import messagebox
from tkinter import *
import cv2
from PIL import Image, ImageTk

#Main window

window = Tk()
window.title("SiT RiTe")
window.geometry("1080x720")
window.minsize(480, 360)
window.iconbitmap("ergonomie.ico")
window.config(background="#71A1AC")

# CAMERA APPEARANCE
width_cam, height_cam = 1080, 720
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_cam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_cam)

# creation of window with camera

window2 = Toplevel(window)
#window2.geometry("720x480")
#window2.config(background="#71A1AC")
window2.bind('<Escape>', lambda e: window2.quit())
lmain = Label(window2)
lmain.pack(side='top')
button_capture = Button(window2, text="Take Capture").pack(side='bottom')

def show_frame():
    window.withdraw()
    check, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)  # recursion


# Title
label_title = Label(window, text="Personal Information", font=("Verdana", 40), bg="#71A1AC", bd=1)
label_title.pack()

# firstname
label_first_name = Label(window, text="First Name", font=("Verdana", 20), bg="#71A1AC")
label_first_name.place(x='100', y='150')

entry_first_name = Entry(window, font=("Verdana", 20), bg="#71A1AC")
entry_first_name.place(x='300', y='150')

# lastname
label_last_name = Label(window, text="Last Name", font=("Verdana", 20), bg="#71A1AC")
label_last_name.place(x='100', y='250')

entry_last_name = Entry(window, font=("Verdana", 20), bg="#71A1AC")
entry_last_name.place(x='300', y='250')

# age
label_age = Label(window, text="Age", font=("Verdana", 20), bg="#71A1AC")
label_age.place(x='100', y='350')

entry_age = Entry(window, font=("Verdana", 20), bg="#71A1AC")
entry_age.place(x='300', y='350')

# image

image = PhotoImage(file='image_ergonomic.png')
width = 560
height = 625
canvas = Canvas(window, width=width, height=height, bg="#71A1AC", bd=1)
canvas.create_image(width / 2, height / 2, image=image)
canvas.place(x='750', y='80')


def PermissionButton():
    MsgBox = messagebox.askquestion('Check Permission', 'do you allow the app to use your camera?')
    if MsgBox == 'no':
        messagebox.showinfo('Exit', 'Exit because no Camera Permission')
        window.destroy()
    else:
        messagebox.showinfo('Welcome', 'Welcome to the App')
        show_frame()


# Confirm Button
confirmation_button = Button(window, text='Confirm', font=("Verdana", 20), bg="white", command=PermissionButton)
confirmation_button.pack(pady=25, fill=X)
confirmation_button.place(x='360', y='430')

# show the result
window.mainloop()
