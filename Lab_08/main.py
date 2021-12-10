import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2

root = tk.Tk()
root.geometry('1300x700')

main_image_cv2 = None

contour_image_cv2 = None

hsv_min = np.array((59, 119, 17), np.uint8)
hsv_max = np.array((79, 255, 255), np.uint8)


def open_image_handler():
    global main_image_cv2
    file_name = fd.askopenfilename(filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png")))
    main_image_cv2 = cv2.imread(file_name)
    main_image_cv2 = cv2.cvtColor(main_image_cv2, cv2.COLOR_BGR2RGB)
    figure = plt.figure(figsize=(4, 4))
    c = FigureCanvasTkAgg(figure, root)
    c.get_tk_widget().place(x=10, y=200)
    plt.subplot(111), plt.imshow(main_image_cv2), plt.title('Original')
    make_contour_button['state'] = 'active'


def make_contours():
    global contour_image_cv2
    global main_image_cv2
    contour_image_cv2 = cv2.cvtColor(main_image_cv2, cv2.COLOR_RGB2GRAY)

    figure = plt.figure(figsize=(4, 4))
    c = FigureCanvasTkAgg(figure, root)
    c.get_tk_widget().place(x=420, y=200)
    plt.subplot(111), plt.imshow(cv2.cvtColor(contour_image_cv2, cv2.COLOR_BGR2RGB)), plt.title('Gray image')

    ret, thresh = cv2.threshold(contour_image_cv2, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(main_image_cv2, contours, -1, (255, 0, 0), 2)

    figure = plt.figure(figsize=(4, 4))
    c = FigureCanvasTkAgg(figure, root)
    c.get_tk_widget().place(x=830, y=200)
    plt.subplot(111), plt.imshow(main_image_cv2), plt.title('With Contour')


optionFrame = Frame(master=root)
optionFrame.place(x=10, y=10)

open_image_button = Button(master=optionFrame, text="Открыть", command=open_image_handler)
open_image_button.grid(row=0, column=0, padx=10, pady=10)

make_contour_button = Button(master=optionFrame, text="Найти объекты", command=make_contours)
make_contour_button.grid(row=0, column=1, padx=10, pady=10)
make_contour_button['state'] = 'disabled'

root.mainloop()

