import tkinter as tk
from tkinter import *

def vp_start_gui():
    global app
    app = MenuQ()
    app.mainloop()

class MenuQ(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        f = tk.Label(text = "dog")
        f.pack()
        self.checker()

    def checker(self):
        g= tk.Button(self, text="Back to homepage",
                                  command= refresh)
        g.pack()


if __name__ == '__main__':
    def refresh():
        app.destroy()
        vp_start_gui()

vp_start_gui()
