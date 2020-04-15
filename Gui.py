import re,uuid
from tkinter import *


imageLink = 'server ip goes here'
bandGenre = ''


def submit():
    #set up for first call
    global imageLink , bandGenre;
    imageLink = str(textbox.get())
    bandGenre = str(textbox2.get())
    #CODE TO SUBMIT TO HTTP? or call GAN py file
    window.destroy()


def clearData():
    window.destroy()

# set up GUI for first portion (GET IMAGES LINK (git hub) and band genre)
window = Tk()
window.geometry("250x200")
window.title("Band Album Generator")

imageLabel= Label(window, text ="Images link Here")
imageLabel.pack(pady=2, padx=2)

imageName = StringVar()
textbox = Entry(window, textvariable=imageName)
textbox.focus_set()
textbox.pack(pady=10, padx=10)

serverPortLabel= Label(window,text ="Band Genre Here")
serverPortLabel.pack(pady=2, padx=2)

bandGenre = StringVar()
textbox2 = Entry(window, textvariable=bandGenre)
textbox2.focus_set()
textbox2.pack(pady=10, padx=10)

subButton = Button(window, text="Submit", command=submit)
subButton.pack(pady=2, padx=2)

window.mainloop()




# set up GUI for second portion
window = Tk()
window.geometry("250x200")
window.title("Generated Image")



# button for quiting the program
Button(window, text="Quit", width=8, bg="green", fg="white", command=clearData).grid(row=2, column=10)

window.mainloop()
