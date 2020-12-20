import math
import mycv
from tkinter import messagebox
from tkinter import *
import cv2
from PIL import Image, ImageTk
import Intro
import myopencv

limitAngle=7

# Main window

window = Tk()
window.title("SiT RiTe")
window.geometry("1080x720")
window.minsize(480, 360)
# window.iconbitmap("ergonomie.ico")
window.config(background="#8B0000")

# CAMERA APPEARANCE
width_cam, height_cam = 1080, 720
cap = cv2.VideoCapture(0) #chose 0 for main camera, 1 for side camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_cam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_cam)

window2 = Toplevel(window)
# window2.geometry("720x480")
window2.config(background="#8B0000")
window2.title("SiT RiTe")
window2.bind('<Escape>', lambda e: window2.quit())
lmain = Label(window2)
lmain.pack(side='top')

baseAngles=None
frame = None

def take_capture():
    global baseAngles
    global frame
    cv2.imwrite('Output-Skeleton.jpg', frame)
    baseAngles=mycv.checkImg(frame)

    # window2.withdraw()
    # baseAngle=function(show_frame())


capture_button = Button(window2, text="capture", font=("Arial", 20), bg="white", command=take_capture)
capture_button.pack(side='bottom')

label_explication = Label(window2, text="Please place yourself according to the instructions"
                                        " received previously and then click on Capture Button",
                          font=("Arial", 15), bg="#8B0000", fg="gold", borderwidth=3,
                          relief="sunken")

label_close = Label(window2, text="Click on escape to close the window",
                    font=("Arial", 15), bg="#8B0000", fg="gold", borderwidth=2,
                    relief="sunken")

label_explication.pack(expand='yes')
label_close.pack(expand='yes')

def calcDiffAngles(current,base):
    global limitAngle
    if current==None or base==None:
        return False
    else:
        return (abs(current-base)>limitAngle)

def show_frame():
    global baseAngles
    global frame
    global limitAngle
    window.withdraw()
    check, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if(baseAngles!=None):
        currentAngles = mycv.checkImg(frame)
        #take care about exeptoin angle==None
        if calcDiffAngles(currentAngles[0],baseAngles[0]) or calcDiffAngles(currentAngles[1],baseAngles[1]):
            print("Oh no")
            messagebox.showwarning("Warning", "היציבה שלך לא נכונה")
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)  # recusrion


image = PhotoImage(file="don't-worry-img.png")
width = 600
height = 250
canvas = Canvas(window, width=width, height=height, bg="#8B0000", bd=0, highlightthickness=0)
canvas.create_image(width / 2, height / 2, image=image)
#canvas.place(x='200', y='50')
canvas.pack(side='top')



def PermissionButton():
    MsgBox = messagebox.askquestion('Check Permission', 'do you allow the app to use your camera?')
    if MsgBox == 'no':
        messagebox.showinfo('Exit', 'Exit because no Camera Permission')
        window.destroy()
    else:
        messagebox.showinfo('Welcome', 'Welcome to the App')
        show_frame()


# Agree Button and Label
agree_button = Button(window, text='Agree', font=("Arial", 20), bg="white", command=PermissionButton)
agree_button.pack(side='bottom', pady=25)


label_privacy = Label(window, text="Your privacy is our priority\n"
                                   "Your Personal data is safe here and is yours alone.\nThank you.",
                      font=("Arial", 30), bg="#8B0000", fg="gold", borderwidth=0,
                      relief="sunken")

label_privacy.pack(expand='yes')
# show the result
window.mainloop()
