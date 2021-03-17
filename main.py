from tkinter import *
import random
import pandas
import time

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
IMAGE_CARD_FRONT = "card_front.png"
IMAGE_CARD_BACK = "card_back.png"

current_card = {}
data_dic = {}

# ---------------------  Read Data  -----------------------#
try:
    data = pandas.read_csv("data/french_words.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    data_dic = original_data.to_dict(orient="records")
else:
    data_dic = data.to_dict(orient="records")


# ---------------------  Change Data  -----------------------#
def nex_card():
    global current_card, timer
    window.after_cancel(timer)
    current_card = random.choice(data_dic)
    canvas.itemconfig(canvas_tile, text="French", fill="black")
    canvas.itemconfig(canvas_words, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front)
    timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(canvas_tile, text="English", fill="white")
    canvas.itemconfig(canvas_words, text=current_card["English"], fill="white")


def remove_data():
    nex_card()
    data_dic.remove(current_card)
    data_to_learn = pandas.DataFrame(data_dic)
    data_to_learn.to_csv("data/words_to_learn.csv", index=False)


# ---------------------  UI  -----------------------#
# Window
window = Tk()
window.title("Flashy")
window.minsize(width=800, height=600)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = window.after(3000, flip_card)

# Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
canvas_image = canvas.create_image(400, 264, image=card_front)
canvas.grid(row=0, column=0, columnspan=2)
canvas_tile = canvas.create_text(400, 150, text="Title", font=(FONT_NAME, 40, "italic"))
canvas_words = canvas.create_text(400, 263, text="word", font=(FONT_NAME, 60, "bold"))


# Buttons
image_button_right = PhotoImage(file="images/right.png")
button_right = Button(image=image_button_right, highlightthickness=0, command=remove_data)
button_right.grid(row=1, column=1)
image_button_wrong = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=image_button_wrong, highlightthickness=0, command=nex_card)
button_wrong.grid(row=1, column=0)

nex_card()

window.mainloop()
