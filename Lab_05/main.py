import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2

root = tk.Tk()
root.geometry('1200x700')

image = Image.new("RGB", (800, 550), (255, 255, 255))
photo = None
c_image = None
img = None
pix = []


def open_image_handler():
    file_name = fd.askopenfilename(filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png")))
    global image
    global photo
    global c_image
    global pix
    global img
    image = Image.open(file_name)
    img = cv2.imread(file_name)
    image = image.resize((canvas.winfo_width(), canvas.winfo_height()), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    c_image = canvas.create_image(0, 0, anchor='nw', image=photo)
    build_hists_button['state'] = 'active'
    pix = image.load()


def build_hist():
    color = ('b', 'g', 'r')
    figure = plt.Figure(figsize=(5, 5), dpi=100)
    ax = figure.add_subplot(111)
    c = FigureCanvasTkAgg(figure, root)
    c.get_tk_widget().place(x=570, y=10)
    for i, col in enumerate(color):
        hist = cv2.calcHist([img], [i], None, [256], [0, 256])
        ax.plot(hist, color=col)


canvas = Canvas(master=root, width=550, height=550, bg='white')
canvas.place(x=10, y=10)

open_image_button = Button(master=root, text="Открыть", command=open_image_handler)
open_image_button.place(x=10, y=570)

build_hists_button = Button(master=root, text="Построить гистограмму", command=build_hist)
build_hists_button.place(x=100, y=570)
build_hists_button['state'] = 'disabled'

root.mainloop()
