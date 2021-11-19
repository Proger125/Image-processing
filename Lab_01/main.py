import tkinter as tk
import numpy as np
from tkinter import filedialog as fd
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry('1000x700')

image = Image.new("RGB", (800, 400), (255, 255, 255))
photo = None
c_image = None
first_point_x_entry = Entry()
first_point_y_entry = Entry()
second_point_x_entry = Entry()
second_point_y_entry = Entry()
center_point_x_entry = Entry()
center_point_y_entry = Entry()
radius_entry = Entry()
v_radius_entry = Entry()
h_radius_entry = Entry()
fill_point_x_entry = Entry()
fill_point_y_entry = Entry()
line_type = IntVar()
line_type.set(0)


def draw_pixel(x=0, y=0):
    if 0 < x < image.width:
        if 0 < y < image.height:
            image.putpixel((x, y), (0, 0, 0))
            canvas.create_rectangle((x, y) * 2)


def rgb_to_hex(red, green, blue):
    return '#%02x%02x%02x' % (red, green, blue)


def draw_fill_pixel(x, y, color):
    if 0 < x < image.width:
        if 0 < y < image.height:
            image.putpixel((x, y), color)
            hex_color = rgb_to_hex(color[0], color[1], color[2])
            canvas.create_rectangle((x, y) * 2, outline=hex_color)


def fill_wrapper():
    x_str = fill_point_x_entry.get()
    y_str = fill_point_y_entry.get()
    if x_str.isnumeric() and y_str.isnumeric():
        x = int(x_str)
        y = int(y_str)
        color = tuple(np.random.choice(range(256), size=3))
        fill(x, y, color)


def fill(x, y, color):
    to_fill = set()
    to_fill.add((x, y))
    while not len(to_fill) == 0:
        (x, y) = to_fill.pop()
        current_color = image.getpixel((x, y))
        if current_color == (0, 0, 0) or current_color == color:
            continue
        draw_fill_pixel(x, y, color)
        to_fill.add((x - 1, y))
        to_fill.add((x + 1, y))
        to_fill.add((x, y - 1))
        to_fill.add((x, y + 1))


def draw_line_wrapper():
    x1_str = first_point_x_entry.get()
    y1_str = first_point_y_entry.get()
    x2_str = second_point_x_entry.get()
    y2_str = second_point_y_entry.get()
    if x1_str.isnumeric() and y1_str.isnumeric() and x2_str.isnumeric() and y2_str.isnumeric():
        x1 = int(x1_str)
        y1 = int(y1_str)
        x2 = int(x2_str)
        y2 = int(y2_str)
        draw_line(x1, y1, x2, y2)
    else:
        messagebox.showerror("Ошибка!", "Введены некорректные данные")


def draw_circle_wrapper():
    x_str = center_point_x_entry.get()
    y_str = center_point_y_entry.get()
    r_str = radius_entry.get()
    if x_str.isnumeric() and y_str.isnumeric() and r_str.isnumeric():
        x = int(center_point_x_entry.get())
        y = int(center_point_y_entry.get())
        r = int(radius_entry.get())
        draw_circle(x, y, r)
    else:
        messagebox.showerror("Ошибка!", "Введены некорректные данные")


def draw_ellipse_wrapper():
    x_str = center_point_x_entry.get()
    y_str = center_point_y_entry.get()
    v_r_str = v_radius_entry.get()
    h_r_str = h_radius_entry.get()
    if x_str.isnumeric() and y_str.isnumeric() and v_r_str.isnumeric() and h_r_str.isnumeric():
        x = int(center_point_x_entry.get())
        y = int(center_point_y_entry.get())
        v_r = int(v_radius_entry.get())
        h_r = int(h_radius_entry.get())
        draw_ellipse(h_r, v_r, x, y)
    else:
        messagebox.showerror("Ошибка!", "Введены некорректные данные")


def draw_line(x1=0, y1=0, x2=0, y2=0):
    dx = x2 - x1
    dy = y2 - y1

    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

    if dx < 0: dx = -dx
    if dy < 0: dy = -dy

    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy

    x, y = x1, y1

    error, t = el / 2, 0
    if 0 < x < image.width:
        if 0 < y < image.height:
            image.putpixel((x, y), (0, 0, 0))
            canvas.create_rectangle((x, y) * 2)

    while t < el:
        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1
        if 0 < x < image.width:
            if 0 < y < image.height:
                image.putpixel((x, y), (0, 0, 0))
                canvas.create_rectangle((x, y) * 2)


