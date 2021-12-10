import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2

root = tk.Tk()
root.geometry('1300x700')

main_image_cv2 = None

median_filter_image_cv2 = None

averaging_filter_image_cv2 = None


def open_image_handler():
    global main_image_cv2
    file_name = fd.askopenfilename(filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png")))
    main_image_cv2 = cv2.imread(file_name)
    main_image_cv2 = cv2.cvtColor(main_image_cv2, cv2.COLOR_BGR2RGB)
    figure = plt.figure(figsize=(4, 4))
    c = FigureCanvasTkAgg(figure, root)
    c.get_tk_widget().place(x=10, y=200)
    plt.subplot(111), plt.imshow(main_image_cv2), plt.title('Original')
    draw_median_filter_image_button['state'] = 'active'
    draw_averaging_filter_image_button['state'] = 'active'


def draw_median_filter_image_handler():
    global main_image_cv2
    global median_filter_image_cv2
    shift_str = median_operator_entry.get()
    if shift_str.isnumeric():
        shift = int(shift_str)
        figure = plt.figure(figsize=(4, 4))
        c = FigureCanvasTkAgg(figure, root)
        c.get_tk_widget().place(x=830, y=200)
        median_filter_image_cv2 = cv2.medianBlur(main_image_cv2, shift)
        plt.subplot(111), plt.imshow(median_filter_image_cv2), plt.title(
            'Median filter')
        plt.xticks([]), plt.yticks([])
        plt.show()
    else:
        messagebox.showerror("Ошибка!", "Введены некорректные данные")


def draw_average_filter_image_handler():
    global main_image_cv2
    global averaging_filter_image_cv2
    size_str = average_operator_entry.get()
    if size_str.isnumeric():
        size = int(size_str)
        figure = plt.figure(figsize=(4, 4))
        c = FigureCanvasTkAgg(figure, root)
        c.get_tk_widget().place(x=420, y=200)
        averaging_filter_image_cv2 = cv2.blur(main_image_cv2, (size, size))
        plt.subplot(111), plt.imshow(averaging_filter_image_cv2), plt.title('Mean filter')
        plt.xticks([]), plt.yticks([])
        plt.show()
    else:
        messagebox.showerror("Ошибка!", "Введены некорректные данные")


optionFrame = Frame(master=root)
optionFrame.place(x=10, y=10)

open_image_button = Button(master=optionFrame, text="Открыть", command=open_image_handler)
open_image_button.grid(row=0, column=0, padx=10, pady=10)

draw_median_filter_image_button = Button(master=optionFrame, text="Median", command=draw_median_filter_image_handler)
draw_median_filter_image_button.grid(row=0, column=3, padx=10, pady=10)
draw_median_filter_image_button['state'] = 'disabled'

draw_averaging_filter_image_button = Button(master=optionFrame, text="Mean", command=draw_average_filter_image_handler)
draw_averaging_filter_image_button.grid(row=0, column=1, padx=10, pady=10)
draw_averaging_filter_image_button['state'] = 'disabled'

average_operator_label = Label(master=optionFrame, text="Size for average operator:")
average_operator_label.grid(row=1, column=0, padx=10, pady=10)
average_operator_entry = Entry(master=optionFrame)
average_operator_entry.grid(row=1, column=1, padx=10, pady=10)

median_operator_label = Label(master=optionFrame, text="Shift for median operator:")
median_operator_label.grid(row=1, column=2, padx=10, pady=10)
median_operator_entry = Entry(master=optionFrame)
median_operator_entry.grid(row=1, column=3, padx=10, pady=10)

root.mainloop()
