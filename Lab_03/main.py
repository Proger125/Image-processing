import tkinter as tk
import numpy as np
from tkinter import *
from tkinter import messagebox
from PIL import Image
from point import Point
from segment import Segment
from cutter import Cutter

root = tk.Tk()
root.geometry('1000x700')

main_image = Image.new("RGB", (400, 400), (255, 255, 255))
cut_image = Image.new("RGB", (400, 400), (255, 255, 255))

cutter = Cutter(Point(x=0, y=0), Point(x=0, y=0))

flag = True

segment_list = []


def clear_main_canvas():
    main_canvas.delete("all")


def clear_cutter_canvas():
    cutter_canvas.delete("all")


def find_point_code(point):
    t = [0] * 4
    t[0] = 1 if point.x < cutter.left_up_point.x else 0
    t[1] = 1 if point.x > cutter.right_down_point.x else 0
    t[2] = 1 if point.y > cutter.right_down_point.y else 0
    t[3] = 1 if point.y < cutter.left_up_point.y else 0
    return t


def find_r_point(start, end, is_first):
    global flag
    eps = 0.0000001
    m = 10 ** 30
    q = start if is_first else end

    if start.x != end.x:
        m = (end.y - start.y) / (end.x - start.x)

        if cutter.left_up_point.x >= q.x:
            y = np.round(m * (cutter.left_up_point.x - q.x) + q.y)
            if (y >= cutter.left_up_point.y) and (y <= cutter.right_down_point.y):
                return Point(cutter.left_up_point.x, y)

        if cutter.right_down_point.x <= q.x:
            y = np.round(m * (cutter.right_down_point.x - q.x) + q.y)
            if (y >= cutter.left_up_point.y) and (y <= cutter.right_down_point.y):
                return Point(cutter.right_down_point.x, y)

    if np.abs(m - 0) <= eps:
        flag = False
        return q

    if cutter.left_up_point.y >= q.y:
        x = np.round((cutter.left_up_point.y - q.y) / m + q.x)
        if (x >= cutter.left_up_point.x) and (x <= cutter.right_down_point.x):
            return Point(x, cutter.left_up_point.y)

    if cutter.right_down_point.y <= q.y:
        x = np.round((cutter.right_down_point.y - q.y) / m + q.x)
        if (x >= cutter.left_up_point.x) and (x <= cutter.right_down_point.x):
            return Point(x, cutter.right_down_point.y)

    flag = False
    return q


def segment_cut_off(start, end):
    r1 = start
    r2 = end

    s1 = 0
    s2 = 0
    pl = 0

    t1 = find_point_code(start)
    t2 = find_point_code(end)

    k = 0
    while k < 4:
        s1 = s1 + t1[k]
        s2 = s2 + t2[k]

        pl = pl + t1[k] * t2[k]

        k = k + 1

    if (s1 == 0) and (s2 == 0):
        draw_line(cut_image, cutter_canvas, start.x, start.y, end.x, end.y)
        return

    if pl != 0:
        return

    if s1 != 0:
        r1 = find_r_point(start=start, end=end, is_first=True)

    if s2 != 0:
        r2 = find_r_point(start=start, end=end, is_first=False)

    if flag:
        draw_line(cut_image, cutter_canvas, r1.x, r1.y, r2.x, r2.y)


def draw_cut_line_wrapper():
    global cutter

    x1_str = left_up_point_x_entry.get()
    y1_str = left_up_point_y_entry.get()
    x2_str = right_down_point_x_entry.get()
    y2_str = right_down_point_y_entry.get()

    if x1_str.isnumeric() and y1_str.isnumeric() and x2_str.isnumeric() and y2_str.isnumeric():
        x1 = int(x1_str)
        y1 = int(y1_str)
        x2 = int(x2_str)
        y2 = int(y2_str)

        left_up_point = Point(x1, y1)
        right_down_point = Point(x2, y2)
        cutter.left_up_point = left_up_point
        cutter.right_down_point = right_down_point

        for segment in segment_list:
            segment_cut_off(segment.first_point, segment.second_point)


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

        first_point = Point(x1, y1)
        second_point = Point(x2, y2)
        segment = Segment(first_point, second_point)
        segment_list.append(segment)

        draw_line(main_image, main_canvas, x1, y1, x2, y2)
    else:
        messagebox.showerror("Ошибка!", "Введены некорректные данные")


def draw_line(image, canvas, x1=0, y1=0, x2=0, y2=0):
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


lineOptionsFrame = Frame(master=root)
lineOptionsFrame.place(x=10, y=10)

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

cutterOptionsPane = Frame(master=root)
cutterOptionsPane.place(x=10, y=100)

left_up_point_x_label = Label(master=cutterOptionsPane, text="X координата левого верхнего угла: ")
left_up_point_x_label.grid(row=0, column=0, padx=10, pady=10)
left_up_point_x_entry = Entry(master=cutterOptionsPane)
left_up_point_x_entry.grid(row=0, column=1, padx=10, pady=10)
left_up_point_y_label = Label(master=cutterOptionsPane, text="Y координата левого верхнего угла: ")
left_up_point_y_label.grid(row=1, column=0, padx=10, pady=10)
left_up_point_y_entry = Entry(master=cutterOptionsPane)
left_up_point_y_entry.grid(row=1, column=1, padx=10, pady=10)

right_down_point_x_label = Label(master=cutterOptionsPane, text="X координата правого нижнего угла: ")
right_down_point_x_label.grid(row=0, column=2, padx=10, pady=10)
right_down_point_x_entry = Entry(master=cutterOptionsPane)
right_down_point_x_entry.grid(row=0, column=3, padx=10, pady=10)

right_down_point_y_label = Label(master=cutterOptionsPane, text="Y координата правого нижнего угла: ")
right_down_point_y_label.grid(row=1, column=2, padx=10, pady=10)
right_down_point_y_entry = Entry(master=cutterOptionsPane)
right_down_point_y_entry.grid(row=1, column=3, padx=10, pady=10)

cut_button = Button(master=cutterOptionsPane, text="Вырезать", command=draw_cut_line_wrapper)
cut_button.grid(row=0, column=4, padx=10, pady=10)

main_canvas = Canvas(master=root, width=400, height=400, bg='white')
main_canvas.place(x=10, y=200)

cutter_canvas = Canvas(master=root, width=400, height=400, bg='white')
cutter_canvas.place(x=450, y=200)

main_canvas_clear_button = Button(master=root, text="Очистить", command=clear_main_canvas)
main_canvas_clear_button.place(x=10, y=610)

cutter_canvas_clear_button = Button(master=root, text="Очистить", command=clear_cutter_canvas)
cutter_canvas_clear_button.place(x=450, y=610)

root.mainloop()