def draw_circle(x, y, r):
    disp_x = x
    disp_y = y
    x = 0
    y = r
    delta = (1 - 2 * r)
    while y >= 0:
        draw_pixel(disp_x + x, disp_y + y)
        draw_pixel(disp_x + x, disp_y - y)
        draw_pixel(disp_x - x, disp_y + y)
        draw_pixel(disp_x - x, disp_y - y)

        error = 2 * (delta + y) - 1
        if (delta < 0) and (error <= 0):
            x += 1
            delta = delta + (2 * x + 1)
            continue
        error = 2 * (delta - x) - 1
        if (delta > 0) and (error > 0):
            y -= 1
            delta = delta + (1 - 2 * y)
            continue
        x += 1
        delta = delta + (2 * (x - y))
        y -= 1


def draw_ellipse(rx, ry, xc, yc):
    x = 0
    y = ry

    d1 = ((ry * ry) - (rx * rx * ry) +
          (0.25 * rx * rx))
    dx = 2 * ry * ry * x
    dy = 2 * rx * rx * y

    while dx < dy:
        draw_pixel(x + xc, y + yc)
        draw_pixel(-x + xc, y + yc)
        draw_pixel(x + xc, -y + yc)
        draw_pixel(-x + xc, -y + yc)

        if d1 < 0:
            x += 1
            dx = dx + (2 * ry * ry)
            d1 = d1 + dx + (ry * ry)
        else:
            x += 1
            y -= 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            d1 = d1 + dx - dy + (ry * ry)

    d2 = (((ry * ry) * ((x + 0.5) * (x + 0.5))) +
          ((rx * rx) * ((y - 1) * (y - 1))) -
          (rx * rx * ry * ry))

    while y >= 0:
        draw_pixel(x + xc, y + yc)
        draw_pixel(-x + xc, y + yc)
        draw_pixel(x + xc, -y + yc)
        draw_pixel(-x + xc, -y + yc)

        if d2 > 0:
            y -= 1
            dy = dy - (2 * rx * rx)
            d2 = d2 + (rx * rx) - dy
        else:
            y -= 1
            x += 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            d2 = d2 + dx - dy + (rx * rx)


