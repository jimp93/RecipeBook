import tkinter as tk
from tkinter import *
import sqlite3
import shelve
import webbrowser
import os


osCommandString = "notepad.exe /Users/james/Documents/recipeglitches.txt"
os.system(osCommandString)

# def callback(event, jeff):
#     if jeff[:4] == "http":
#         webbrowser.open_new(jeff)
#     else:
#         link1 = Label(root, text=jeff, fg="blue", cursor="hand2")
#         link1.pack()
#
#
# def make_button(**args):
#     jeff = args['one']
#     link = Label(root, text="link", fg="blue", cursor="hand2")
#     link.pack()
#     link.bind("<Button-1>", lambda event, jeff=jeff: callback(event, jeff))
#
# def get_box(e):
#     dicto = {}
#     s = e.get()
#     dicto['one'] = s
#     make_button(**dicto)
#
#
# def make_box():
#     e = Entry(root)
#     e.pack()
#     b = Button(root, command= lambda: get_box(e))
#     b.pack()
#
#
# # link = Label(root, text="Google Hyperlink", fg="blue", cursor="hand2")
# # link.pack()
# # link.bind("<Button-1>", callback)
# root = Tk()
# make_box()
# root.mainloop()