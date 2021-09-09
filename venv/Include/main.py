from tkinter import Tk
import tkinter as tk
from PIL import Image, ImageTk
import functions


def main_window():
    """Строит главное окно."""
    root = Tk()
    root.title('Распознавание голоса')
    root.resizable(False, False)
    root.width = root.winfo_screenwidth() // 2
    root.height = root.winfo_screenheight() // 2
    root.geometry('600x400+{}+{}'.format(root.width-400, root.height-400))
    image = Image.open('repeat.png')
    image.thumbnail((25, 25), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    repeat = tk.Button(root, image=image, command=functions.repeat_cmd)
    repeat.place(x=550, y=350)
    repeat.config(width=25, height=25)
    button = tk.Button(root, text="Говорите", font='arial 14', command=functions.recording_1)
    button.place(x=260, y=190)
    root.mainloop()


main_window()