def open_image_handler():
    file_name = fd.askopenfilename(filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png")))
    global image
    global photo
    global c_image
    image = Image.open(file_name)
    image = image.resize((canvas.winfo_width(), canvas.winfo_height()), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    c_image = canvas.create_image(0, 0, anchor='nw', image=photo)


def save_image_handler():
    file = fd.asksaveasfile(filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png")))
    file_name = file.name
    if '.' not in file_name:
        messagebox.showerror("Ошибка", "Отсутствует расширение!")
    else:
        image.save(file_name)


def change_line_type_handler():
    for widget in lineOptionsFrame.winfo_children():
        widget.destroy()

    value = line_type.get()
    if value == 0:
        global first_point_x_entry
        global first_point_y_entry
        global second_point_x_entry
        global second_point_y_entry
        first_point_x_label = Label(master=lineOptionsFrame, text="X координата первой точки: ")
        first_point_x_label.grid(row=0, column=0, padx=10, pady=10)
        first_point_x_entry = Entry(master=lineOptionsFrame)
        first_point_x_entry.grid(row=0, column=1, padx=10, pady=10)
        first_point_y_label = Label(master=lineOptionsFrame, text="Y координата первой точки: ")
        first_point_y_label.grid(row=1, column=0, padx=10, pady=10)
        first_point_y_entry = Entry(master=lineOptionsFrame)
        first_point_y_entry.grid(row=1, column=1, padx=10, pady=10)
        second_point_x_label = Label(master=lineOptionsFrame, text="X координата второй точки: ")
        second_point_x_label.grid(row=0, column=2, padx=10, pady=10)
        second_point_x_entry = Entry(master=lineOptionsFrame)
        second_point_x_entry.grid(row=0, column=3, padx=10, pady=10)
        second_point_y_label = Label(master=lineOptionsFrame, text="Y координата второй точки: ")
        second_point_y_label.grid(row=1, column=2, padx=10, pady=10)
        second_point_y_entry = Entry(master=lineOptionsFrame)
        second_point_y_entry.grid(row=1, column=3, padx=10, pady=10)

        draw_button = Button(master=lineOptionsFrame, text="Нарисовать", command=draw_line_wrapper)
        draw_button.grid(row=0, column=4, padx=10, pady=10)
    if value == 1:
        global center_point_x_entry
        global center_point_y_entry
        global radius_entry
        center_point_x_label = Label(master=lineOptionsFrame, text="X координата центра окружности: ")
        center_point_x_label.grid(row=0, column=0, padx=10, pady=10)
        center_point_x_entry = Entry(master=lineOptionsFrame)
        center_point_x_entry.grid(row=0, column=1, padx=10, pady=10)
        center_point_y_label = Label(master=lineOptionsFrame, text="Y координата центра окружности: ")
        center_point_y_label.grid(row=1, column=0, padx=10, pady=10)
        center_point_y_entry = Entry(master=lineOptionsFrame)
        center_point_y_entry.grid(row=1, column=1, padx=10, pady=10)
        radius_label = Label(master=lineOptionsFrame, text="Радиус окружности: ")
        radius_label.grid(row=0, column=2)
        radius_entry = Entry(master=lineOptionsFrame)
        radius_entry.grid(row=0, column=3)
        draw_button = Button(master=lineOptionsFrame, text="Нарисовать", command=draw_circle_wrapper)
        draw_button.grid(row=0, column=4, padx=10, pady=10)
    if value == 2:
        global v_radius_entry
        global h_radius_entry
        center_point_x_label = Label(master=lineOptionsFrame, text="X координата центра эллипса: ")
        center_point_x_label.grid(row=0, column=0, padx=10, pady=10)
        center_point_x_entry = Entry(master=lineOptionsFrame)
        center_point_x_entry.grid(row=0, column=1, padx=10, pady=10)
        center_point_y_label = Label(master=lineOptionsFrame, text="Y координата центра эллипса: ")
        center_point_y_label.grid(row=1, column=0, padx=10, pady=10)
        center_point_y_entry = Entry(master=lineOptionsFrame)
        center_point_y_entry.grid(row=1, column=1, padx=10, pady=10)
        v_radius_label = Label(master=lineOptionsFrame, text="Вертикальный радиус эллипса: ")
        v_radius_label.grid(row=0, column=2)
        v_radius_entry = Entry(master=lineOptionsFrame)
        v_radius_entry.grid(row=0, column=3)
        h_radius_label = Label(master=lineOptionsFrame, text="Горизонтальный радиус эллипса: ")
        h_radius_label.grid(row=1, column=2)
        h_radius_entry = Entry(master=lineOptionsFrame)
        h_radius_entry.grid(row=1, column=3)
        draw_button = Button(master=lineOptionsFrame, text="Нарисовать", command=draw_ellipse_wrapper)
        draw_button.grid(row=0, column=4, padx=10, pady=10)
    if value == 3:
        global fill_point_x_entry
        global fill_point_y_entry
        fill_point_x_label = Label(master=lineOptionsFrame, text="X координата точки закрашивания: ")
        fill_point_x_label.grid(row=0, column=0, padx=10, pady=10)
        fill_point_x_entry = Entry(master=lineOptionsFrame)
        fill_point_x_entry.grid(row=0, column=1, padx=10, pady=10)

        fill_point_y_label = Label(master=lineOptionsFrame, text="Y координата точки закрашивания: ")
        fill_point_y_label.grid(row=1, column=0, padx=10, pady=10)
        fill_point_y_entry = Entry(master=lineOptionsFrame)
        fill_point_y_entry.grid(row=1, column=1, padx=10, pady=10)
        fill_button = Button(master=lineOptionsFrame, text="Закрасить", command=fill_wrapper)
        fill_button.grid(row=0, column=4, padx=10, pady=10)


openImageButton = Button(master=root, text="Открыть изображение", command=open_image_handler)
openImageButton.place(x=10, y=10)

saveImageButton = Button(master=root, text="Сохранить изображение", command=save_image_handler)
saveImageButton.place(x=150, y=10)

lineTypeFrame = Frame(master=root)
lineTypeFrame.place(x=10, y=50)

line_radio = Radiobutton(master=lineTypeFrame, text='Отрезок', variable=line_type, value=0,
                         command=change_line_type_handler)
line_radio.grid(row=0, column=0)
circle_radio = Radiobutton(master=lineTypeFrame, text='Окружность', variable=line_type, value=1,
                           command=change_line_type_handler)
circle_radio.grid(row=0, column=1)
ellipse_radio = Radiobutton(master=lineTypeFrame, text='Эллипс', variable=line_type, value=2,
                            command=change_line_type_handler)
ellipse_radio.grid(row=0, column=2)

fill_radio = Radiobutton(master=lineTypeFrame, text='Заливка', variable=line_type, value=3,
                         command=change_line_type_handler)
fill_radio.grid(row=0, column=3)

lineOptionsFrame = Frame(master=root)
lineOptionsFrame.place(x=10, y=80)
change_line_type_handler()

canvas = Canvas(master=root, width=800, height=400)
canvas.place(x=10, y=200)

root.mainloop()
