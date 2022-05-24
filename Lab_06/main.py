import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw

root = tk.Tk()
root.geometry('1300x700')

main_image = Image.new("RGB", (400, 400), (255, 255, 255))
main_photo = None
main_c_image = None
main_image_pix = None

gray_image = Image.new("RGB", (400, 400), (255, 255, 255))
gray_photo = None
gray_c_image = None
gray_image_pix = None
gray_image_draw = ImageDraw.Draw(gray_image)

bin_image = Image.new("RGB", (400, 400), (255, 255, 255))
bin_photo = None
bin_c_image = None
bin_image_draw = ImageDraw.Draw(bin_image)


def open_image_handler():
    file_name = fd.askopenfilename(filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png")))
    global main_image
    global main_photo
    global main_c_image
    global main_image_pix
    main_image = Image.open(file_name)
    main_image = main_image.resize((main_canvas.winfo_width(), main_canvas.winfo_height()), Image.ANTIALIAS)
    main_photo = ImageTk.PhotoImage(main_image)
    main_c_image = main_canvas.create_image(0, 0, anchor='nw', image=main_photo)
    main_image_pix = main_image.load()
    transform_image_button['state'] = 'active'


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def transform_image_handler():
    global gray_image
    global gray_photo
    global gray_c_image
    global gray_image_pix
    global gray_image_draw
    r_coeff_str = red_coeff_str.get()
    g_coeff_str = green_coeff_str.get()
    b_coeff_str = blue_coeff_str.get()
    if is_float(r_coeff_str) and is_float(g_coeff_str) and is_float(b_coeff_str):
        r_coeff = float(r_coeff_str)
        g_coeff = float(g_coeff_str)
        b_coeff = float(b_coeff_str)

        image_height, image_width = gray_image.size
        for i in range(image_height):
            for j in range(image_width):
                red, green, blue = main_image_pix[i, j]
                gray = round(r_coeff * red + g_coeff * green + b_coeff * blue)
                gray_image_draw.point((i, j), (gray, gray, gray))

        gray_photo = ImageTk.PhotoImage(gray_image)
        gray_c_image = gray_canvas.create_image(0, 0, anchor='nw', image=gray_photo)
        gray_image_pix = gray_image.load()
        bin_image_button['state'] = 'active'
    else:
        messagebox.showerror("Ошибка!", "Введены некорректные данные")


def find_treshold():
    global gray_image_pix
    image_height, image_width = gray_image.size
    size = 256
    intensity_histogram = [0] * size
    intensity_sum = 0

    for i in range(image_height):
        for j in range(image_width):
            intensity_histogram[gray_image_pix[i, j][0]] += 1
            intensity_sum += gray_image_pix[i, j][0]

    pixel_count = image_height * image_width
    best_threshold = 0
    max_sigma = 0.0
    first_class_pixel_count = 0
    first_class_intensity_sum = 0

    for threshold in range(size - 1):
        first_class_pixel_count += intensity_histogram[threshold]
        first_class_intensity_sum += threshold * intensity_histogram[threshold]

        if pixel_count - first_class_pixel_count == 0 or first_class_pixel_count == 0:
            continue

        first_class_prob = first_class_pixel_count / pixel_count
        second_class_prob = 1.0 - first_class_prob

        first_class_mean = first_class_intensity_sum / first_class_pixel_count
        second_class_mean = (intensity_sum - first_class_intensity_sum) / (pixel_count - first_class_pixel_count)

        mean_delta = first_class_mean - second_class_mean

        sigma = first_class_prob * second_class_prob * mean_delta * mean_delta

        if sigma > max_sigma:
            max_sigma = sigma
            best_threshold = threshold

    return best_threshold


def binarization():
    global bin_image
    global bin_photo
    global bin_c_image
    global gray_image
    global gray_image_pix
    global bin_image_draw

    image_height, image_width = bin_image.size
    treshold = find_treshold()

    for i in range(image_height):
        for j in range(image_width):
            if gray_image_pix[i, j][0] <= treshold:
                bin_image_draw.point((i, j), (0, 0, 0))
            else:
                bin_image_draw.point((i, j), (255, 255, 255))

    bin_photo = ImageTk.PhotoImage(bin_image)
    bin_c_image = bin_canvas.create_image(0, 0, anchor='nw', image=bin_photo)


optionFrame = Frame(master=root)
optionFrame.place(x=10, y=10)

red_coeff_str = tk.StringVar()
red_coeff_label = Label(master=optionFrame, text="Коэффициент красного:")
red_coeff_label.grid(row=0, column=0, padx=10, pady=10)
red_coeff_entry = Entry(master=optionFrame, textvariable=red_coeff_str)
red_coeff_entry.grid(row=1, column=0, padx=10, pady=10)
red_coeff_str.set("0.299")

green_coeff_str = tk.StringVar()
green_coeff_label = Label(master=optionFrame, text="Коэффициент зеленого:")
green_coeff_label.grid(row=0, column=1, padx=10, pady=10)
green_coeff_entry = Entry(master=optionFrame, textvariable=green_coeff_str)
green_coeff_entry.grid(row=1, column=1, padx=10, pady=10)
green_coeff_str.set("0.587")

blue_coeff_str = tk.StringVar()
blue_coeff_label = Label(master=optionFrame, text="Коэффициент голубого:")
blue_coeff_label.grid(row=0, column=2, padx=10, pady=10)
blue_coeff_entry = Entry(master=optionFrame, textvariable=blue_coeff_str)
blue_coeff_entry.grid(row=1, column=2, padx=10, pady=10)
blue_coeff_str.set("0.114")

open_image_button = Button(master=optionFrame, text="Открыть", command=open_image_handler)
open_image_button.grid(row=0, column=3, padx=10, pady=10)

transform_image_button = Button(master=optionFrame, text="Преобразовать", command=transform_image_handler)
transform_image_button.grid(row=1, column=3, padx=10, pady=10)
transform_image_button['state'] = 'disabled'

bin_image_button = Button(master=optionFrame, text="Биноризировать", command=binarization)
bin_image_button.grid(row=2, column=3, padx=10, pady=10)
bin_image_button['state'] = 'disabled'

main_canvas = Canvas(master=root, width=400, height=400, bg='white')
main_canvas.place(x=10, y=200)

gray_canvas = Canvas(master=root, width=400, height=400, bg='white')
gray_canvas.place(x=420, y=200)

bin_canvas = Canvas(master=root, width=399, height=399, bg='white')
bin_canvas.place(x=830, y=200)

root.mainloop()
