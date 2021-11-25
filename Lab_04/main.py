from point import Point
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image

root = tk.Tk()
root.geometry('1000x700')

image = Image.new("RGB", (800, 550), (255, 255, 255))

p = []

tim = 0.0


def lin1(p1, p2, t):
    q = Point(0, 0)
    q.x = p2.x * t + p1.x * (1 - t)
    q.y = p2.y * t + p1.y * (1 - t)
    return q


def cast_r(t, n, m):
    global p
    if n == 0:
        return p[m]
    else:
        return lin1(cast_r(t, n - 1, m), cast_r(t, n - 1, m + 1), t)


def clean():
    canvas.delete("all")
    text.delete(1.0, END)


def draw():
    text.delete(1.0, END)
    n_str = segmentAmountEntry.get()

    x1_str = first_point_x_entry.get()
    y1_str = first_point_y_entry.get()

    x2_str = second_point_x_entry.get()
    y2_str = second_point_y_entry.get()

    x3_str = third_point_x_entry.get()
    y3_str = third_point_y_entry.get()

    x4_str = fourth_point_x_entry.get()
    y4_str = fourth_point_y_entry.get()

    if n_str.isnumeric() and x1_str.isnumeric() and y1_str.isnumeric() \
            and x2_str.isnumeric() and y2_str.isnumeric() \
            and x3_str.isnumeric() and y3_str.isnumeric() \
            and x4_str.isnumeric() and y4_str.isnumeric():
        n = int(n_str)

        p.append(Point(int(x1_str), int(y1_str)))
        p.append(Point(int(x2_str), int(y2_str)))
        p.append(Point(int(x3_str), int(y3_str)))
        p.append(Point(int(x4_str), int(y4_str)))

        d = 1 / n
        t = 0.0

        q = Point(0, 0)
        r = cast_r(t, 3, 0)
        text.insert(END, "X: " + str(r.x) + "\n")
        text.insert(END, "Y: " + str(r.y) + "\n")

        while t <= 1:
            t = t + d
            q = cast_r(t, 3, 0)
            text.insert(END, "X: " + str(q.x) + "\n")
            text.insert(END, "Y: " + str(q.y) + "\n")
            draw_line(r.x, r.y, q.x, q.y)
            r = q
        p.clear()
    else:
        messagebox.showerror("Ошибка!", "Введены некорректные данные")


def draw_line(x1=0, y1=0, x2=0, y2=0):
    global image
    global canvas
    dx = x2 - x1
    dy = y2 - y1

    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

    if dx < 0:
        dx = -dx
    if dy < 0:
        dy = -dy

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
            image.putpixel((int(x), int(y)), (0, 0, 0))
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
                image.putpixel((int(x), int(y)), (0, 0, 0))
                canvas.create_rectangle((x, y) * 2)


optionsFrame = Frame(master=root)
optionsFrame.place(x=10, y=10)

segmentAmountLabel = Label(master=optionsFrame, text="Число отрезков:")
segmentAmountLabel.grid(row=0, column=0)
segmentAmountEntry = Entry(master=optionsFrame)
segmentAmountEntry.grid(row=0, column=1)

infoLabel = Label(master=optionsFrame, text="Координаты точек кривой Безье:")
infoLabel.grid(row=1, column=1, padx=10, pady=10)

first_point_x_label = Label(master=optionsFrame, text="X1:")
first_point_x_label.grid(row=1, column=2, padx=5)
first_point_x_entry = Entry(master=optionsFrame)
first_point_x_entry.grid(row=1, column=3)

first_point_y_label = Label(master=optionsFrame, text="Y1:")
first_point_y_label.grid(row=2, column=2, padx=5)
first_point_y_entry = Entry(master=optionsFrame)
first_point_y_entry.grid(row=2, column=3)

second_point_x_label = Label(master=optionsFrame, text="X2:")
second_point_x_label.grid(row=1, column=4, padx=5)
second_point_x_entry = Entry(master=optionsFrame)
second_point_x_entry.grid(row=1, column=5)

second_point_y_label = Label(master=optionsFrame, text="Y2:")
second_point_y_label.grid(row=2, column=4, padx=5)
second_point_y_entry = Entry(master=optionsFrame)
second_point_y_entry.grid(row=2, column=5)

third_point_x_label = Label(master=optionsFrame, text="X3:")
third_point_x_label.grid(row=1, column=6, padx=5)
third_point_x_entry = Entry(master=optionsFrame)
third_point_x_entry.grid(row=1, column=7)

third_point_y_label = Label(master=optionsFrame, text="Y3:")
third_point_y_label.grid(row=2, column=6, padx=5)
third_point_y_entry = Entry(master=optionsFrame)
third_point_y_entry.grid(row=2, column=7)

fourth_point_x_label = Label(master=optionsFrame, text="X4:")
fourth_point_x_label.grid(row=1, column=8, padx=5)
fourth_point_x_entry = Entry(master=optionsFrame)
fourth_point_x_entry.grid(row=1, column=9)

fourth_point_y_label = Label(master=optionsFrame, text="Y4:")
fourth_point_y_label.grid(row=2, column=8, padx=5)
fourth_point_y_entry = Entry(master=optionsFrame)
fourth_point_y_entry.grid(row=2, column=9)

draw_button = Button(master=optionsFrame, text="Рисовать", command=draw)
draw_button.grid(row=2, column=0)

clear_button = Button(master=optionsFrame, text="Очистить", command=clean)
clear_button.grid(row=2, column=1)

canvas = Canvas(master=root, width=800, height=550, bg='white')
canvas.place(x=10, y=100)

text = Text(master=root, width=20, height=30, bg='white')
text.place(x=825, y=100)

root.mainloop()
