import tkinter as tk
from tkinter import *
import sqlite3
import shelve
import random
import webbrowser
from PIL import ImageTk, Image
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def make_tables():
    conn = sqlite3.connect('master.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS RecipeList (
        meal text,
        link text,
        MainIngredient text,
        expense text,
        PrepTime text
        )""")
    conn.commit()

    c.execute("""SELECT meal FROM RecipeList""")
    start_up_rl_checker = c.fetchall()

    if len(start_up_rl_checker) == 0:
        start_options_dict = {'MainIngredient': {'beef', 'pork', 'vegetables', 'seafood',
                                                 'pasta', 'lamb', 'fish', 'chicken'},
                              'expense': {'cheap', 'normal', 'expensive'},
                              'PrepTime': {'quick','normal', 'long time'}}
        s = shelve.open('test_shelf.db')
        s['key1'] = start_options_dict

        title_holder_dict = {'Meal': 'Meal Name', 'link': 'Link/Reminder', 'MainIngredient': 'Main Ingredient',
                             'expense': 'Expense','PrepTime': 'Prep Time'}
        s = shelve.open('test_shelf.db')
        s['title_holder'] = title_holder_dict

        default_dict = {'MainIngredient': {'Any': 1}, 'expense': {'Any': 1},
                             'PrepTime': {'Any': 1}}
        s = shelve.open('test_shelf.db')
        s['default_holder'] = default_dict

        c.execute("""INSERT INTO RecipeList VALUES  (?, ?, ?, ?, ?
            )""", ("EnterRecipe", "EnterRecipe", "EnterRecipe", "EnterRecipe", "EnterRecipe"))
        conn.commit()

    c.close()
    conn.close()


make_tables()


def slicer(n):
    return n[1:]


conn = sqlite3.connect('master.db')
c = conn.cursor()
criteria = {}
recipe_dict = {}
cursor = conn.execute('select * FROM RecipeList')
customised_rows = list(map(lambda x: x[0], cursor.description))
conn.close()
count = len(customised_rows)
customised_rows_low = [x.lower() for x in customised_rows]
abbrev_customised_rows = map(slicer, customised_rows_low)
custom_dict = dict(zip(abbrev_customised_rows, customised_rows))
for i in customised_rows_low:
    recipe_dict[i] = ''
erht_master = int(screensize[1] * 0.4)
erht_inside = int(erht_master / 6)
wid=int(screensize[0]*2/3)
hei=int(screensize[1]*2/3)
xxx = int(screensize[0]*1/6)
yyy = int(screensize[1]*1/6)
# diary_wid = int(screensize[0]*2/3)
# diary_height = int(diary_wid*.8)
diary_wid = int(screensize[0]*15/28)
diary_height = int(diary_wid*.8)
diary_x=int(screensize[0]*0.28)
diary_y=int(screensize[1]*0.1)
LARGE_FONT = ("Courier", 12)

def vp_start_gui():
    global app
    app = MenuQ()
    app.state('zoomed')
    app.mainloop()


if __name__ == '__main__':
    def refresh():
        global app
        app.destroy()
        vp_start_gui()


class MenuQ(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        master = tk.Frame()
        self.title('CHOP CHOP')
        master.pack(side="top", fill="both", expand=True)
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, RecipeBookStartPage, CustomSearch, AmendRecipe, AddRecipe, DeleteRecipe,
                  PlannerStartPage, CustomPlan, AddColumn, DeleteColumn, AddDefault, AddDeleteOption):
            frame = F(master, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage, master)

    def show_frame(self, cont, master):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        photo = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
        w = Label(self, image=photo)
        w.image = photo
        w.place(x=0, y=0, relwidth=1, relheight=1)
        self.lbutt16=ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((int(screensize[1] / 16), int(screensize[1] / 16))))
        self.lwbutt16 = ImageTk.PhotoImage \
            (Image.open("lwbutt.png").resize((int(screensize[1] / 16), int(screensize[1] / 16))))
        self.null_cells = {}
        self.st_list_of_widgets = []
        self.three_labs =[]
        self.st1_list_of_widgets = []
        self.st2_list_of_widgets = []
        self.placew = int(screensize[0] * 3 / 8)
        self.placeh = int(screensize[1] / 3)
        self.wid = int(screensize[0] / 4)
        self.he = int(screensize[1] / 3)
        self.test_for_nulls(parent, controller)

    def test_for_nulls(self, parent, controller):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        cursor = conn.execute('select * FROM RecipeList')
        cols = list(map(lambda x: x[0], cursor.description))
        cols_1 = cols[1:]
        c.execute('select meal from RecipeList')
        mealer = c.fetchall()
        if mealer[0][0] == "EnterRecipe":
            self.get_started(parent, controller)
        else:
            for col in cols_1:
                sq = "select meal FROM RecipeList WHERE " + col + " IS NULL"
                c.execute(sq)
                blank_meals = c.fetchall()
                if len(blank_meals) != 0:
                    blank_meals_l = [item for t in blank_meals for item in t]
                    self.null_cells[col] = blank_meals_l
                    self.null_cells = {k: v for k, v in self.null_cells.items()}
            conn.close()

            if len(self.null_cells) == 0:
                self.get_started(parent, controller)
            else:
                self.frmx1 = Frame(self, bg='black', width=self.wid, height=.75*self.he)
                self.frmx1.place(relx=.5, y=self.placeh-(0.25*self.placeh), anchor = 'center')

                self.frmx2 = Frame(self, bg='black', width=1.5*self.wid, height=0.5*self.he)
                self.frmx2.place(relx=.5, y=self.placeh - (0.5 * self.placeh), anchor='center')


                null_label = tk.Label(self.frmx2, text="You have some blank values"
                                                       +"\n" + "fill them in and get started!",
                                      fg = 'green', bg = 'black', font = ("Courier", int(screensize[0] / 80)))
                null_label.place(relx=.5, rely=0.5, anchor="center")

                self.fill_lb = tk.Label(self.frmx1, text='FILL IN THE BLANKS', fg='red',
                                            bg='black', font=("Courier", int(screensize[0] / 70)))
                self.fill_lb.place(relx=.5, rely=0.59, anchor="center")

                null_button1 = tk.Button(self.frmx1, text="Fill in the blanks", image=self.lbutt16,
                                           borderwidth=0, highlightthickness=0, command=lambda: self.destroy_create())
                null_button1.place(relx=.5, rely=0.81, anchor="center")
                null_button1.image = self.lbutt16

                self.st1_list_of_widgets.append(self.fill_lb)
                self.st1_list_of_widgets.append(null_button1)
                self.st1_list_of_widgets.append(self.frmx2)
                self.st1_list_of_widgets.append(null_label)
                self.st2_list_of_widgets.append(self.frmx1)

    def destroy_create(self):
        self.frmx = Frame(self, bg='black', width=self.wid, height=self.he)
        self.frmx.place(relx=.5, y=self.placeh+(0.5*self.placeh), anchor = 'center')
        for widget in self.st_list_of_widgets:
            widget.destroy()
        for widget in self.st2_list_of_widgets:
            widget.destroy()
        for category in self.null_cells:
            for meal in self.null_cells[category]:
                self.make_st_widgets(meal, category)
        for widget in self.st1_list_of_widgets:
            widget.destroy()
        for widget in self.three_labs:
            widget.destroy()
        self.dc_meal_lb = tk.Label(self.frmx, text="Book updated", fg='green',
                                        bg='black', font=("Courier", int(screensize[0] / 70)))
        self.dc_meal_lb.place(relx=.5, rely=0.15, anchor="center")

        self.dc_meal_lb2 = tk.Label(self.frmx, text='BACK TO HOMEPAGE', fg='red',
                                    bg='black', font=("Courier", int(screensize[0] / 70)))
        self.dc_meal_lb2.place(relx=.5, rely=0.59, anchor="center")


        self.dc_button = tk.Button(self.frmx, text="Back to Homepage", image = self.lbutt16,
                                       borderwidth = 0, highlightthickness = 0, command=refresh)
        self.dc_button.place(relx=.5, rely=0.81, anchor="center")
        self.dc_button.image = self.lbutt16

        self.st1_list_of_widgets.append(self.dc_meal_lb)
        self.st1_list_of_widgets.append(self.dc_meal_lb2)
        self.st1_list_of_widgets.append(self.dc_button)
        self.st1_list_of_widgets.append(self.frmx)

    def make_st_widgets(self, meal, category):
        self.meal_cat_lb = tk.Label(self.frmx, text=meal, fg = 'green',
                                   bg = 'black', font = ("Courier", int(screensize[0] / 70)))
        self.meal_cat_lb.place(x=(self.wid/2), y=(self.he*2/20),anchor='center')

        self.meal_cat_lb1 = tk.Label(self.frmx, text=category, fg='white',
                                   bg='black', font=("Courier", int(screensize[0] / 70)))
        self.meal_cat_lb1.place(x=(self.wid/2), y=(self.he*5/20), anchor='center')

        self.var = StringVar()
        s = shelve.open('test_shelf.db')
        opto_stage = s['key1']
        if category == 'link':
            self.linker = Entry(self.frmx, textvariable=self.var, font=('Courier', int(screensize[1]/ 70)))
            self.linker.place(relx=.5, y=(self.he*9/20), anchor = 'center')
            self.three_labs.append(self.linker)
        else:
            self.optos = opto_stage[category]
            self.st_box = OptionMenu(self.frmx, self.var, *self.optos)
            self.st_box.config(bg='white', font=("Courier", int(screensize[0] / 70)))
            menu = self.nametowidget(self.st_box.menuname)
            menu.config(fg='black', font=("Courier", int(screensize[0] / 90)))
            self.st_box.place(relx=.5, y=(self.he*9/20), anchor = 'center')
        swait_var = tk.IntVar()

        self.meal_snd_lb1 = tk.Label(self.frmx, text='SEND', fg='red',
                                     bg='black', font=("Courier", int(screensize[0] / 70)))
        self.meal_snd_lb1.place(x=(self.wid / 2), y=(self.he * 14/ 20), anchor='center')

        self.st_button = tk.Button(self.frmx, text="Send",
                                   image=self.lbutt16, borderwidth=0, highlightthickness=0,
                                   command=lambda: swait_var.set(1))
        self.st_button.place(relx=.5, y=(self.he*17/20), anchor = 'center')
        self.st_button.image = self.cbuttimgr
        swait_var = tk.IntVar()
        self.st_button.wait_variable(swait_var)
        self.three_labs.append(self.meal_cat_lb)
        self.st1_list_of_widgets.append(self.meal_snd_lb1)
        self.three_labs.append(self.meal_cat_lb1)
        self.three_labs.append(self.st_box)
        self.st1_list_of_widgets.append(self.st_button)
        self.s_updater(meal, category)

    def s_updater(self, meal, category):
        for widget in self.three_labs:
            widget.destroy()
        option_choice = self.var.get()
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute("UPDATE RecipeList SET " + category + " = (?) "
                                                                   "WHERE meal = (?)", (option_choice, meal))
        conn.commit()
        conn.close()

    def get_started(self, parent, controller):
        yex = int(screensize[0]/8)
        img = ImageTk.PhotoImage(Image.open("RB1.png").
                                 resize ((int(screensize[0] * .15), int(screensize[0] / 6.5))))
        button1 = tk.Button(self, text="Recipe Book", image=img,
                            command=lambda: controller.show_frame(RecipeBookStartPage, parent))
        button1.place(x= int(screensize[0]/4), y = int(screensize[1]*.36666))
        button1.image = img
        img2 = ImageTk.PhotoImage(Image.open("diary1.png").
                                  resize((int(screensize[0] * .15), int(screensize[0] / 6.5))))
        label = tk.Label(self, image=img)
        label.image = img2
        button2 = tk.Button(self, text="Planner", image=img2,
                            command=lambda: controller.show_frame(PlannerStartPage, parent))
        button2.place(x=int((screensize[0] * 5) / 8), y=int(screensize[1] * .3666))

        photo1= ImageTk.PhotoImage(Image.open("tit.png").resize
                                   ((int(screensize[0] * 0.44), int(screensize[0] * .14))))
        w1 = Label(self, image=photo1)
        w1.image = photo1
        w1.place(x=int(screensize[0] * 0.21), y=int(screensize[1] * 0.025))

        photo2 = ImageTk.PhotoImage(Image.open("logo.png").resize
                                    ((int(screensize[0] * 0.14), int(screensize[0] * .14))))
        w2 = Label(self, image=photo2)
        w2.image = photo2
        w2.place(x=int(screensize[0] * 0.65), y=int(screensize[1] * 0.025))

        frin = Frame(self, bg='white',
                          width=int(screensize[0]*.14), height=int(screensize[0]*0.08))
        frin.place(x=int(screensize[0]*.45), y=int(screensize[1]*0.7))
        inlab = tk.Label(frin, text='HOW TO USE', fg='black',
                                     bg='white', font=("Courier", int(screensize[0] / 70)))
        inlab.place(relx=0.1, rely=0.05)

        button3 = tk.Button(frin, text="Instructions", image=self.lwbutt16, borderwidth = 0,
                                highlightthickness = 0, command=self.instructions)
        button3.place(relx=0.35, rely = 0.4)
        button3.image = self.lwbutt16

    def instructions(self):
        instr = tk.Toplevel()
        instr.geometry('{}x{}+{}+{}'.format((int(screensize[0]*.85)), (int(screensize[1]*.85)),
                                            (int(screensize[0] *.1)), (int(screensize[1]*.05))))
        frm_instr = Frame(instr, bg='black',
                          width=int(screensize[0]), height=int(screensize[1]))
        frm_instr.place(x=0)
        frmi_instr = Frame(frm_instr, bg='black', width=(int(screensize[0]*.85)), height = (int(screensize[1]*.85)))
        frmi_instr.place(x=0)
        self.ne_label2 = tk.Label(frmi_instr,
        text="CHOP CHOP IS A RECIPE BOOK AND STRESS-FREE WEEKLY MENU PLANNER.""\n"
        "BOTH CAN BE ACTIVATED WITH ONE CLICK, OR HIGHLY PERSONALISED TO CATER FOR YOUR DAILY NEEDS""\n""\n",
                                  fg='green', bg='black', wraplength=1100, justify= 'left',
                                  font=("Courier", int(diary_height / 45)))
        self.ne_label2.pack()

        self.ne_label3 = tk.Label(frmi_instr,text="Recipe Book:""\n"
          "    The recipe book allows you to keep all your favourite meals in one place, and is easy to view and update by"
          " clicking" "\n" "    on the recipe book icon on the welcome page and use the following buttons...""\n""\n"
          "    ONE-CLICK RECIPE BOOK - Shows you all your recipes, with weblinks/reminders.""\n"                                 
          "    PERSONALISED RECIPE BOOK - Allows you to filter your recipes by various SEARCH OPTIONS. For instance,"
          "if you only want" "\n" "        to see your chicken meals, select SEARCH OPTION 'chicken' from the SEARCH CATEGORY 'Main Ingredient'.""\n"                                              
          "    ADD RECIPE - Chop Chop will ask you for the name of the new meal and a weblink/reminder of where to find the recipe.""\n"
          "        It will also ask you to tag the meal with the SEARCH OPTIONS.""\n"
          "    DELETE RECIPE and  CHANGE RECIPE - are hopefully self-explanatory!""\n"                                        
          "    ADD SEARCH CATEGORY - Chop Chop comes with three 'SEARCH CATEGORIES'; Main Ingredient, Expense, and Preparation Time.""\n"
          "        But you can personalise your book by adding your own. "
            "For example, you could create an 'Allergies' SEARCH""\n""        CATEGORY and use it to filter out meals tagged with the "
                                                  "'dairy' and 'gluten' SEARCH OPTIONS."  "\n"                                
          "    DELETE SEARCH CATEGORY - If you want to keep it really basic, or don't need any of the SEARCH CATEGORIES, "
                                                  "delete them""\n" "        with this button.""\n"                                   
          "    ADD/DELETE OPTION - You can even go into each SEARCH CATEGORY and tailor them to your needs by adding or"
                                                  " deleting""\n" "        SEARCH OPTIONS." "\n",
                                  fg='white', bg='black', wraplength=1100, justify= 'left',
                                  font=("Courier", int(diary_height / 55)))
        self.ne_label3.pack()
        self.ne_label4 = tk.Label(frmi_instr, text="Weekly Planner:""\n"
           "    The weekly planner uses your recipe book to generates a meal for each day of the week,"
             " making sure you never forget" "\n" "    about any of your dishes.""\n""\n"
            "    ONE-CLICK PLAN -  Creates an instant plan using seven random meals from your recipe book.""\n"
            "    PERSONALISED PLAN - Allows you to specify your needs for every day of the weekly plan ""\n"
            "    ADD/CHANGE DEFAULT - Allows you to add a default SEARCH OPTIONS for each SEARCH CATEGORY, "
                "meaning your planner will" "\n" "        "
                                                   "only suggest recipes tagged with those options, unless overridden by the Personalised Plan.""\n"
           "        For example, if you generally only want vegetarian meals, set the 'MAIN INGREDIENT' search category to the "
             "\n""        'VEGETABLE' option, and use the PERSONALISED PLAN if you want meat on a certain day.""\n"
            "        You can also make the default 'ANYTHING BUT' a certain SEARCH OPTION, means=ing the planner will ignore "
             "all ""\n""        recipes tagged with that option. ""\n"
             "        For example, if you don’t generally want 'EXPENSIVE' meals, select that SEARCH OPTION and the untick "
             "the""\n" "        'ANYTHING BUT' box.""\n""\n"
             "BON APPETIT!!!", fg='red', bg='black', wraplength=1100, justify='left',
                                  font=("Courier", int(diary_height / 55)))
        self.ne_label4.pack()

class PlannerStartPage (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        photo = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
        w = Label(self, image=photo)
        w.image = photo
        w.place(x=0, y=0, relwidth=1, relheight=1)
        self.ryes_dict = {}
        self.ryes1_dict = {}
        self.rno_dict = {}
        self.rno1_dict = {}
        self.rmeal_list_after_def = []
        self.rto_zip = []
        self.rdefault_dict = {}
        self.rdef_dict = {}
        self.random_template = {}
        self.full_list = []
        self.random_search_widgets = []
        self.rset_of_meals = []
        self.link_dict = {}
        self.ranlink_full = {}
        self.lbutt8 = ImageTk.PhotoImage \
                (Image.open("lbutt.png").resize(
                (int(screensize[1] / 8), int(screensize[1] / 8))))
        self.lwbutt8 = ImageTk.PhotoImage \
                (Image.open("lwbutt.png").resize(
                (int(screensize[1] / 8), int(screensize[1] / 8))))
        self.make_widges(controller, 0, parent)

    def make_widges(self, controller, x, parent):
        widt_master = int(screensize[0] * 0.4)
        widt_inside = int(widt_master / 2)
        ht_master = int(screensize[1] * 0.4)
        ht_inside = int(ht_master / 6)
        ht_butt = int(ht_master * 2)

        frm = Frame(self, bg='black', width=widt_master, height=ht_master)
        frm.place(x=int(screensize[0] * 0.35), y=int(screensize[1] * 0.1))

        frmb = Frame(self, bg='black', width=widt_master / 3, height=ht_inside * 1.75)
        frmb.place(x=int((screensize[0] * 0.35) + (.65*widt_inside)), y=int(screensize[1] * 0.1) + ht_master)

        frm1 = Frame(frm, bg='black', width=widt_inside, height=ht_inside)
        frm1.place(x=0, y=0)

        frm2 = Frame(frm, bg='black', width=widt_inside, height=ht_inside)
        frm2.place(x=widt_inside, y=0)

        frm3 = Frame(frm, bg='black', width=widt_inside, height=ht_inside * 2)
        frm3.place(x=0, y=ht_inside)

        frm4 = Frame(frm, bg='black', width=widt_inside, height=ht_inside * 2)
        frm4.place(x=widt_inside, y=ht_inside)

        frm5 = Frame(frm, bg='black', width=widt_inside, height=ht_inside)
        frm5.place(x=0, y=ht_inside*3)

        frm6 = Frame(frm, bg='black', width=widt_inside, height=ht_inside)
        frm6.place(x=0, y=ht_inside*4)

        self.lbutthi=ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((ht_inside, ht_inside)))

        lab1 = Label(frm1, fg='green', bg='black', text="ONE-CLICK PLAN", font=("Courier", int(ht_inside / 5)))
        lab1.place(relx=.5, rely=.5, anchor="center")

        lab2 = Label(frm2, fg='green', bg='black', text="PERSONALISED PLAN", font=("Courier", int(ht_inside / 5)))
        lab2.place(relx=.5, rely=.5, anchor="center")

        lab5 = Label(frm5, fg='white', bg='black', text="ADD/CHANGE DEFAULT",
                     font=("Courier", int(ht_inside / 5)))
        lab5.place(relx=.5, rely=.5, anchor="center")


        ps_button = tk.Button(frm3, text="Random planner", image = self.lbutthi, borderwidth = 0,
                              highlightthickness = 0, command=lambda: self.random_opener(controller, parent))
        ps_button.place(relx=.5, rely=0.3, anchor="center")
        ps_button.image = self.lbutthi

        ps2_button = tk.Button(frm4, text="Custom planner", image = self.lbutthi, borderwidth = 0, highlightthickness = 0,
                               command=lambda: controller.show_frame(CustomPlan, parent))
        ps2_button.place(relx=.5, rely=0.3, anchor="center")
        ps2_button.image = self.lbutthi

        add_default_button = tk.Button(frm6, text="Add or change a default value",
                                       image = self.lbutthi, borderwidth = 0, highlightthickness = 0,
                                      command=lambda: controller.show_frame(AddDefault, parent))
        add_default_button.place(relx=.5, rely=0.5, anchor="center")
        add_default_button.image = self.lbutthi

        lab7 = Label(frmb, fg='red', bg='black', text="BACK TO HOMEPAGE", font=("Courier", int(ht_inside / 5)))
        lab7.place(relx=.5, rely=0.15, anchor="center")

        back_button = tk.Button(frmb, text="Back to homepage", image = self.lbutthi, borderwidth = 0,
                                highlightthickness = 0, command=lambda: self.sweeper_upper(controller, parent))
        back_button.place(relx=.5, rely=.6, anchor="center")
        back_button.image = self.lbutthi

        self.random_search_widgets.append(ps_button)
        self.random_search_widgets.append(frm)
        self.random_search_widgets.append(frmb)
        self.random_search_widgets.append(frm1)
        self.random_search_widgets.append(frm2)
        self.random_search_widgets.append(frm3)
        self.random_search_widgets.append(frm4)
        self.random_search_widgets.append(frm5)
        self.random_search_widgets.append(frm6)
        self.random_search_widgets.append(lab1)
        self.random_search_widgets.append(lab2)
        self.random_search_widgets.append(lab5)
        self.random_search_widgets.append(lab7)
        self.random_search_widgets.append(ps2_button)
        self.random_search_widgets.append(back_button)
        self.random_search_widgets.append(add_default_button)
        if x == 1:
            controller.show_frame(StartPage, parent)

    def sweeper_upper(self, controller, parent):
        for widget in self.random_search_widgets:
            widget.destroy()
        self.make_widges(controller, 1, parent)

    def random_opener(self, controller, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute('select meal from RecipeList')
        tester_value = c.fetchall()
        ex_tester = [i for word in tester_value for i in word]
        conn.close()
        if ex_tester == ['EnterRecipe']:
            ran_em_win = tk.Toplevel()
            ran_em_win.title("Empty Plan Results")
            ran_em_win.geometry('{}x{}+{}+{}'.format(wid, hei, xxx, yyy))
            frm60 = Frame(ran_em_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            frm60.place(x=0)
            frm7 = Frame(frm60, bg='black', width=int(screensize[0] * 2 / 3), height=int(screensize[1] * 2 / 3))
            frm7.place(x=0, y=0)
            ran_empty = Label(frm7, fg='green', bg='black', text="ENTER A RECIPE FIRST",
                                   font=("Courier", int(erht_inside)))
            ran_empty.place(relx=0.5, rely=0.25, anchor ="center")
            ran_cl = Label(frm7, fg='white', bg='black', text="CLOSE WINDOW",
                                   font=("Courier", int(erht_inside)))
            ran_cl.place(relx=0.5, rely=0.5, anchor ="center")

            ran_em_button_m = tk.Button(frm7, text="Close Window", image=self.lbutt8,
                                        borderwidth=0, highlightthickness=0,  command=ran_em_win.destroy)
            ran_em_button_m.place(relx=0.5, rely=0.75, anchor ="center")
            ran_em_button_m.image = self.lbutt8


        else:
            self.random_template = {'Monday': '', 'Tuesday': '', 'Wednesday': '', 'Thursday': '',
                               'Friday': '', 'Saturday': '', 'Sunday': ''}
            self.rmake_default_dict()

    def rmake_default_dict(self):
        holder_list = []
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        s = shelve.open('test_shelf.db')
        self.rdefault_dict = s['default_holder']
        self.rdef_dict = self.rdefault_dict
        for citem in self.rdef_dict:
            for opt in self.rdef_dict[citem]:
                if opt == 'Any':
                    holder_list.append(citem)
        for hitem in holder_list:
            del self.rdef_dict[hitem]
        for citem in self.rdef_dict:
            for opt in self.rdef_dict[citem]:
                if self.rdef_dict[citem][opt] == 1:
                    self.ryes_dict[citem] = self.rdef_dict[citem]
                if self.rdef_dict[citem][opt] == 0:
                    self.rno_dict[citem] = self.rdef_dict[citem]
        abc = 0
        for yitem in self.ryes_dict:
            ygap = (map(list, self.ryes_dict.values()))
            ygap1 = (list(ygap))
            ygap2 = ygap1[abc]
            abc += 1
            self.ryes1_dict[yitem] = ygap2[0]
        self.ryes_dict = self.ryes1_dict
        xyz = 0
        for nitem in self.rno_dict:
            ngap = (map(list, self.rno_dict.values()))
            ngap1 = (list(ngap))
            ngap2 = ngap1[xyz]
            xyz += 1
            self.rno1_dict[nitem] = ngap2[0]
        self.rno_dict = self.rno1_dict
        for key in self.ryes_dict:
            rvaly = self.ryes_dict[key]
            c.execute("select meal from RecipeList WHERE " + key + "=?", (rvaly,))
            ryes = c.fetchall()
            self.rmeal_list_after_def.append(ryes)
        for key in self.rno_dict:
            rvaln = self.rno_dict[key]
            c.execute("select meal from RecipeList WHERE " + key + "!=?", (rvaln,))
            rno = c.fetchall()
            self.rmeal_list_after_def.append(rno)

        exploded_def_meals = ([item for t in self.rmeal_list_after_def for item in t])
        self.rset_of_meals=set(exploded_def_meals)
        exp = [i[0] for i in self.rset_of_meals]
        expo = str(exp)
        if len(self.rset_of_meals) != 0 and len(self.rset_of_meals) < 7:
            ln = len(self.rset_of_meals)
            sln = str(ln)
            short = 7-ln
            sshort = str(short)
            rand_win2 = tk.Toplevel()
            rand_win2.geometry('{}x{}+{}+{}'.format(int(diary_wid*1.5), int(diary_height*1.2),
                                                    int(diary_x*0.3), int(diary_y*0.25)))
            rand2 = Frame(rand_win2, bg='black',
                              width=int(screensize[0]), height=int(screensize[1]))
            rand2.place(x=0)
            randi2 = Frame(rand2, bg='black', width=int(diary_wid*1.5), height=int(diary_height*1.2))
            randi2.place(x=0)
            self.r_label2 = tk.Label(randi2,
                                      text="Only " + sln + " meals fit the bill, " "\n" + expo + "\n"
                                                " change default or use custom search for " + sshort + " meals",
                                      fg='white', bg='black',  wraplength=1410, justify='left',
                                     font=("Courier", int(diary_height / 30)))
            self.r_label2.place(relx=0, rely=0.1)
            rnad_button_ta2 = tk.Button(randi2, text="Close Window", image=self.lbutt8,
                                        borderwidth=0, highlightthickness=0, command=rand_win2.destroy)
            rnad_button_ta2.place(relx=0.48, rely=0.75)
            rnad_button_ta2.image = self.lbutt8
            conn.close()
        if len(self.rset_of_meals) != 0 and len(self.rset_of_meals) > 6:
            conn.close()
            self.rcalc_results(**self.random_template)
        if len(self.rset_of_meals) == 0:
            c.execute('select meal from RecipeList')
            self.rset_of_meals = c.fetchall()
            self.rcalc_results(**self.random_template)
            conn.close()


    def rcalc_results(self, **kwargs):
        rand_exploded_raw_meal_list = [i[0] for i in self.rset_of_meals]
        rand_existing_meals = list(kwargs.values())
        self.rand_final_meal_list = [x for x in rand_exploded_raw_meal_list if x not in rand_existing_meals]
        self.rpop_upper(**kwargs)

    def rpop_upper(self, **kwargs):
        colourd=['red', 'black', 'green','red', 'black', 'green','red']
        ccount=0
        diary_win = tk.Toplevel()
        for k, v in kwargs.items():
            if not v:
                kwargs[k] = random.choice(self.rand_final_meal_list)
            if kwargs[k] in self.rand_final_meal_list:
                self.rand_final_meal_list.remove(kwargs[k])
        diary_win.title("Random Plan Results")
        diary_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
        frmd = Frame(diary_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
        frmd.place(x=0)
        frmdi = Frame(frmd, bg='black', width=diary_wid, height=diary_height)
        frmdi.place(x=0, y=0)
        left_y_count =1
        right_y_count=1
        dir_pic = ImageTk.PhotoImage \
            (Image.open("diary.png").resize((diary_wid, diary_height)))
        dim = Label(frmdi, image=dir_pic)
        dim.image = dir_pic
        dim.place(x=0, y=0, relwidth=1, relheight=1)
        for key in kwargs:
            jeff = kwargs[key]
            self.ranlink_full[key] = Label(frmdi, text=jeff, fg='black',
            bg = 'white', font = ("Courier", int(diary_height/40)), cursor="hand2")
            self.ranlink_full[key].bind("<Button-1>", lambda event,
                                                             key = key, jeff=jeff: self.ranlink_open(event, jeff, key))
            if left_y_count<8:
                self.ranlink_full[key].place(x=diary_wid*0.05, y = int(diary_height/8)*left_y_count)
                left_y_count+=2
                ccount+=1
            else:
                self.ranlink_full[key].place(x=diary_wid*.55, y=int(diary_height / 8) * right_y_count)
                right_y_count += 2
                ccount+=1
        ran_lab = Label(frmdi, fg='red', bg='white', text="CLOSE WINDOW",
                       font=("Courier", int(diary_height/45)))
        ran_lab.place(x=diary_wid*.68, y=int(diary_height*25/ 32))

        ran_pl_button_m = tk.Button(frmdi, text="Close Window", image=self.lwbutt8,
                                    borderwidth=0, highlightthickness=0, command=diary_win.destroy)
        ran_pl_button_m.place(x=diary_wid*.70, y=int(diary_height*26.5/ 32))
        ran_pl_button_m.image = self.lwbutt8

    def ranlink_open(self, event, jeff, key):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute("select link from RecipeList WHERE meal =?", (jeff,))
        ln = c.fetchall()
        conn.close()
        ln1 = [item for t in ln for item in t]
        if ln1[0][:4] == "http":
            webbrowser.open_new(ln1[0])
        else:
            self.ranlink_full[key]['text'] = jeff + " - " + ln1[0]


class RecipeBookStartPage (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        photo = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
        w = Label(self, image=photo)
        w.image = photo
        w.place(x=0, y=0, relwidth=1, relheight=1)
        n = self
        widt_master = int(screensize[0]*0.6)
        widt_inside = int(widt_master/3)
        ht_master = int(screensize[1]*0.6)
        ht_inside = int(ht_master/9)
        ht_butt = int(ht_master*2)
        self.flink_full = {}

        frm = Frame(self, bg='black', width=widt_master, height=ht_master)
        frm.place(x=int(screensize[0]*0.2), y=int(screensize[1]*0.1))

        frmb = Frame(self, bg='black', width=widt_master/3, height=ht_inside*1.75)
        frmb.place(x=int((screensize[0] * 0.2)+widt_inside), y=int(screensize[1] * 0.1)+ht_master)

        frm1 = Frame(frm, bg='black', width=widt_inside, height=ht_inside)
        frm1.place(x=0, y=0)

        frm2 = Frame(frm, bg='black', width=widt_inside, height=ht_inside)
        frm2.place(x=widt_inside, y=0)

        frm3 = Frame(frm, bg='black', width=widt_inside, height=ht_inside)
        frm3.place(x=widt_inside*2, y=0)

        frm4 = Frame(frm, bg='black', width=widt_inside, height=ht_inside*2)
        frm4.place(x=0, y=ht_inside)

        frm5 = Frame(frm, bg='black', width=widt_inside, height=ht_inside*2)
        frm5.place(x=widt_inside, y=ht_inside)

        frm6 = Frame(frm, bg='black', width=widt_inside, height=ht_inside*2)
        frm6.place(x=widt_inside * 2, y=ht_inside)

        frm7 = Frame(frm, bg='black', width=widt_inside, height=ht_inside)
        frm7.place(x=0, y=ht_inside*3)

        frm8 = Frame(frm, bg='black', width=widt_inside, height=ht_inside)
        frm8.place(x=widt_inside, y=ht_inside*3)

        frm9 = Frame(frm, bg='black', width=widt_inside, height=ht_inside)
        frm9.place(x=widt_inside*2, y=ht_inside*3)

        frm10 = Frame(frm, bg='black', width=widt_inside, height=ht_inside*2)
        frm10.place(x=0, y=ht_inside*4)

        frm11 = Frame(frm, bg='black', width=widt_inside, height=ht_inside*2)
        frm11.place(x=widt_inside, y=ht_inside*4)

        frm12 = Frame(frm, bg='black', width=widt_inside, height=ht_inside*2)
        frm12.place(x=widt_inside * 2, y=ht_inside*4)

        frm13 = Frame(frm, bg='black', width=widt_inside, height=ht_inside)
        frm13.place(x=0, y=ht_inside*6)

        frm14 = Frame(frm, bg='black', width=widt_inside, height=ht_inside)
        frm14.place(x=widt_inside, y=ht_inside*6)

        frm15 = Frame(frm, bg='black', width=widt_inside, height=ht_inside)
        frm15.place(x=widt_inside*2, y=ht_inside*6)

        frm16 = Frame(frm, bg='black', width=widt_inside, height=ht_inside*2)
        frm16.place(x=0, y=ht_inside*7)

        frm17 = Frame(frm, bg='black', width=widt_inside, height=ht_inside*2)
        frm17.place(x=widt_inside, y=ht_inside*7)

        frm18 = Frame(frm, bg='black', width=widt_inside, height=ht_inside*2)
        frm18.place(x=widt_inside * 2, y=ht_inside*7)

        self.lbutthi = ImageTk.PhotoImage\
            (Image.open("lbutt.png").resize((ht_inside, ht_inside)))

        lab1 = Label(frm1, fg = 'green', bg='black', text="ONE-CLICK RECIPE BOOK", font=("Courier", int(ht_inside/5)))
        lab1.place(relx=.5, rely=.5, anchor="center")

        lab2 = Label(frm2, fg='green', bg='black', text="PERSONALISED RECIPE BOOK", font=("Courier", int(ht_inside / 5)))
        lab2.place(relx=.5, rely=.5, anchor="center")

        lab7 = Label(frm7, fg='white', bg='black', text="ADD RECIPE", font=("Courier", int(ht_inside / 5)))
        lab7.place(relx=.5, rely=.5, anchor="center")

        lab8 = Label(frm8, fg='white', bg='black', text="DELETE RECIPE", font=("Courier", int(ht_inside / 5)))
        lab8.place(relx=.5, rely=.5, anchor="center")

        lab9 = Label(frm9, fg='white', bg='black', text="CHANGE RECIPE", font=("Courier", int(ht_inside / 5)))
        lab9.place(relx=.5, rely=.5, anchor="center")

        lab13 = Label(frm13, fg='red', bg='black',
                      text="ADD SEARCH CATEGORY", font=("Courier", int(ht_inside / 5)))
        lab13.place(relx=.5, rely=.5, anchor="center")

        lab14 = Label(frm14, fg='red', bg='black',
                      text="DELETE SEARCH CATEGORY", font=("Courier", int(ht_inside / 5)))
        lab14.place(relx=.5, rely=.5, anchor="center")

        lab15 = Label(frm15, fg='red', bg='black',
                      text="ADD/DELETE OPTION", font=("Courier", int(ht_inside / 5)))
        lab15.place(relx=.5, rely=.5, anchor="center")

        lab20 = Label(frmb, fg='white', bg='black', text="BACK TO HOMEPAGE", font=("Courier", int(ht_inside / 5)))
        lab20.place(relx=.5, rely=0.15, anchor="center")

        button4 = tk.Button(frm4, text="View full list", image=self.lbutthi, borderwidth=0, highlightthickness=0,
                                      command=lambda: self.view_full_list(controller, parent))
        button4.place(relx=.5, rely=0.3, anchor="center")
        button4.image = self.lbutthi

        button5 = tk.Button(frm5, text='custom', image=self.lbutthi, borderwidth=0, highlightthickness=0,
                                                      command=lambda: controller.show_frame(CustomSearch, parent))
        button5.place(relx=.5, rely=.25, anchor="center")
        button5.image = self.lbutthi

        button10 = tk.Button(frm10, text="Add a recipe", image=self.lbutthi, borderwidth=0, highlightthickness=0,
                            command = lambda: controller.show_frame(AddRecipe, parent))
        button10.place(relx=.5, rely=.25, anchor="center")
        button10.image = self.lbutthi

        button11 = tk.Button(frm11, text="Delete a recipe", image=self.lbutthi, borderwidth=0, highlightthickness=0,
                                         command=lambda: controller.show_frame(DeleteRecipe, parent))
        button11.place(relx=.5, rely=.25, anchor="center")
        button11.image = self.lbutthi

        button12 = tk.Button(frm12, text="Change a recipe", image=self.lbutthi, borderwidth=0, highlightthickness=0,
                                 command=lambda: controller.show_frame(AmendRecipe, parent))
        button12.place(relx=.5, rely=.25, anchor="center")
        button12.image = self.lbutthi

        button16 = tk.Button(frm16, text="Add a new attribute", image=self.lbutthi, borderwidth=0, highlightthickness=0,
                                         command=lambda: controller.show_frame(AddColumn, parent))
        button16.place(relx=.5, rely=.25, anchor="center")
        button16.image = self.lbutthi

        button17 = tk.Button(frm17, text="Delete an attribute",image=self.lbutthi, borderwidth=0, highlightthickness=0,
                                      command=lambda: controller.show_frame(DeleteColumn, parent))
        button17.place(relx=.5, rely=.25, anchor="center")
        button17.image = self.lbutthi

        button18 = tk.Button(frm18, text="Add or delete and option", image= self.lbutthi, borderwidth=0, highlightthickness=0,
                                       command=lambda: controller.show_frame(AddDeleteOption, parent))
        button18.place(relx=.5, rely=.25, anchor="center")
        button18.image = self.lbutthi

        button23 = tk.Button(frmb, text="Back to homepage", image=self.lbutthi, borderwidth=0, highlightthickness=0,
                                command=lambda: controller.show_frame(StartPage, parent))
        button23.place(relx=.5, rely=.6, anchor="center")
        button23.image = self.lbutthi


    def view_full_list(self, controller, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute('select meal from RecipeList')
        tester_value = c.fetchall()
        ex_tester = [i for word in tester_value for i in word]
        conn.close()
        if ex_tester == ['EnterRecipe']:
            self.lbutt8 = ImageTk.PhotoImage \
                    (Image.open("lbutt.png").resize(
                    (int(screensize[1] / 8), int(screensize[1] / 8))))
            ran_em_win = tk.Toplevel()
            ran_em_win.title("Empty Plan Results")
            ran_em_win.geometry('{}x{}+{}+{}'.format(wid, hei, xxx, yyy))
            frm60 = Frame(ran_em_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            frm60.place(x=0)
            frm7 = Frame(frm60, bg='black', width=int(screensize[0] * 2 / 3), height=int(screensize[1] * 2 / 3))
            frm7.place(x=0, y=0)
            ran_empty = Label(frm7, fg='green', bg='black', text="ENTER A RECIPE FIRST",
                              font=("Courier", int(erht_inside)))
            ran_empty.place(relx=0.5, rely=0.25, anchor="center")
            ran_cl = Label(frm7, fg='white', bg='black', text="CLOSE WINDOW",
                           font=("Courier", int(erht_inside)))
            ran_cl.place(relx=0.5, rely=0.5, anchor="center")

            ran_em_button_m = tk.Button(frm7, text="Close Window", image=self.lbutt8,
                                        borderwidth=0, highlightthickness=0, command=ran_em_win.destroy)
            ran_em_button_m.place(relx=0.5, rely=0.75, anchor="center")
            ran_em_button_m.image = self.lbutt8

        else:
            conn = sqlite3.connect('master.db')
            c = conn.cursor()
            full_win = tk.Toplevel()
            full_win.wm_title("Full Recipe Book")
            full_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
            self.canvas = tk.Canvas(full_win, borderwidth=0, background="black")
            self.frame = tk.Frame(self.canvas, background="black")
            self.vsb = tk.Scrollbar(full_win, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.vsb.set)
            self.vsb.pack(side="right", fill="y")
            self.canvas.pack(side="left", fill="both", expand=True)
            self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                      tags="self.frame")
            self.frame.bind("<Configure>", self.onFrameConfigure)
            c.execute("""SELECT meal FROM RecipeList""")
            full_book = c.fetchall()
            conn.close()
            exploded_list = ([item for t in full_book for item in t])
            final_display = ("\n".join(exploded_list))
            z = StringVar()
            z.set(final_display)
            left_y_count = 1
            cols=['red', 'white', 'green']
            ccnt = 0
            for item in exploded_list:
                jeff = item
                self.flink_full[jeff] = Label(self.frame, text=jeff,
                                        font=("Courier", int(diary_y/6)), fg=cols[ccnt], bg='black', cursor="hand2")
                self.flink_full[jeff].bind("<Button-1>", lambda event, jeff=jeff: self.flink_open(event, jeff))
                self.flink_full[jeff].pack(side='bottom', anchor = 'w')
                left_y_count+=1
                ccnt+=1
                if ccnt==3:
                    ccnt-=3

            self.buttd8 = ImageTk.PhotoImage \
                (Image.open("lbutt.png").resize((int(diary_height / 8), int(diary_height / 8))))
            ran_lab = Label(full_win, fg='red', bg='black', text="CLOSE WINDOW",
                            font=("Courier", int(diary_height /35)))
            ran_lab.place(x=int(diary_wid *.74), y=int(diary_height * 4.75/10))

            ran_pl_button_m = tk.Button(full_win, text="Close Window", image=self.buttd8,
                                        borderwidth=0, highlightthickness=0, command=full_win.destroy)
            ran_pl_button_m.place(x=diary_wid * .80, y=int(diary_height * 5.5/ 10))
            ran_pl_button_m.image = self.buttd8


    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def flink_open(self, event, jeff):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute("select link from RecipeList WHERE meal =?", (jeff,))
        ln = c.fetchall()
        conn.close()
        ln1 = [item for t in ln for item in t]
        if ln1[0][:4] == "http":
            webbrowser.open_new(ln1[0])
        else:
            self.flink_full[jeff]['text'] = (jeff + " - " + ln1[0])


class CustomSearch (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='orange')
        self.cs_widgets_list = []
        self.ct_widgets_list = []
        self.dict_to_use = {}
        self.temp_dict = {}
        self.potential_meals = []
        self.lbutt8 = ImageTk.PhotoImage \
                (Image.open("lbutt.png").resize(
                (int(screensize[1] / 8), int(screensize[1] / 8))))
        self.lbuttd8 = ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((int(diary_height / 8), int(diary_height / 8))))
        self.cs_starter(controller, parent)

    def cs_starter(self, controller, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute('select meal from RecipeList')
        tester_value = c.fetchall()
        ex_tester = [i for word in tester_value for i in word]
        conn.close()
        if ex_tester == ['EnterRecipe']:
            photow = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
            wa = Label(self, image=photow)
            wa.image = photow
            wa.place(x=0, y=0, relwidth=1, relheight=1)
            frm50 = Frame(self, bg='black', width=wid, height=hei)
            frm50.place(x=xxx, y=yyy)
            frm60 = Frame(frm50, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            frm60.place(x=0)
            frm7 = Frame(frm50, bg='black', width=int(screensize[0] * 2 / 3), height=int(screensize[1] * 2 / 3))
            frm7.place(x=0, y=0)
            ran_empty = Label(frm7, fg='green', bg='black', text="ENTER A RECIPE FIRST",
                              font=("Courier", int(erht_inside)))
            ran_empty.place(relx=0.5, rely=0.25, anchor="center")
            ran_cl = Label(frm7, fg='white', bg='black', text="BACK TO HOMEPAGE",
                           font=("Courier", int(erht_inside)))
            ran_cl.place(relx=0.5, rely=0.5, anchor="center")

            ran_em_button_m = tk.Button(frm7, text="Back to homepage", image=self.lbutt8, borderwidth=0,
                                       highlightthickness=0, command=lambda: controller.show_frame(StartPage, parent))
            ran_em_button_m.place(relx=0.5, rely=0.75, anchor="center")
            ran_em_button_m.image = self.lbutt8

        else:
            self.make_dict(controller, 0, parent)

    def make_dict_to_use(self, sv, item):
        val = sv.get()
        if val == 'any':
            val = ''
        self.temp_dict = {str(item): val}
        for ky in self.temp_dict:
            if ky in self.dict_to_use.keys():
                self.dict_to_use[ky] = self.temp_dict[ky]
        self.calculate_custom_view()

    def calculate_custom_view(self):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        self.potential_meals = []
        demand = {k: v for k, v in self.dict_to_use.items() if v}
        x = len(demand)
        c.execute('select * from RecipeList')
        final_list = list(self.dict_to_use.values())
        for row in c.fetchall():
            make_row_a_list = list(row)
            cut_off_meal = make_row_a_list[2:]
            mapped = zip(cut_off_meal, final_list)
            counter = 0
            for i in mapped:
                if i[0] == i[1]:
                    counter += 1
            if counter == x:
                self.potential_meals.append(row[0])
        conn.close()

    def pop_upper(self):
        self.link_list = []
        self.linkc_dict = {}
        self.clink_full = {}
        cus_win = tk.Toplevel()
        cus_win.wm_title("Full Recipe Book")
        cus_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
        self.canvas = tk.Canvas(cus_win, borderwidth=0, background="black")
        self.frame = tk.Frame(self.canvas, background="black")
        self.vsb = tk.Scrollbar(cus_win, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        ran_lab = Label(cus_win, fg='red', bg='black', text="CLOSE WINDOW",
                        font=("Courier", int(diary_height / 35)))
        ran_lab.place(x=int(diary_wid * .74), y=int(diary_height * 4.75 / 10))

        ran_pl_button_m = tk.Button(cus_win, text="Close Window", image=self.lbuttd8,
                                    borderwidth=0, highlightthickness=0, command=cus_win.destroy)
        ran_pl_button_m.place(x=diary_wid * .80, y=int(diary_height * 5.5 / 10))
        ran_pl_button_m.image = self.lbuttd8
        left_y_count = 1
        cols = ['red', 'white', 'green']
        ccnt = 0
        if len(self.potential_meals) == 0:
            self.c_label2 = Label(self.frame, text="NO MATCHES" "\n" "CLOSE WINDOW",
                                     fg='white', bg='black', font=("Courier", int(diary_height / 10)))
            self.c_label2.pack(side='bottom', anchor='w')

        for li in self.potential_meals:
            jeff = li
            self.clink_full[jeff] = Label(self.frame, text=jeff,
                                          font=("Courier", int(diary_y / 6)), fg=cols[ccnt], bg='black', cursor="hand2")
            self.clink_full[jeff].bind("<Button-1>", lambda event, jeff=jeff: self.clink_open(event, jeff))
            self.clink_full[jeff].pack(side='bottom', anchor='w')
            left_y_count += 1
            ccnt += 1
            if ccnt == 3:
                ccnt -= 3

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def clink_open(self, event, jeff):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute("select link from RecipeList WHERE meal =?", (jeff,))
        ln = c.fetchall()
        conn.close()
        ln1 = [item for t in ln for item in t]
        if ln1[0][:4] == "http":
            webbrowser.open_new(ln1[0])
        else:
            self.clink_full[jeff]['text'] = jeff + " - " + ln1[0]

    def make_dict(self, controller, x, parent):
        photow = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
        wa = Label(self, image=photow)
        wa.image = photow
        wa.place(x=0, y=0, relwidth=1, relheight=1)

        cwidt_master = int(screensize[0]/3)
        cwidt_wid = int(cwidt_master/3)
        cwidt_tit = int(cwidt_wid*2)
        cht_master = int(screensize[1]*0.8)
        cht_inside = int(cht_master/12)
        im = int(cht_inside/2)
        frm_wid_place = cwidt_master + cwidt_tit
        self.lbuttim = ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((im, im)))
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        cursor = conn.execute('select * FROM RecipeList')
        names = list(map(lambda x: x[0], cursor.description))
        names1 = names[2:]
        no_wid = len(names1)
        no_wids = len(names1)+1


        cfrm_tit = Frame(self, bg='black', width=cwidt_tit, height=cht_inside*no_wids)
        cfrm_tit.place(x=int(screensize[0]/3), y=int(screensize[1]*0.1))

        cfrm_wid = Frame(self, bg='black', width=cwidt_wid, height=cht_inside * no_wids)
        cfrm_wid.place(x=frm_wid_place, y=int(screensize[1] * 0.1))

        cfrmb = Frame(self, bg='black', width=cht_inside*3.5, height=cht_inside)
        cfrmb.place(x=int(screensize[0]*0.4325), y=int((screensize[1] * 0.1)+cht_inside* no_wids))

        s = shelve.open('test_shelf.db')
        cst = s['title_holder']
        nice_names = list(cst.values())
        nice_names1 = nice_names[2:]
        yy = 0
        yv = 0
        cx = 0
        ccx = 0
        colours = ['green', 'black', 'red', 'green', 'black', 'red', 'green', 'black', 'red', 'green']
        coloursw = ['green', 'white', 'red', 'green', 'white', 'red', 'green', 'white', 'red', 'green']
        for widget in self.cs_widgets_list:
            widget.destroy()
        for widget in self.ct_widgets_list:
            widget.destroy()
        for item in names1:
            self.dict_to_use[item] = ""

        for nice_item in nice_names1:
            self.lbel = tk.Label(cfrm_tit, text=nice_item, font=LARGE_FONT, bg = 'black', fg = coloursw[cx])
            self.lbel.place(relx=0, y=yy)
            self.cs_widgets_list.append(self.lbel)
            yy += cht_inside
            cx += 1

        for item in names1:
            c.execute("SELECT " + item + " FROM RecipeList")
            fetch = c.fetchall()
            ohfetch = StringVar()
            ohfetch.set('any')
            mfetch = [itt for t in fetch for itt in t]
            sfetch = set(mfetch)
            ohfetch.trace("w", lambda name, index, mode, item =item, sv=ohfetch: self.make_dict_to_use(sv, item))
            self.box = OptionMenu(cfrm_wid, ohfetch, *sfetch, 'any')
            self.box.config(bg=coloursw[ccx], font=("Courier", int(cht_inside / 5)))
            menu = self.nametowidget(self.box.menuname)
            menu.config(font=("Courier", int(cht_inside / 5)), fg=colours[ccx])
            self.box.place(relx=0.25, y=yv)
            yv += cht_inside
            ccx += 1
            self.cs_widgets_list.append(self.box)
        conn.close()

        labcb = Label(cfrm_tit, fg='red', bg='black', text="SHOW RESULTS", font=("Courier", int(cht_inside / 5)))
        labcb.place(relx=.75, y=(cht_inside*no_wid)+cht_inside*.05, anchor="center")

        cust_button_m = tk.Button(cfrm_tit, text="Show Results",
                                  image=self.lbuttim, borderwidth=0, highlightthickness=0, command=self.pop_upper)
        cust_button_m.place(relx=.7, y=(cht_inside*no_wid)+cht_inside*.3)
        cust_button_m.image = self.lbuttim

        labcb2 = Label(cfrmb, fg='white', bg='black', text="BACK TO HOMEPAGE", font=("Courier", int(cht_inside / 5)))
        labcb2.place(relx=.5, rely=0.15, anchor="center")

        cust_button_m2 = tk.Button(cfrmb, text="Back to homepage", image=self.lbuttim, borderwidth=0, highlightthickness=0,
                                command=lambda: self.make_dict(controller, 1, parent))
        cust_button_m2.place(relx=.5, rely=.6, anchor="center")
        cust_button_m2.image = self.lbuttim

        self.ct_widgets_list.append(labcb)
        self.ct_widgets_list.append(labcb2)
        self.ct_widgets_list.append(cust_button_m)
        self.ct_widgets_list.append(cust_button_m2)
        if x == 1:
            controller.show_frame(StartPage, parent)


class AmendRecipe (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        cursor = conn.execute('select * FROM RecipeList')
        self.names = list(map(lambda x: x[0], cursor.description))
        self.names1 = self.names[2:]
        self.meal = self.names[0]
        self.meal_cut = self.meal[2:-2]
        s = shelve.open('test_shelf.db')
        self.at = s['title_holder']
        self.am_nice_names = list(self.at.values())
        conn.close()
        self.am_nice_names1 = self.am_nice_names[1:]
        self.amend_recipe_dict = {}
        self.holding_dict = {}
        self.holding_dict_meal = {}
        self.list_of_widgets = []
        self.f1list_of_widgets = []
        self.clist_of_widgets = []
        self.frame = Frame(self)
        self.frame.place(x=5, y=5)
        self.frame2 = Frame(self)
        self.frame2.pack()
        self.holding_dict_link = {}
        self.lb8 = ImageTk.PhotoImage \
                (Image.open("lbutt.png").resize(
                (int(screensize[1] / 8), int(screensize[1] / 8))))
        self.lb16 = ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((int(screensize[1] / 16), int(screensize[1] / 16))))
        self.meal_box_maker(controller, 0, parent)

    def meal_box_maker(self, controller, x, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute('select meal from RecipeList')
        tester_value = c.fetchall()
        ex_tester = [i for word in tester_value for i in word]
        conn.close()
        if ex_tester == ['EnterRecipe']:
            photow = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
            wa = Label(self, image=photow)
            wa.image = photow
            wa.place(x=0, y=0, relwidth=1, relheight=1)
            frm50 = Frame(self, bg='black', width=wid, height=hei)
            frm50.place(x=xxx, y=yyy)
            frm60 = Frame(frm50, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            frm60.place(x=0)
            frm7 = Frame(frm50, bg='black', width=int(screensize[0] * 2 / 3), height=int(screensize[1] * 2 / 3))
            frm7.place(x=0, y=0)
            ran_empty = Label(frm7, fg='green', bg='black', text="ENTER A RECIPE FIRST",
                              font=("Courier", int(erht_inside)))
            ran_empty.place(relx=0.5, rely=0.25, anchor="center")
            ran_cl = Label(frm7, fg='white', bg='black', text="BACK TO HOMEPAGE",
                           font=("Courier", int(erht_inside)))
            ran_cl.place(relx=0.5, rely=0.5, anchor="center")

            ran_em_button_m = tk.Button(frm7, text="Back to homepage", image=self.lb8, borderwidth=0,
                                        highlightthickness=0, command=lambda: controller.show_frame(StartPage, parent))
            ran_em_button_m.place(relx=0.5, rely=0.75, anchor="center")
            ran_em_button_m.image = self.lb8

        else:
            for widget in self.clist_of_widgets:
                widget.destroy()
            for widget in self.f1list_of_widgets:
                widget.destroy()
            for widget in self.list_of_widgets:
                widget.destroy()
            conn = sqlite3.connect('master.db')
            c = conn.cursor()
            c.execute("""SELECT meal FROM RecipeList""")
            am_full_book = c.fetchall()
            conn.close()
            am_exploded_list = ([item for t in am_full_book for item in t])
            photoar = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
            ara = Label(self, image=photoar)
            ara.image = photoar
            ara.place(x=0, y=0, relwidth=1, relheight=1)

            self.amfrm = Frame(self, bg='black', width=int(screensize[0] / 3), height=screensize[1])
            self.amfrm.place(relx=2 / 3, rely=1 / 10)

            self.amfrmt = Frame(self, bg='black', width=int(screensize[0] / 3.25), height=screensize[1] / 10)
            self.amfrmt.place(relx=2 / 3, rely=0)

            self.amfrmbt = Frame(self, bg='black', width=int(screensize[0] / 4), height=screensize[1] / 4)
            self.amfrmbt.place(relx=0.33, rely=0.4)

            laba = Label(self.amfrmt, fg='white', bg='black', text="RECIPE TO CHANGE",
                          font=("Courier", int(screensize[1]/ 52)))
            laba.place(relx=.5, rely=.5, anchor="center")


            self.mlistbox = Listbox(self.amfrm, width=35, height=50, fg = 'white', bg = "black")
            self.mlistbox.pack(side='left', fill='y')
            scrollbar = Scrollbar(self.frame, orient="vertical", command=self.mlistbox.yview)
            scrollbar.pack(side="right", fill="y")
            self.f1list_of_widgets.append(scrollbar)
            self.mlistbox.insert(END, *am_exploded_list)
            self.mlistbox.config(yscrollcommand=scrollbar.set, font=("Courier", int(screensize[1] / 52)))


            mbm_labs = Label(self.amfrmbt, fg='white', bg='black', text="SELECT RECIPE",
                          font=("Courier", int(screensize[0] / 70)))
            mbm_labs.place(relx=.5, rely=0.15, anchor="center")

            mbm_labb = Label(self.amfrmbt, fg='red', bg='black', text="BACK TO HOMEPAGE",
                          font=("Courier", int(screensize[0] / 70)))
            mbm_labb.place(relx=.5, rely=0.65, anchor="center")

            mbm_button1 = tk.Button(self.amfrmbt, text="Select Meal",
                                    image=self.lb16, borderwidth=0, highlightthickness=0,
                                    command=lambda: self.to_stop_crash(controller, parent))
            mbm_button1.place(relx = .5, rely = 0.35, anchor='center')
            mbm_button1.image = self.lb16


            mam_button2 = tk.Button(self.amfrmbt, text="Back to homepage",
                                    image = self.lb16, borderwidth = 0, highlightthickness = 0,
                                    command=lambda: self.meal_box_maker(controller, 1, parent))
            mam_button2.place(relx=.5, rely=0.85, anchor='center')
            mam_button2.image = self.lb16

            self.f1list_of_widgets.append(self.mlistbox)
            self.f1list_of_widgets.append(self.amfrm)
            self.f1list_of_widgets.append(self.amfrmt)
            self.f1list_of_widgets.append(self.amfrmbt)
            self.f1list_of_widgets.append(mbm_labb)
            self.f1list_of_widgets.append(mbm_labs)
            self.f1list_of_widgets.append(laba)
            self.f1list_of_widgets.append(mbm_button1)
            self.f1list_of_widgets.append(mam_button2)
            if x == 1:
                controller.show_frame(StartPage, parent)

    def to_stop_crash(self, controller, parent):
        index = self.mlistbox.curselection()
        self.value = self.mlistbox.get(index)
        for widget in self.f1list_of_widgets:
            widget.destroy()
        conn = sqlite3.connect('master.db')
        c = conn.cursor()

        cwidt_master = int(screensize[0] / 3)
        cwidt_wid = int(cwidt_master / 3)
        self.cwidt_tit = int(cwidt_wid * 2)
        self.cht_master = int(screensize[1] * 0.8)
        self.cht_inside = int(self.cht_master / 13)
        aim = int(self.cht_inside / 2)
        frm_wid_place = cwidt_master + self.cwidt_tit

        self.cno_wid = len(self.names)
        self.cno_wids = len(self.names1) + 3
        self.cfor_wids = 2 * self.cht_inside

        yv = self.cfor_wids + (.25 * self.cht_inside)
        yy = 0.25 * self.cht_inside
        cx = 0
        ccx = 0
        colours = ['green', 'black', 'red', 'green', 'black', 'red', 'green', 'black', 'red', 'green']
        colourswid = ['green', 'white', 'red', 'green', 'white', 'red', 'green', 'white', 'red', 'green']
        coloursw = ['white', 'white', 'green', 'white', 'red', 'green', 'white', 'red',
                      'green', 'white', 'red', 'green']


        self.cfrm_tit = Frame(self, bg='black', width=self.cwidt_tit, height=self.cht_inside * self.cno_wids)
        self.cfrm_tit.place(x=int(screensize[0] / 3), y=int(screensize[1] * 0.1))

        cfrm_wid = Frame(self, bg='black', width=cwidt_wid, height=self.cht_inside * self.cno_wids)
        cfrm_wid.place(x=frm_wid_place, y=int(screensize[1] * 0.1))

        cfrmb = Frame(self, bg='black', width=cwidt_wid + self.cwidt_tit, height=self.cht_inside)
        cfrmb.place(x=int(screensize[0]/3), y=int((screensize[1] * 0.1) + self.cht_inside * self.cno_wids))

        self.e = Entry(cfrm_wid, font=('Courier', int(self.cht_inside / 5)))
        self.e.insert(END, self.value)
        self.e.place(relx=0, y=self.cht_inside * .25)
        c.execute("select link from RecipeList WHERE meal =?", (self.value,))
        clinkie = c.fetchall()
        alinkie = [bt for b in clinkie for bt in b]
        self.le = Entry(cfrm_wid, font=('Courier', int(self.cht_inside / 5)))
        self.le.insert(END, *alinkie)
        self.le.place(relx=0, y=self.cht_inside * 1.25)

        for nice_item in self.am_nice_names:
            lbel = tk.Label(self.cfrm_tit, text=nice_item, font=LARGE_FONT, bg='black', fg=coloursw[cx])
            lbel.place(relx=0, y=yy)
            self.list_of_widgets.append(lbel)
            yy += self.cht_inside
            cx += 1

        for item in self.names1:
            c.execute("SELECT " + item + " FROM RecipeList")
            nevery_value_am = c.fetchall()
            every_value_am = [gt for g in nevery_value_am for gt in g]
            selected_var_am = StringVar()
            s = shelve.open('test_shelf.db')
            op_lst = s['key1']
            options_list = op_lst[item]
            c.execute("SELECT " + item + " FROM RecipeList WHERE meal = (?)", (self.value,))
            acurrent_value_for_meal = c.fetchall()
            current_value_for_meal = [iti for ab in acurrent_value_for_meal for iti in ab]
            selected_var_am.set(*current_value_for_meal)
            selected_var_am.trace("w", lambda name, index, mode, item = item,
                                      sv=selected_var_am: self.store_values(sv, item))
            self.box = OptionMenu(cfrm_wid, selected_var_am, *options_list)
            self.box.config(bg=colourswid[ccx], font=("Courier", int(self.cht_inside / 5)))
            menu = self.nametowidget(self.box.menuname)
            menu.config(font=("Courier", int(self.cht_inside / 5)), fg=colours[ccx])
            self.box.pack(side=LEFT)
            self.list_of_widgets.append(self.box)
            self.box.place(relx=0.25, y=yv)
            yv += self.cht_inside
            ccx += 1
            self.list_of_widgets.append(self.box)
        conn.close()

        self.lba = ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((aim, aim)))

        labs = Label(self.cfrm_tit, fg='red', bg='black', text="SEND CHANGES",
                      font=("Courier", int(self.cht_inside / 5)))
        labs.place(relx=.725, y=(self.cht_inside * self.cno_wid) + self.cht_inside * .05, anchor="center")

        am_button3 = tk.Button(self.cfrm_tit, text="Send Changes", image=self.lba,
                               borderwidth=0, highlightthickness=0,
                               command=lambda: self.test_eb(controller, parent))
        am_button3.place(relx=.675, y=(self.cht_inside * self.cno_wid) + self.cht_inside * .3)
        am_button3.image = self.lba

        labbac = Label(cfrmb, fg='white', bg='black', text="BACK TO HOMEPAGE",
                      font=("Courier", int(self.cht_inside / 5)))
        labbac.place(relx=.75, rely=0.15, anchor="center")

        labbac1 = Label(cfrmb, fg='green', bg='black', text="BACK A PAGE",
                        font=("Courier", int(self.cht_inside / 5)))
        labbac1.place(relx=.25, rely=0.15, anchor="center")


        am_button2 = tk.Button(cfrmb, text="Back to homepage",
                               image=self.lba, borderwidth=0, highlightthickness=0,
                               command=lambda: self.meal_box_maker(controller, 1, parent))
        am_button2.place(relx=.75, rely=.6, anchor="center")
        am_button2.image = self.lba


        am_button1 = tk.Button(cfrmb, text="Back a Page",
                               image=self.lba, borderwidth=0, highlightthickness=0,
                               command=lambda: self.meal_box_maker(controller, 0, parent))
        am_button1.place(relx=.25, rely=.6, anchor="center")
        am_button1.image = self.lba

        self.list_of_widgets.append(am_button1)
        self.list_of_widgets.append(am_button2)
        self.list_of_widgets.append(am_button3)
        self.list_of_widgets.append(self.e)
        self.list_of_widgets.append(self.le)
        self.list_of_widgets.append(cfrm_wid)
        self.list_of_widgets.append(cfrmb)
        self.list_of_widgets.append(self.cfrm_tit)
        self.list_of_widgets.append(labs)
        self.list_of_widgets.append(labbac)
        self.list_of_widgets.append(labbac1)

    def store_values(self, sv, item):
        self.ctit= item
        self.vtit = sv.get()
        self.holding_dict[item] = self.vtit

    def test_eb(self, controller, parent):
        self.new_meal_title = self.e.get()
        self.new_link_title = self.le.get()
        self.lbd8 = ImageTk.PhotoImage \
                (Image.open("lbutt.png").resize(
                (int(diary_height / 8), int(diary_height / 8))))
        if len(self.new_meal_title) == 0 and len(self.new_link_title) == 0:
            both_win = tk.Toplevel()
            both_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
            test1 = Frame(both_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            test1.place(x=0)
            testi1 = Frame(test1, bg='black', width=diary_wid, height=diary_height)
            testi1.place(x=0)
            both_lbl = Label(testi1, text="Please fill in the meal and link names",
                             fg='white', bg='black', font=("Courier", int(diary_height / 30)))
            both_lbl.place(relx=0.1, rely=0.3)
            test_button = tk.Button(testi1, text="Close Window", image=self.lbd8,
                                       borderwidth=0, highlightthickness=0, command=both_win.destroy)
            test_button.place(relx=0.45, rely=0.5)
            test_button.image = self.lbd8
        else:
            if len(self.new_meal_title)==0:
                both_win1 = tk.Toplevel()
                both_win1.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
                test2= Frame(both_win1, bg='black', width=int(screensize[0]), height=int(screensize[1]))
                test2.place(x=0)
                testi2 = Frame(test2, bg='black', width=diary_wid, height=diary_height)
                testi2.place(x=0)
                both_lbl1 = Label(testi2, text="Please fill in the meal name",
                                 fg='white', bg='black', font=("Courier", int(diary_height / 30)))
                both_lbl1.place(relx=0.225, rely=0.3)
                test_button1 = tk.Button(testi2, text="Close Window", image=self.lbd8,
                                        borderwidth=0, highlightthickness=0, command=both_win1.destroy)
                test_button1.place(relx=0.45, rely=0.5)
                test_button1.image = self.lbd8
            if len(self.new_link_title)==0:
                both_win1 = tk.Toplevel()
                both_win1.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
                test2 = Frame(both_win1, bg='black', width=int(screensize[0]), height=int(screensize[1]))
                test2.place(x=0)
                testi2 = Frame(test2, bg='black', width=diary_wid, height=diary_height)
                testi2.place(x=0)
                both_lbl1 = Label(testi2, text="Please enter a link",
                                  fg='white', bg='black', font=("Courier", int(diary_height / 30)))
                both_lbl1.place(relx=0.3, rely=0.3)
                test_button1 = tk.Button(testi2, text="Close Window", image=self.lbd8,
                                         borderwidth=0, highlightthickness=0, command=both_win1.destroy)
                test_button1.place(relx=0.45, rely=0.5)
                test_button1.image = self.lbd8

            if len(self.new_meal_title) > 50 or len(self.new_link_title) > 500:
                ad_long_win = tk.Toplevel()
                ad_long_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
                ad_l = Frame(ad_long_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
                ad_l.place(x=0)
                adi_l = Frame(ad_long_win, bg='black', width=diary_wid, height=diary_height)
                adi_l.place(x=0, y=0)

                ad_long_lab = Label(adi_l, fg='red', bg='black', text="CLOSE WINDOW",
                                    font=("Courier", int(diary_height / 30)))
                ad_long_lab.place(x=diary_wid * .38, y=int(diary_height * 15 / 32))

                ad_long_button = tk.Button(adi_l, text="Close Window", image=self.lbd8,
                                           borderwidth=0, highlightthickness=0, command=ad_long_win.destroy)
                ad_long_button.place(x=diary_wid * .43, y=int(diary_height * 18 / 32))
                ad_long_button.image = self.lbd8

                if len(self.new_meal_title) > 50 and len(self.new_link_title) <= 500:
                    labx = "Meal title maximum 50 characters"
                if len(self.new_meal_title) <= 50 and len(self.new_link_title) > 500:
                    labx = "Link maximum 500 characters"
                if len(self.new_meal_title) > 50 and len(self.new_link_title) > 500:
                    labx = "Meal title maximum 50 characters" "\n""Link maximum 500 characters"
                ad_lab = Label(adi_l, fg='red', bg='black', text=labx,
                               font=("Courier", int(diary_height / 30)))
                ad_lab.place(x=diary_wid * .2, y=int(diary_height * 10 / 32))
            if 0 < len(self.new_meal_title) <= 50 and 0< len(self.new_link_title) <= 500:
                self.make_changes(controller, parent)

    def make_changes(self, controller, parent):
        self.new_meal_title = self.e.get()
        self.new_link_title = self.le.get()
        self.holding_dict_meal["new meal"] = self.new_meal_title
        self.holding_dict_link["new link"] = self.new_link_title
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        for k in self.holding_dict:
            c.execute("UPDATE RecipeList SET " + k + " = (?) WHERE meal = (?)",
                      (self.holding_dict[k], self.value))
            conn.commit()

        for ky in self.holding_dict_meal:
            c.execute("UPDATE RecipeList SET meal = (?) WHERE meal = (?)",
                      (self.holding_dict_meal[ky], self.value))
            conn.commit()
        for kys in self.holding_dict_link:
            c.execute("UPDATE RecipeList SET link = (?) WHERE meal = (?)",
                      (self.holding_dict_link[kys], self.value))
            conn.commit()
        conn.close()
        self.holding_dict_meal = {}
        self.holding_dict = {}
        self.holding_dict_link = {}
        for widget in self.list_of_widgets:
            widget.destroy()

        self.amfrmbt = Frame(self, bg='black', width=int(screensize[0] / 4), height=screensize[1] / 4)
        self.amfrmbt.place(relx=0.33, rely=0.4)


        calab = Label(self.amfrmbt, fg='white', bg='black', text="CHANGE ANOTHER RECIPE",
                         font=("Courier", int(screensize[0] / 70)))
        calab.place(relx=.5, rely=0.15, anchor="center")

        balab = Label(self.amfrmbt, fg='red', bg='black', text="BACK TO HOMEPAGE",
                         font=("Courier", int(screensize[0] / 70)))
        balab.place(relx=.5, rely=0.65, anchor="center")

        cam_button1 = tk.Button(self.amfrmbt, text="Change Another Meal",
                                image=self.lb16, borderwidth=0, highlightthickness=0,
                                command=lambda: self.meal_box_maker(controller, 0, parent))
        cam_button1.place(relx=.5, rely=0.35, anchor='center')
        cam_button1.image = self.lb16

        cam_button2 = tk.Button(self.amfrmbt, text="Back to homepage",
                                image=self.lb16, borderwidth=0, highlightthickness=0,
                                command=refresh)
        cam_button2.place(relx=.5, rely=0.85, anchor='center')
        cam_button2.image = self.lb16

        self.clist_of_widgets.append(cam_button1)
        self.clist_of_widgets.append(cam_button2)
        self.clist_of_widgets.append(self.amfrmbt)
        self.clist_of_widgets.append(calab)
        self.clist_of_widgets.append(balab)


class AddRecipe(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.list_of_widgets = []
        self.f1list_of_wirdgets = []
        self.opening_widgets = []
        self.opening_widgets2 = []
        self.opening_widgets_sb = []
        self.opening_widgets_sbn = []
        self.frame = Frame(self)
        self.frame.place(x=5, y=5)
        self.final_dict = {}
        self.holding_dict_meal = {}
        self.holding_dict = {}
        self.holding_dict_new = {}
        self.holding_dict_meal_new = {}
        self.final_first_dict = {}
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        cursor = conn.execute('select * FROM RecipeList')
        self.names = list(map(lambda x: x[0], cursor.description))
        self.names1 = self.names[2:]
        self.meal = self.names[0]
        self.optos = []
        conn.close()
        s = shelve.open('test_shelf.db')
        self.art = s['title_holder']
        self.add_nice_names = list(self.art.values())
        self.add_nice_names1 = self.add_nice_names[1:]
        self.first_meal = []
        self.first_link = []
        self.new_meal_title = []
        self.new_link_title = []
        self.holding_dict_link_new = {}
        self.holding_dict_link = {}
        self.starter_motor(controller, parent)

    def starter_motor(self, controller, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute('select meal from RecipeList')
        tester_value = c.fetchall()
        ex_tester = [i for word in tester_value for i in word]
        c.close()
        if ex_tester == ['EnterRecipe']:
            self.first_recipe(controller, 0, parent)
        else:
            self.box_maker(controller, 0, parent)

    def first_recipe(self, controller, y, parent):
        photoar = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
        ara = Label(self, image=photoar)
        ara.image = photoar
        ara.place(x=0, y=0, relwidth=1, relheight=1)

        awidt_master = int(screensize[0] / 3)
        awidt_wid = int(awidt_master / 3)
        self.awidt_tit = int(awidt_wid * 2)
        self.aht_master = int(screensize[1] * 0.8)
        self.aht_inside = int(self.aht_master / 13)
        aim = int(self.aht_inside / 2)
        frm_wid_place = awidt_master + self.awidt_tit

        self.ano_wid = len(self.names)
        self.ano_wids = len(self.names1) + 3
        self.for_wids = 2 * self.aht_inside

        self.lba = ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((aim, aim)))

        s = shelve.open('test_shelf.db')
        cst = s['title_holder']
        nice_names = list(cst.values())
        nice_names1 = nice_names[2:]
        yy = self.for_wids + (.25 * self.aht_inside)
        yv = 0.25 * self.aht_inside
        cx = 0
        ccx = 0
        colours = ['green', 'black', 'red', 'green', 'black', 'red', 'green', 'black', 'red', 'green']
        colourswid = ['green', 'white', 'red', 'green', 'white', 'red', 'green', 'white', 'red', 'green']
        colourslab = ['white', 'white', 'green', 'white', 'red', 'green', 'white', 'red',
                      'green', 'white', 'red', 'green']

        for widget in self.opening_widgets:
            widget.destroy()
        for widget in self.opening_widgets_sb:
            widget.destroy()
        self.holding_dict_meal_new = {}
        self.holding_dict_link_new = {}
        self.holding_dict_new = {}
        self.final_first_dict = {}
        self.afrm_tit = Frame(self, bg='black', width=self.awidt_tit, height=self.aht_inside * self.ano_wids)
        self.afrm_tit.place(x=int(screensize[0] / 3), y=int(screensize[1] * 0.1))

        afrm_wid = Frame(self, bg='black', width=awidt_wid, height=self.aht_inside * self.ano_wids)
        afrm_wid.place(x=frm_wid_place, y=int(screensize[1] * 0.1))

        afrmb = Frame(self, bg='black', width=self.aht_inside * 3.5, height=self.aht_inside)
        afrmb.place(x=int(screensize[0] * 0.4325), y=int((screensize[1] * 0.1) + self.aht_inside * self.ano_wids))

        first_meal_var = StringVar()
        first_meal_var.trace("w", lambda name, index, mode,
                                         msv1=first_meal_var: self.new_meal_maker(msv1, controller, parent))
        self.first_meal_entry = Entry(afrm_wid, textvariable=first_meal_var,
                           font=('Courier', int(self.aht_inside / 5)))
        self.first_meal_entry.place(relx=0, y=self.aht_inside * .25)

        first_link_var = StringVar()
        first_link_var.trace("w", lambda name, index, mode,
                                         msv2=first_link_var: self.new_link_maker(msv2, controller, parent))
        self.first_link_entry = Entry(afrm_wid, textvariable=first_link_var,
                                font=('Courier', int(self.aht_inside / 5)))
        self.first_link_entry.place(relx=0, y=self.aht_inside * 1.25)

        self.opening_widgets.append(self.afrm_tit)
        self.opening_widgets.append(afrmb)
        self.opening_widgets.append(afrm_wid)
        self.opening_widgets.append(self.first_link_entry)
        self.opening_widgets.append(self.first_meal_entry)


        for nice_item in self.add_nice_names:
            a_lbel = tk.Label(self.afrm_tit, text=nice_item, font=LARGE_FONT, bg='black', fg=colourslab[cx])
            a_lbel.place(relx=0, y=yv)
            self.opening_widgets.append(a_lbel)
            yv += self.aht_inside
            cx += 1

        for name in self.names1:
            s = shelve.open('test_shelf.db')
            opto_stage = s['key1']
            self.optos = opto_stage[name]
            mi_var = StringVar()
            mi_var.set("Empty")
            self.mi_box = OptionMenu(afrm_wid, mi_var, *self.optos)
            self.mi_box.config(bg=colourswid[ccx], font=("Courier", int(self.aht_inside / 5)))
            mi_var.trace("w", lambda name, index, mode, ite=name,
                                              svm=mi_var: self.store_r_values(svm, ite, controller, parent))
            menu = self.nametowidget(self.mi_box.menuname)
            menu.config(font=("Courier", int(self.aht_inside / 5)), fg=colours[ccx])
            self.mi_box.place(relx=.25, y=yy)
            yy += self.aht_inside
            ccx += 1
            self.opening_widgets.append(self.mi_box)

        labba = Label(afrmb, fg='white', bg='black', text="BACK TO HOMEPAGE",
                      font=("Courier", int(self.aht_inside / 5)))
        labba.place(relx=.5, rely=0.15, anchor="center")

        first_button2 = tk.Button(afrmb, text="Back to homepage",
                               image=self.lba, borderwidth=0, highlightthickness=0,
                               command=lambda: self.first_recipe(controller, 1, parent))
        first_button2.place(relx=.5, rely=.6, anchor="center")
        first_button2.image = self.lba
        self.opening_widgets.append(first_button2)
        self.opening_widgets.append(labba)
        if y == 1:
            controller.show_frame(StartPage, parent)

    def button_func(self, controller, parent):
        for widget in self.opening_widgets_sb:
            widget.destroy()

        self.nln4 = 0
        self.nln2 = 0

        self.nln1 = len(self.names1)

        for k in self.holding_dict_meal_new:
            if self.holding_dict_meal_new[k]:
                self.nln2 = 1

        self.nln3 = len(self.holding_dict_new.values())

        for k in self.holding_dict_link_new:
            if self.holding_dict_link_new[k]:
                self.nln4 = 1
        if self.nln2 != 0 and self.nln4 != 0 \
                and self.nln1 == self.nln3 and 'Empty' not in (self.final_first_dict.values()):
            first_button1 = tk.Button(self.afrm_tit, text="Send Recipe", image=self.lba,
                                   borderwidth=0, highlightthickness=0,
                                   command=lambda: self.make_first_changes_test(controller, parent))
            first_button1.place(relx=.675, y=(self.aht_inside * self.ano_wid) + self.aht_inside * .3)
            first_button1.image = self.lba

            labcs = Label(self.afrm_tit, fg='red', bg='black', text="SEND RECIPE",
                          font=("Courier", int(self.aht_inside / 5)))
            labcs.place(relx=.725, y=(self.aht_inside * self.ano_wid) + self.aht_inside * .05, anchor="center")

            self.opening_widgets_sb.append(first_button1)
            self.opening_widgets_sb.append(labcs)

    def new_meal_maker(self, msv1, controller, parent):
        self.first_meal = str(msv1.get())
        self.holding_dict_meal_new['meal'] = self.first_meal
        jiff = list(self.holding_dict_meal_new.values())
        joff = (jiff[0].lstrip(' '))
        self.holding_dict_meal_new['meal'] = joff
        self.button_func(controller, parent)

    def new_link_maker(self, msv2, controller, parent):
        self.first_link = self.first_link_entry.get()
        self.holding_dict_link_new['link'] = self.first_link
        biff = list(self.holding_dict_link_new.values())
        boff = (biff[0].lstrip(' '))
        self.holding_dict_link_new['link'] = boff
        self.button_func(controller, parent)

    def store_r_values(self, svm, ite, controller, parent):
        for widget in self.opening_widgets_sb:
            widget.destroy()
        self.knrec = ite
        self.vnrec = svm.get()
        self.holding_dict_new[ite] = self.vnrec
        self.button_func(controller, parent)

    def make_first_changes_test(self, controller, parent):
        if len(self.first_meal) > 50 or len(self.first_link) > 500:
            ad_long_win = tk.Toplevel()
            ad_long_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
            ad_l = Frame(ad_long_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            ad_l.place(x=0)
            adi_l = Frame(ad_long_win, bg='black', width=diary_wid, height=diary_height)
            adi_l.place(x=0, y=0)
            self.lbd8 = ImageTk.PhotoImage \
                (Image.open("lbutt.png").resize((int(diary_height / 8), int(diary_height / 8))))

            ad_long_lab = Label(adi_l, fg='red', bg='black', text="CLOSE WINDOW",
                                font=("Courier", int(diary_height / 30)))
            ad_long_lab.place(x=diary_wid * .38, y=int(diary_height * 15 / 32))

            ad_long_button = tk.Button(adi_l, text="Close Window", image=self.lbd8,
                                       borderwidth=0, highlightthickness=0, command=ad_long_win.destroy)
            ad_long_button.place(x=diary_wid * .43, y=int(diary_height * 18 / 32))
            ad_long_button.image = self.lbd8

            if len(self.first_meal) > 50 and len(self.first_link) <= 500:
                labx = "Meal title maximum 50 characters"
            if len(self.first_meal) <= 50 and len(self.first_link) > 500:
                labx = "Link maximum 500 characters"
            if len(self.first_meal) > 50 and len(self.first_link) > 500:
                labx = "Meal title maximum 50 characters" "\n""Link maximum 500 characters"
            ad_lab = Label(adi_l, fg='red', bg='black', text=labx,
                           font=("Courier", int(diary_height / 30)))
            ad_lab.place(x=diary_wid * .2, y=int(diary_height * 10 / 32))
        else:
            self.make_first_changes(controller, parent)

    def make_first_changes(self, controller, parent):
        self.final_first_dict = dict(self.holding_dict_meal_new, **self.holding_dict_link_new, **self.holding_dict_new)
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        first_values = list(self.final_first_dict.values())
        count_f = len(first_values)
        sql = "INSERT INTO RecipeList VALUES(" + ",".join(count_f * ["?"]) + ")"
        c.execute(sql, first_values)
        conn.commit()
        c.execute("""DELETE FROM RecipeList WHERE meal == 'EnterRecipe'""")
        conn.commit()
        conn.close()
        for widget in self.opening_widgets:
            widget.destroy()
        for widget in self.opening_widgets_sb:
            widget.destroy()

        self.ft = screensize[1] / 15
        self.stop_rel=int(screensize[1]/3)
        self.adfrm1 = Frame(self, bg='black', width=int(screensize[0] / 4), height=int(screensize[1] / 3))
        self.adfrm1.place(relx=3 / 8, rely=3 / 10)

        self.lb16 = ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((int(screensize[1] / 16), int(screensize[1] / 16))))

        self.stop_rel = int(screensize[1] / 3)
        lbl = tk.Label(self.adfrm1, text="ADD ANOTHER RECIPE", fg='white', bg='black',
                       font=("Courier", int(screensize[0] / 70)))
        lbl.place(relx=.5, y=self.stop_rel*0.05, anchor="center")

        labb = Label(self.adfrm1, fg='red', bg='black', text="BACK TO HOMEPAGE",
                     font=("Courier", int(screensize[0] / 70)))
        labb.place(relx=.5, y=self.stop_rel*0.55, anchor="center")

        self.opening_widgets2.append(lbl)
        self.opening_widgets2.append(labb)
        self.opening_widgets2.append(self.adfrm1)

        first_button3 = tk.Button(self.adfrm1, text="Add another recipe?",
                          image=self.lb16, borderwidth=0, highlightthickness=0,
                          command=lambda: self.box_maker(controller, 0, parent))
        first_button3.place(relx=.5, y=self.stop_rel*0.25, anchor="center")
        first_button3.image = self.lb16

        first_button4 = tk.Button(self.adfrm1, text="Back to homepage",
                          image=self.lb16, borderwidth=0, highlightthickness=0,
                          command=refresh)
        first_button4.place(relx=.5, y=self.stop_rel*0.75, anchor='center')
        first_button4.image = self.lb16
        self.opening_widgets2.append(first_button3)
        self.opening_widgets2.append(first_button4)


    def box_maker(self, controller, x, parent):
        photoar = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
        ara = Label(self, image=photoar)
        ara.image = photoar
        ara.place(x=0, y=0, relwidth=1, relheight=1)

        awidt_master = int(screensize[0] / 3)
        awidt_wid = int(awidt_master / 3)
        self.awidt_tit = int(awidt_wid * 2)
        self.aht_master = int(screensize[1] * 0.8)
        self.aht_inside = int(self.aht_master / 13)
        aim = int(self.aht_inside / 2)
        frm_wid_place = awidt_master + self.awidt_tit

        self.ano_wid = len(self.names)
        self.ano_wids = len(self.names1) + 3
        self.for_wids = 2*self.aht_inside

        self.lba = ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((aim, aim)))

        s = shelve.open('test_shelf.db')
        cst = s['title_holder']
        nice_names = list(cst.values())
        nice_names1 = nice_names[2:]
        yy = self.for_wids + (.25*self.aht_inside)
        yv = 0.25*self.aht_inside
        cx = 0
        ccx = 0
        colours = ['green', 'black', 'red', 'green', 'black', 'red', 'green', 'black', 'red', 'green']
        colourswid = ['green', 'white', 'red', 'green', 'white', 'red', 'green', 'white', 'red', 'green']
        colourslab = ['white', 'white', 'green', 'white', 'red', 'green', 'white', 'red',
                    'green', 'white', 'red', 'green']


        for widget in self.opening_widgets2:
            widget.destroy()
        for widget in self.list_of_widgets:
            widget.destroy()
        for widget in self.opening_widgets_sbn:
            widget.destroy()
        self.holding_dict_meal = {}
        self.holding_dict_link = {}
        self.holding_dict = {}
        self.final_dict = {}

        self.afrm_tit = Frame(self, bg='black', width=self.awidt_tit, height=self.aht_inside * self.ano_wids)
        self.afrm_tit.place(x=int(screensize[0] / 3), y=int(screensize[1] * 0.1))

        afrm_wid = Frame(self, bg='black', width=awidt_wid, height=self.aht_inside * self.ano_wids)
        afrm_wid.place(x=frm_wid_place, y=int(screensize[1] * 0.1))

        afrmb = Frame(self, bg='black', width=self.aht_inside * 3.5, height=self.aht_inside)
        afrmb.place(x=int(screensize[0] * 0.4325), y=int((screensize[1] * 0.1) + self.aht_inside * self.ano_wids))

        meal_var = StringVar()
        meal_var.trace("w", lambda name, index, mode, sv1=meal_var: self.make_meal_dict(sv1, controller, parent))
        meal_entry = Entry(afrm_wid, textvariable=meal_var,
                           font=('Courier', int(self.aht_inside / 5)))
        meal_entry.place(relx=0, y=self.aht_inside*.25)
        link_var = StringVar()
        link_var.trace("w", lambda name, index, mode, sv2=link_var: self.make_link_dict(sv2, controller, parent))
        self.link_entry = Entry(afrm_wid, textvariable=link_var,
                                font=('Courier', int(self.aht_inside / 5)))
        self.link_entry.place(relx=0, y=self.aht_inside*1.25)
        self.opening_widgets2.append(self.link_entry)
        self.opening_widgets2.append(meal_entry)
        self.opening_widgets2.append(self.afrm_tit)
        self.opening_widgets2.append(afrmb)
        self.opening_widgets2.append(afrm_wid)

        for nice_item in self.add_nice_names:
            self.lbel = tk.Label(self.afrm_tit, text=nice_item, font=LARGE_FONT, bg='black', fg=colourslab[cx])
            self.lbel.place(relx=0, y=yv)
            yv += self.aht_inside
            cx += 1
            self.list_of_widgets.append(self.lbel)
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        for item in self.names1:
            s = shelve.open('test_shelf.db')
            op_lst = s['key1']
            options_list = op_lst[item]
            selected_var_am = StringVar()
            selected_var_am.trace("w", lambda name, index, mode, item = item,
                                      sv=selected_var_am: self.make_cat_dict(sv, item, controller, parent))
            self.abox = OptionMenu(afrm_wid, selected_var_am, *options_list)
            self.abox.config(bg=colourswid[ccx], font=("Courier", int(self.aht_inside / 5)))
            menu = self.nametowidget(self.abox.menuname)
            menu.config(font=("Courier", int(self.aht_inside / 5)), fg=colours[ccx])
            self.abox.place(relx=.25, y=yy)
            yy += self.aht_inside
            ccx +=1
            self.list_of_widgets.append(self.abox)
        conn.close()
        labba = Label(afrmb, fg='white', bg='black', text="BACK TO HOMEPAGE",
                      font=("Courier", int(self.aht_inside / 5)))
        labba.place(relx=.5, rely=0.15, anchor="center")

        am_button2 = tk.Button(afrmb, text="Back to homepage",
                               image=self.lba, borderwidth=0, highlightthickness=0,
                               command=lambda: self.box_maker(controller, 1, parent))
        am_button2.place(relx=.5, rely=.6, anchor="center")
        am_button2.image = self.lba

        self.list_of_widgets.append(labba)
        self.list_of_widgets.append(am_button2)
        self.list_of_widgets.append(meal_entry)
        if x == 1:
            controller.show_frame(StartPage, parent)

    def button_norm_func(self, controller, parent):
        for widget in self.opening_widgets_sbn:
            widget.destroy()

        self.ln4 = 0
        self.ln2 = 0

        self.ln1 = len(self.names1)

        for k in self.holding_dict_meal:
            if self.holding_dict_meal[k]:
                self.ln2 = 1

        self.ln3 = len(self.holding_dict.values())

        for k in self.holding_dict_link:
            if self.holding_dict_link[k]:
                self.ln4 = 1

        if self.ln2 != 0 and self.ln4 != 0 and self.ln1 == self.ln3 and 'empty' not in (self.holding_dict.values()):
            am_button1 = tk.Button(self.afrm_tit, text="Send Recipe", image=self.lba,
                        borderwidth=0, highlightthickness=0, command=lambda: self.make_changes_test(controller, parent))
            am_button1.place(relx=.675, y=(self.aht_inside * self.ano_wid) + self.aht_inside * .3)
            am_button1.image = self.lba

            labcs = Label(self.afrm_tit, fg='red', bg='black', text="SEND RECIPE",
                          font=("Courier", int(self.aht_inside / 5)))
            labcs.place(relx=.725, y=(self.aht_inside * self.ano_wid) + self.aht_inside * .05, anchor="center")

            self.opening_widgets_sbn.append(labcs)
            self.opening_widgets_sbn.append(am_button1)

    def make_cat_dict(self, sv, item, controller, parent):
        self.ctit= item
        self.vtit = sv.get()
        self.holding_dict[item] = self.vtit
        self.button_norm_func(controller, parent)

    def make_meal_dict(self, sv1, controller, parent):
        self.new_meal_title = sv1.get()
        self.holding_dict_meal["meal"] = self.new_meal_title
        wiff = list(self.holding_dict_meal.values())
        woff = (wiff[0].lstrip(' '))
        self.holding_dict_meal['meal'] = woff
        self.button_norm_func(controller, parent)

    def make_link_dict(self, sv2, controller, parent):
        self.new_link_title = sv2.get()
        self.holding_dict_link['link'] = self.new_link_title
        liff = list(self.holding_dict_link.values())
        loff = (liff[0].lstrip(' '))
        self.holding_dict_link['link'] = loff
        self.button_norm_func(controller, parent)

    def make_changes_test(self, controller, parent):
        if len(self.new_meal_title) >50 or len(self.new_link_title) >500:
            ad_long_win = tk.Toplevel()
            ad_long_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
            ad_l = Frame(ad_long_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            ad_l.place(x=0)
            adi_l = Frame(ad_long_win, bg='black', width=diary_wid, height=diary_height)
            adi_l.place(x=0, y=0)
            self.lbd8 = ImageTk.PhotoImage \
                (Image.open("lbutt.png").resize((int(diary_height / 8), int(diary_height / 8))))

            ad_long_lab = Label(adi_l, fg='red', bg='black', text="CLOSE WINDOW",
                                font=("Courier", int(diary_height / 30)))
            ad_long_lab.place(x=diary_wid * .38, y=int(diary_height * 15 / 32))

            ad_long_button = tk.Button(adi_l, text="Close Window", image=self.lbd8,
                                       borderwidth=0, highlightthickness=0, command=ad_long_win.destroy)
            ad_long_button.place(x=diary_wid * .43, y=int(diary_height * 18 / 32))
            ad_long_button.image = self.lbd8

            if len(self.new_meal_title) > 50 and len(self.new_link_title) <= 500:
                labx="Meal title maximum 50 characters"
            if len(self.new_meal_title) <= 50 and len(self.new_link_title) > 500:
                labx = "Link maximum 500 characters"
            if len(self.new_meal_title) > 50 and len(self.new_link_title) > 500:
                labx = "Meal title maximum 50 characters" "\n""Link maximum 500 characters"
            ad_lab = Label(adi_l, fg='red', bg='black', text=labx,
                           font=("Courier", int(diary_height / 30)))
            ad_lab.place(x=diary_wid * .2, y=int(diary_height * 10 / 32))
        else:
            self.make_changes(controller, parent)

    def make_changes(self, controller, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        self.final_dict = dict(self.holding_dict_meal, **self.holding_dict_link, **self.holding_dict)
        fin_values = list(self.final_dict.values())
        count = len(fin_values)
        sql = "INSERT INTO RecipeList VALUES(" + ",".join(count * ["?"]) + ")"
        c.execute(sql, fin_values)
        conn.commit()
        conn.close()
        self.holding_dict_meal = {}
        self.holding_dict = {}
        self.final_dict = {}
        for widget in self.opening_widgets2:
            widget.destroy()
        for widget in self.list_of_widgets:
            widget.destroy()
        for widget in self.opening_widgets_sbn:
            widget.destroy()

        self.ft = screensize[1] / 15
        self.adfrm1 = Frame(self, bg='black', width=int(screensize[0] / 4), height=screensize[1] / 3)
        self.adfrm1.place(relx=3 / 8, rely=3 / 10)

        self.lb16 = ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((int(screensize[1] / 16), int(screensize[1] / 16))))

        self.stop_rel = int(screensize[1] / 3)
        lbl = tk.Label(self.adfrm1, text="ADD ANOTHER RECIPE", fg='white', bg='black',
                               font=("Courier", int(screensize[0] / 70)))
        lbl.place(relx=.5, y=self.stop_rel*0.05, anchor="center")

        labb = Label(self.adfrm1, fg='red', bg='black', text="BACK TO HOMEPAGE",
                      font=("Courier", int(screensize[0] / 70)))
        labb.place(relx=.5, y=self.stop_rel*0.55, anchor="center")

        self.list_of_widgets.append(lbl)
        self.list_of_widgets.append(labb)
        self.list_of_widgets.append(self.adfrm1)


        butt3 = tk.Button(self.adfrm1, text="Add another recipe?",
                                       image=self.lb16, borderwidth=0, highlightthickness=0,
                                       command = lambda: self.box_maker(controller, 0, parent))
        butt3.place(relx=.5, y=self.stop_rel*0.25, anchor="center")
        butt3.image =self.lb16


        butt4 = tk.Button(self.adfrm1, text="Back to homepage",
                                  image=self.lb16, borderwidth=0, highlightthickness=0,
                                  command=refresh)
        butt4.place(relx=.5, y=self.stop_rel*0.75, anchor='center')
        butt4.image =self.lb16

        self.list_of_widgets.append(butt3)
        self.list_of_widgets.append(butt4)



class DeleteRecipe(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.list_of_widgets = []
        self.f1list_of_widgets = []
        self.frame = Frame(self)
        self.frame.place(x=5, y=5)
        self.frame2 = Frame(self)
        self.frame2.pack()
        self.ones_to_go = []
        self.lb8 = ImageTk.PhotoImage \
                (Image.open("lbutt.png").resize(
                (int(screensize[1] / 8), int(screensize[1] / 8))))
        self.lb16 = ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((int(screensize[1] / 16), int(screensize[1] / 16))))
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        cursor = conn.execute('select * FROM RecipeList')
        self.names = list(map(lambda x: x[0], cursor.description))
        conn.close()
        self.meal_box_maker(controller, 0, parent)

    def meal_box_maker(self, controller, x, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute('select meal from RecipeList')
        tester_value = c.fetchall()
        ex_tester = [i for word in tester_value for i in word]
        conn.close()
        if ex_tester == ['EnterRecipe']:
            photow = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
            wa = Label(self, image=photow)
            wa.image = photow
            wa.place(x=0, y=0, relwidth=1, relheight=1)
            frm50 = Frame(self, bg='black', width=wid, height=hei)
            frm50.place(x=xxx, y=yyy)
            frm60 = Frame(frm50, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            frm60.place(x=0)
            frm7 = Frame(frm50, bg='black', width=int(screensize[0] * 2 / 3), height=int(screensize[1] * 2 / 3))
            frm7.place(x=0, y=0)
            ran_empty = Label(frm7, fg='green', bg='black', text="ENTER A RECIPE FIRST",
                              font=("Courier", int(erht_inside)))
            ran_empty.place(relx=0.5, rely=0.25, anchor="center")
            ran_cl = Label(frm7, fg='white', bg='black', text="BACK TO HOMEPAGE",
                           font=("Courier", int(erht_inside)))
            ran_cl.place(relx=0.5, rely=0.5, anchor="center")

            ran_em_button_m = tk.Button(frm7, text="Back to homepage", image=self.lb8, borderwidth=0,
                                        highlightthickness=0, command=lambda: controller.show_frame(StartPage, parent))
            ran_em_button_m.place(relx=0.5, rely=0.75, anchor="center")
            ran_em_button_m.image = self.lb8
        else:
            for widget in self.f1list_of_widgets:
                widget.destroy()
            conn = sqlite3.connect('master.db')
            c = conn.cursor()
            c.execute("""SELECT meal FROM RecipeList""")
            am_full_book = c.fetchall()
            conn.close()
            am_exploded_list = ([item for t in am_full_book for item in t])

            photoar = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
            ara = Label(self, image=photoar)
            ara.image = photoar
            ara.place(x=0, y=0, relwidth=1, relheight=1)


            self.dfrm = Frame(self, bg='black', width=int(screensize[0]/3), height=screensize[1])
            self.dfrm.place(relx=2/3, rely=1/10)

            self.dfrmt = Frame(self, bg='black', width=int(screensize[0] / 3.25), height=screensize[1]/10)
            self.dfrmt.place(relx=2 / 3, rely=0)

            self.dfrmbt = Frame(self, bg='black', width=int(screensize[0] / 4), height=screensize[1] / 4)
            self.dfrmbt.place(relx=0.33, rely=0.4)

            labd = Label(self.dfrmt, fg='white', bg='black', text="SELECT RECIPES TO DELETE",
                          font=("Courier", int(screensize[1]/ 52)))
            labd.place(relx=.5, rely=.5, anchor="center")

            self.listbox = Listbox(self.dfrm, selectmode = "multiple", width=35, height=50, fg = 'white', bg = "black")
            self.listbox.pack(side='left', fill='y')
            scrollbar = Scrollbar(self.dfrm, orient="vertical", command=self.listbox.yview)
            scrollbar.pack(side="right", fill="y")

            labdd = Label(self.dfrmbt, fg='white', bg='black', text="DELETE RECIPES",
                          font=("Courier", int(screensize[0] / 70)))
            labdd.place(relx=.5, rely=0.15, anchor="center")

            labdb = Label(self.dfrmbt, fg='red', bg='black', text="BACK TO HOMEPAGE",
                          font=("Courier", int(screensize[0] / 70)))
            labdb.place(relx=.5, rely=0.65, anchor="center")

            delete_button1 = tk.Button(self.dfrmbt, text = 'delete',
                                       image=self.lb16, borderwidth=0, highlightthickness=0,
                                       command=lambda: self.delete_meal(controller, parent))
            delete_button1.place(relx = .5, rely = 0.35, anchor='center')
            delete_button1.image = self.lb16

            delete_button2 = tk.Button(self.dfrmbt, text="Back to homepage",image=self.lb16,
                                       borderwidth=0, highlightthickness=0,
                                       command=lambda: self.meal_box_maker(controller, 1, parent))
            delete_button2.place(relx=.5, rely=0.85, anchor='center')
            delete_button2.image = self.lb16


            self.listbox.insert(END, *am_exploded_list)
            self.listbox.config(yscrollcommand=scrollbar.set, font=("Courier", int(screensize[1] / 52)))
            self.listbox.bind('<<ListboxSelect>>', lambda event: self.list_of_selected())
            self.f1list_of_widgets.append(self.listbox)
            self.f1list_of_widgets.append(self.dfrm)
            self.f1list_of_widgets.append(self.dfrmt)
            self.f1list_of_widgets.append(labdd)
            self.f1list_of_widgets.append(labdb)
            self.f1list_of_widgets.append(labd)
            self.f1list_of_widgets.append(delete_button1)
            self.f1list_of_widgets.append(delete_button2)
            self.f1list_of_widgets.append(scrollbar)
            if x == 1:
                controller.show_frame(StartPage, parent)

    def list_of_selected(self):
        self.ones_to_go = []
        selcted_indices = self.listbox.curselection()
        lst_select = list(selcted_indices)
        for mealy in lst_select:
            self.ones_to_go.append(self.listbox.get(mealy))

    def delete_meal(self, controller, parent):
        listie = []
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        for i in self.ones_to_go:
            c.execute("DELETE FROM RecipeList WHERE meal =?", (i,))
            conn.commit()
        conn.close()
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute("select * from RecipeList")
        ch = c.fetchall()
        for widget in self.f1list_of_widgets:
            widget.destroy()
        if len(ch) != 0:
            labdd1 = Label(self.dfrmbt, fg='white', bg='black', text="DELETE ANOTHER RECIPE",
                          font=("Courier", int(screensize[0] / 70)))
            labdd1.place(relx=.5, rely=0.15, anchor="center")

            labdb1 = Label(self.dfrmbt, fg='red', bg='black', text="BACK TO HOMEPAGE",
                          font=("Courier", int(screensize[0] / 70)))
            labdb1.place(relx=.5, rely=0.65, anchor="center")
            self.f1list_of_widgets.append(labdd1)
            self.f1list_of_widgets.append(labdb1)
            self.f1list_of_widgets.append(self.dfrmbt)

            dbutt3 = tk.Button(self.dfrmbt, text="Delete another recipe?",
                               image=self.lb16, borderwidth=0, highlightthickness=0,
                          command=lambda: self.meal_box_maker(controller, 0, parent))
            dbutt3.place(relx=.5, rely=0.35, anchor='center')
            dbutt3.image =self.lb16

            self.f1list_of_widgets.append(dbutt3)
        else:
            for colo in self.names:
                listie.append("EnterRecipe")
            count = len(self.names)
            sql = "INSERT INTO RecipeList VALUES(" + ",".join(count * ["?"]) + ")"
            c.execute(sql, listie)
            conn.commit()
        conn.close()

        labdb2 = Label(self.dfrmbt, fg='red', bg='black', text="BACK TO HOMEPAGE",
                       font=("Courier", int(screensize[0] / 70)))
        labdb2.place(relx=.5, rely=0.65, anchor="center")
        dbutt4 = tk.Button(self.dfrmbt, text="Back to homepage", image=self.lb16,
                           borderwidth=0, highlightthickness=0, command=refresh)
        dbutt4.place(relx=.5, y=(int(screensize[1] / 4)*0.85), anchor='center')
        dbutt4.image = self.lb16
        self.f1list_of_widgets.append(dbutt4)
        self.f1list_of_widgets.append(labdb2)


class AddColumn(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.ac_list_of_widgets = []
        self.frame = Frame(self)
        self.frame.place(x=5, y=5)
        self.frame2 = Frame(self)
        self.frame2.pack()
        self.ones_to_go = []
        self.title_adder = {}
        self.title_to_add = {}
        self.default_adder = {}
        self.default_to_add = {}
        self.options_adder = {}
        self.options_menu = []
        self.ac_list_of_widgets_op = []
        self.ac_list = []
        self.lbd8 = ImageTk.PhotoImage \
                (Image.open("lbutt.png").resize(
                (int(diary_height / 8), int(diary_height / 8))))
        self.lb16 = ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((int(screensize[1] / 16), int(screensize[1] / 16))))
        self.options_to_add = {}
        self.ac_ob_list_of_widgets = []
        self.create_widgets(controller, 0, parent)

    def create_widgets(self, controller, x, parent):
        for widget in self.ac_list_of_widgets:
            widget.destroy()
        for widget in self.ac_list:
            widget.destroy()
        photoar = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
        ara = Label(self, image=photoar)
        ara.image = photoar
        ara.place(x=0, y=0, relwidth=1, relheight=1)
        self.ft = screensize[1]/15
        self.acfrm = Frame(self, bg='black', width=int(screensize[0] / 4), height=screensize[1]/3)
        self.acfrm.place(relx=3/8, rely=3/10)

        self.acrmt = Frame(self, bg='black', width=int(screensize[0] / 4), height=screensize[1] / 10)
        self.acrmt.place(relx=3/8, rely=1/5)

        self.cwlbel = tk.Label(self.acrmt, text="ENTER NEW ATTRIBUTE", fg='white', bg='black',
                               font=("Courier", int(screensize[0] / 70)))
        self.cwlbel.place(relx=.5, rely=0.25, anchor="center")

        self.new_column_box = Entry(self.acrmt, width = int(screensize[0]/100),
                                    font = ("Courier", int(screensize[0] / 70)))
        self.new_column_box.place(relx=.5, rely=0.75, anchor="center")

        labse = Label(self.acfrm, fg='white', bg='black', text="SEND",
                         font=("Courier", int(screensize[0] / 70)))
        labse.place(relx=.5, rely=0.15, anchor="center")

        alabb = Label(self.acfrm, fg='red', bg='black', text="BACK TO HOMEPAGE",
                         font=("Courier", int(screensize[0] / 70)))
        alabb.place(relx=.5, rely=0.65, anchor="center")

        self.new_col_but = tk.Button(self.acfrm, text="Send", image=self.lb16, borderwidth=0, highlightthickness=0,
                                         command=lambda: self.tester(controller, parent))
        self.new_col_but.place(relx=.5, rely=0.35, anchor='center')
        self.new_col_but.image = self.lb16

        bh_button = tk.Button(self.acfrm, text="Back to homepage",
                                image=self.lb16, borderwidth=0, highlightthickness=0,
                                command=lambda: self.create_widgets(controller, 1, parent))
        bh_button.place(relx=.5, rely=0.85, anchor='center')
        bh_button.image = self.lb16

        self.ac_list_of_widgets.append(self.cwlbel)
        self.ac_list_of_widgets.append(labse)
        self.ac_list_of_widgets.append(alabb)
        self.ac_list_of_widgets.append(bh_button)
        self.ac_list_of_widgets.append(self.new_col_but)
        self.ac_list_of_widgets.append(self.new_column_box)

        if x==1:
            controller.show_frame(StartPage, parent)


    def tester(self, controller, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        cursor = conn.execute('select * FROM RecipeList')
        conn.close()
        self.testes = self.new_column_box.get()
        self.names = list(map(lambda x: x[0], cursor.description))
        if not self.testes:
            ad_long_win = tk.Toplevel()
            ad_long_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
            ad_l = Frame(ad_long_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            ad_l.place(x=0)
            adi_l = Frame(ad_long_win, bg='black', width=diary_wid, height=diary_height)
            adi_l.place(x=0, y=0)
            ad_lab = Label(adi_l, fg='red', bg='black', text="It's empty, try again!",
                           font=("Courier", int(diary_height / 30)))
            ad_lab.place(x=int(diary_wid * 0.28), y=int(diary_height * 10 / 32))

            ad_long_lab = Label(adi_l, fg='red', bg='black', text="CLOSE WINDOW",
                                font=("Courier", int(diary_height / 30)))
            ad_long_lab.place(x=diary_wid * .38, y=int(diary_height * 15 / 32))

            ad_long_button = tk.Button(adi_l, text="Close Window", image=self.lbd8,
                                       borderwidth=0, highlightthickness=0, command=ad_long_win.destroy)
            ad_long_button.place(x=diary_wid * .43, y=int(diary_height * 18 / 32))
            ad_long_button.image = self.lbd8
        else:
            self.tester_big(controller, parent)

    def tester_big(self, controller, parent):
        if len(self.names) > 9:
            ad_long_win = tk.Toplevel()
            ad_long_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
            ad_l = Frame(ad_long_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            ad_l.place(x=0)
            adi_l = Frame(ad_long_win, bg='black', width=diary_wid, height=diary_height)
            adi_l.place(x=0, y=0)

            ad_lab = Label(adi_l, fg='red', bg='black', text="Too many attributes, delete another first",
                           font=("Courier", int(diary_height / 30)))
            ad_lab.place(x=int(diary_wid * 0.1), y=int(diary_height * 10 / 32))

            ad_long_lab = Label(adi_l, fg='red', bg='black', text="CLOSE WINDOW",
                                font=("Courier", int(diary_height / 30)))
            ad_long_lab.place(x=diary_wid * .38, y=int(diary_height * 15 / 32))

            ad_long_button = tk.Button(adi_l, text="Close Window", image=self.lbd8,
                                       borderwidth=0, highlightthickness=0, command=ad_long_win.destroy)
            ad_long_button.place(x=diary_wid * .43, y=int(diary_height * 18 / 32))
            ad_long_button.image = self.lbd8
        else:
            self.tester_exists(controller, parent)

    def tester_exists(self, controller, parent):
        if self.testes in self.names:
            ad_long_win = tk.Toplevel()
            ad_long_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
            ad_l = Frame(ad_long_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            ad_l.place(x=0)
            adi_l = Frame(ad_long_win, bg='black', width=diary_wid, height=diary_height)
            adi_l.place(x=0, y=0)
            ad_lab = Label(adi_l, fg='red', bg='black', text="That attribute already exists",
                           font=("Courier", int(diary_height / 30)))
            ad_lab.place(x=int(diary_wid * 0.2), y=int(diary_height * 10 / 32))

            ad_long_lab = Label(adi_l, fg='red', bg='black', text="CLOSE WINDOW",
                                font=("Courier", int(diary_height / 30)))
            ad_long_lab.place(x=diary_wid * .38, y=int(diary_height * 15 / 32))

            ad_long_button = tk.Button(adi_l, text="Close Window", image=self.lbd8,
                                       borderwidth=0, highlightthickness=0, command=ad_long_win.destroy)
            ad_long_button.place(x=diary_wid * .43, y=int(diary_height * 18 / 32))
            ad_long_button.image = self.lbd8
        else:
            self.tester_long(controller, parent)

    def tester_long(self, controller, parent):
        if len(self.testes ) > 50:
            ad_long_win = tk.Toplevel()
            ad_long_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
            ad_l = Frame(ad_long_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            ad_l.place(x=0)
            adi_l = Frame(ad_long_win, bg='black', width=diary_wid, height=diary_height)
            adi_l.place(x=0, y=0)
            ad_lab = Label(adi_l, fg='red', bg='black', text="New attribute maximum of 50 characters",
                           font=("Courier", int(diary_height / 30)))
            ad_lab.place(x=int(diary_wid * 0.1), y=int(diary_height * 10 / 32))

            ad_long_lab = Label(adi_l, fg='red', bg='black', text="CLOSE WINDOW",
                                font=("Courier", int(diary_height / 30)))
            ad_long_lab.place(x=diary_wid * .38, y=int(diary_height * 15 / 32))

            ad_long_button = tk.Button(adi_l, text="Close Window", image=self.lbd8,
                                       borderwidth=0, highlightthickness=0, command=ad_long_win.destroy)
            ad_long_button.place(x=diary_wid * .43, y=int(diary_height * 18 / 32))
            ad_long_button.image = self.lbd8
        else:
            self.make_col_name(controller, parent)

    def make_col_name(self, controller, parent):
        self.new_column = self.new_column_box.get()
        self.create_opts(controller, 0, parent)

    def create_opts(self, controller, a, parent):
        for widget in self.ac_list_of_widgets:
            widget.destroy()

        self.cwlbel1 = tk.Label(self.acrmt, text="Enter options to choose from" + "\n" + "one at a time!"
                                             " eg - yes", fg='white', bg='black',
                               font=("Courier", int(screensize[0] / 100)))
        self.cwlbel1.place(relx=.5, rely=0.25, anchor="center")


        labso = Label(self.acfrm, fg='white', bg='black', text="SEND OPTION",
                      font=("Courier", int(screensize[0] / 70)))
        labso.place(relx=.5, rely=0.15, anchor="center")

        labad = Label(self.acfrm, fg='red', bg='black', text="ALL DONE",
                      font=("Courier", int(screensize[0] / 70)))
        labad.place(relx=.5, rely=0.6, anchor="center")

        self.new_col_button0 = tk.Button(self.acfrm, text="Send Option", image=self.lb16, borderwidth=0,
                                     highlightthickness=0,
                                     command=lambda: self.tester1(controller, parent))
        self.new_col_button0.place(relx=.5, rely=0.35, anchor='center')
        self.new_col_button0.image = self.lb16

        self.new_col_button1 = tk.Button(self.acfrm, text="All Done",
                              image=self.lb16, borderwidth=0, highlightthickness=0,
                              command=lambda: self.add_the_column(controller, parent))
        self.new_col_button1.place(relx=.5, rely=0.8, anchor='center')
        self.new_col_button1.image = self.lb16

        self.acfrm1 = Frame(self, bg='black', width=int(screensize[0] / 4), height=screensize[1] / 6)
        self.acfrm1.place(relx=3 / 8, rely=19/30)


        labba = Label(self.acfrm1, fg='green', bg='black', text="BACK TO HOMEPAGE",
                      font=("Courier", int(screensize[0] / 70)))
        labba.place(relx=.5, rely=0.25, anchor="center")

        self.new_col_button2 = tk.Button(self.acfrm1, text="Back to homepage",
                              image=self.lb16, borderwidth=0, highlightthickness=0,
                              command=lambda: self.create_widgets(controller, 1, parent))
        self.new_col_button2.place(relx=.5, rely=0.65, anchor='center')
        self.new_col_button2.image = self.lb16

        self.ac_list_of_widgets.append(self.acfrm)
        self.ac_list_of_widgets.append(self.acfrm1)
        self.ac_list_of_widgets.append(self.acrmt)
        self.ac_list_of_widgets.append(labso)
        self.ac_list_of_widgets.append(labba)
        self.ac_list_of_widgets.append(labad)
        self.ac_list_of_widgets.append(self.cwlbel1)
        self.ac_list_of_widgets.append(self.new_col_button0)
        self.ac_list_of_widgets.append(self.new_col_button1)
        self.ac_list_of_widgets.append(self.new_col_button2)
        self.opts_box(controller, 0, parent)

    def opts_box(self, controller, a, parent):
        if a == 1:
            for widget in self.ac_list_of_widgets_op:
                widget.destroy()
        self.new_column_box1 = Entry(self.acrmt,
                                    font=("Courier", int(screensize[0] / 70)))
        self.new_column_box1.place(relx=.5, rely=0.75, anchor="center")
        self.ac_list_of_widgets_op.append(self.new_column_box1)

    def tester1(self, controller, parent):
        self.testes1 = self.new_column_box1.get()
        if self.testes1 in self.options_menu:
            ad_long_win = tk.Toplevel()
            ad_long_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
            ad_l = Frame(ad_long_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            ad_l.place(x=0)
            adi_l = Frame(ad_long_win, bg='black', width=diary_wid, height=diary_height)
            adi_l.place(x=0, y=0)
            ad_lab = Label(adi_l, fg='red', bg='black', text="That Option Already Exists",
                           font=("Courier", int(diary_height / 30)))
            ad_lab.place(relx=0.25, y=int(diary_height * 10 / 32))

            ad_long_lab = Label(adi_l, fg='red', bg='black', text="CLOSE WINDOW",
                                font=("Courier", int(diary_height / 30)))
            ad_long_lab.place(x=diary_wid * .38, y=int(diary_height * 15 / 32))

            ad_long_button = tk.Button(adi_l, text="Close Window", image=self.lbd8,
                                       borderwidth=0, highlightthickness=0, command=ad_long_win.destroy)
            ad_long_button.place(x=diary_wid * .43, y=int(diary_height * 18 / 32))
            ad_long_button.image = self.lbd8
        else:
            self.tester1_long(controller, parent)

    def tester1_long(self, controller, parent):
        if len(self.testes1) >50 or len(self.testes1) ==0:
            ad_long_win = tk.Toplevel()
            ad_long_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
            ad_l = Frame(ad_long_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            ad_l.place(x=0)
            adi_l = Frame(ad_long_win, bg='black', width=diary_wid, height=diary_height)
            adi_l.place(x=0, y=0)

            ad_long_lab = Label(adi_l, fg='red', bg='black', text="CLOSE WINDOW",
                                font=("Courier", int(diary_height / 30)))
            ad_long_lab.place(x=diary_wid * .38, y=int(diary_height * 15 / 32))

            ad_long_button = tk.Button(adi_l, text="Close Window", image=self.lbd8,
                                       borderwidth=0, highlightthickness=0, command=ad_long_win.destroy)
            ad_long_button.place(x=diary_wid * .43, y=int(diary_height * 18 / 32))
            ad_long_button.image = self.lbd8
            if len(self.testes1) >50:
                opx = "Maximum Length 50 Characters"
            if len(self.testes1) <= 50:
                opx = "Please Fill in the Option Box"
            ad_lab = Label(adi_l, fg='red', bg='black', text=opx,
                           font=("Courier", int(diary_height / 30)))
            ad_lab.place(relx=0.23, y=int(diary_height * 10 / 32))
        else:
            self.options_menu.append(self.testes1)
            self.opts_box(controller, 1, parent)

    def add_the_column(self, controller, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        not_nice_new_column = self.new_column.replace(" ", "")
        options_menu_tester = len(self.options_menu)
        new_column_tester = len(self.new_column)
        if options_menu_tester == 0 or new_column_tester == 0:
            for widget in self.ac_list_of_widgets:
                widget.destroy()
            self.atclbel = tk.Label(self.acrmt, text="Fill both boxes, Click to Start Again", fg='white',
                                     bg='black',
                                     font=("Courier", int(screensize[0] / 70)))
            self.atclbel.place(relx=.5, rely=0.5, anchor="center")
            self.ac_list_of_widgets.append(self.atclbel)
            self.at_col_button3 = tk.Button(self.acrmt, text="Start Again",
                                            image=self.lb16, borderwidth=0, highlightthickness=0,
                                            command=lambda: self.create_widgets(controller, 0, parent))
            self.at1_col_button3.place(relx=.5, rely=0.85, anchor='center')
            self.at1_col_button3.image = self.lb16
            self.ac_list_of_widgets.append(self.atclbel)
            self.ac_list_of_widgets.append(self.at1_col_button3)

        else:
            c.execute("""alter table RecipeList add """"" + not_nice_new_column + """""")
            conn.commit()
            conn.close()

            self.title_to_add = {not_nice_new_column: self.new_column}
            s = shelve.open('test_shelf.db')
            self.title_adder = s['title_holder']
            self.title_adder.update(self.title_to_add)
            s = shelve.open('test_shelf.db')
            del s['title_holder']
            s = shelve.open('test_shelf.db')
            s['title_holder'] = self.title_adder

            self.default_to_add = {not_nice_new_column: {'Any': 1}}
            s = shelve.open('test_shelf.db')
            self.default_adder = s['default_holder']
            self.default_adder.update(self.default_to_add)
            s = shelve.open('test_shelf.db')
            del s['default_holder']
            s = shelve.open('test_shelf.db')
            s['default_holder'] = self.default_adder

            self.options_to_add = {not_nice_new_column: self.options_menu}
            s = shelve.open('test_shelf.db')
            self.options_adder = s['key1']
            self.options_adder.update(self.options_to_add)
            s = shelve.open('test_shelf.db')
            del s['key1']
            s = shelve.open('test_shelf.db')
            s['key1'] = self.options_adder
            self.destroy_create(not_nice_new_column, controller, parent)

    def destroy_create(self, not_nice_new_column, controller, parent):
        for widget in self.ac_list_of_widgets:
            widget.destroy()
        for widget in self.ac_list_of_widgets_op:
            widget.destroy()
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute("SELECT meal FROM RecipeList")
        self.meal_for_new_values = c.fetchall()
        conn.close()
        self.ct = 0
        for m in self.meal_for_new_values:
            if m[0] == "EnterRecipe":
                nc_pl_button_m = tk.Button(self, text="Back to homepage",
                                           command=refresh)
                nc_pl_button_m.pack()
            else:
                self.ct += 1
                self.make_widgets(*m, not_nice_new_column)

    def make_widgets(self, m, not_nice_new_column):
        placew=int(screensize[0]*3/8)
        placeh=int(screensize[1] / 3)
        wid=int(screensize[0] / 4)
        he = int(screensize[1] / 3)
        self.frmx = Frame(self, bg='black', width=wid, height=he)
        self.frmx.place(x=placew, y=placeh)

        self.mw_meal_lb = tk.Label(self.frmx, text=m, fg = 'green',
                                   bg = 'black', font = ("Courier", int(screensize[0] / 70)))
        self.mw_meal_lb.place(x=(wid/2), y=(he*2/20),anchor='center')

        self.mw_meal_lb1 = tk.Label(self.frmx, text=self.testes, fg='white',
                                   bg='black', font=("Courier", int(screensize[0] / 70)))
        self.mw_meal_lb1.place(x=(wid/2), y=(he*5/20), anchor='center')

        var = StringVar()

        self.mw_box= OptionMenu(self.frmx, var, *self.options_menu)
        self.mw_box.config(bg='white', font=("Courier", int(screensize[0] / 70)))
        menu = self.nametowidget(self.mw_box.menuname)
        menu.config(fg='black', font=("Courier", int(screensize[0] / 90)))
        self.mw_box.place(relx=.5, y=(he*9/20), anchor = 'center')

        self.mw_meal_lb2 = tk.Label(self.frmx, text='SEND', fg='red',
                                    bg='black', font=("Courier", int(screensize[0] / 70)))
        self.mw_meal_lb2.place(relx=.5, y=(he*13/20), anchor = 'center')

        swait_var = tk.IntVar()
        self.mw_button = tk.Button(self.frmx, text="Send", image=self.lb16, borderwidth=0, highlightthickness=0,
                                   command = lambda: swait_var.set(1))
        self.mw_button.place(relx=.5, y=(he*16/20), anchor = 'center')
        self.mw_button.image = self.lb16
        swait_var = tk.IntVar()
        self.mw_button.wait_variable(swait_var)


        self.ac_list_of_widgets.append(self.mw_meal_lb)
        self.ac_list_of_widgets.append(self.mw_box)
        self.ac_list_of_widgets.append(self.mw_meal_lb1)
        self.ac_list_of_widgets.append(self.mw_meal_lb2)
        self.ac_list_of_widgets.append(self.mw_button)
        self.updater(not_nice_new_column, var, m)

    def updater(self, not_nice_new_column, var, m):
        for widget in self.ac_list_of_widgets:
            widget.destroy()
        option_choice = var.get()
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute("UPDATE RecipeList SET " + not_nice_new_column + " = (?) "
                                                                           "WHERE meal = (?)", (option_choice, m))
        conn.commit()
        conn.close()
        if self.ct == len(self.meal_for_new_values):
            self.dc_meal_lb = tk.Label(self.frmx, text="Book updated", fg='green',
                                        bg='black', font=("Courier", int(screensize[0] / 70)))
            self.dc_meal_lb.place(relx=.5, rely=0.15, anchor="center")

            self.dc_meal_lb2 = tk.Label(self.frmx, text='BACK TO HOMEPAGE', fg='red',
                                        bg='black', font=("Courier", int(screensize[0] / 70)))
            self.dc_meal_lb2.place(relx=.5, rely=0.59, anchor="center")

            self.dc_button = tk.Button(self.frmx, text="Back to homepage", image = self.lb16,
                                       borderwidth = 0, highlightthickness = 0, command=refresh)
            self.dc_button.place(relx=.5, rely=0.81, anchor="center")
            self.dc_button.image = self.lb16
            self.ac_list_of_widgets.append(self.dc_meal_lb)
            self.ac_list_of_widgets.append(self.dc_meal_lb2)
            self.ac_list_of_widgets.append(self.dc_button)
            self.ac_list.append(self.frmx)


class DeleteColumn(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.ac_list_of_widgets = []
        self.one_to_del = []
        self.names = []
        self.lbdel_get = []
        self.columns_to_stay = []
        self.dl_list_of_widgets = []
        self.options_dict = {}
        self.set_list = set()
        self.title_deleter = {}
        self.default_deleter = {}
        self.options_deleter = {}
        self.lb16= ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((int(screensize[1] / 16), int(screensize[1] / 16))))
        self.midbox = []
        self.create_temp(controller, parent)


    def create_temp(self, controller, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute("""BEGIN TRANSACTION""")
        c.execute("""CREATE TABLE IF NOT EXISTS rl_backup (meal)""")
        conn.commit()
        conn.close()
        self.cols_to_stay(controller, parent)

    def cols_to_stay(self, controller, parent):
        photoar = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
        ara = Label(self, image=photoar)
        ara.image = photoar
        ara.place(x=0, y=0, relwidth=1, relheight=1)

        self.hmidbox = int(screensize[1]/4)
        self.wmidbox = int(screensize[0]/4)

        self.dcfrm = Frame(self, bg='black', width=int(screensize[0] / 4), height=screensize[1])
        self.dcfrm.place(relx=0, y = screensize[1]/ 10)

        self.dcfrmt = Frame(self, bg='black', width=int(screensize[0] / 4), height=screensize[1] / 10)
        self.dcfrmt.place(x=0, y=0)

        self.dcfrmbt = Frame(self, bg='black', width=self.wmidbox, height=self.hmidbox)
        self.dcfrmbt.place(x=int(screensize[0]/3), y=int((screensize[1]*.4)))

        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        del_cursor = conn.execute('select * FROM RecipeList')
        self.names = list(map(lambda x: x[0], del_cursor.description))
        conn.close()
        self.names1 = self.names[1:]
        self.names2 = self.names[2:]

        self.delc_meal_lb = tk.Label(self.dcfrmt, fg='white', bg='black',
                                    text="Category to Delete", font=("Courier", int(screensize[1] / 52)))
        self.delc_meal_lb.place(relx=.5, rely=.5, anchor="center")


        self.delc_listbox = Listbox(self.dcfrm, selectmode="single", height=50, fg='white', bg="black",
                                    borderwidth = 0, highlightthickness = 0)
        self.delc_listbox.place(x=0, y=0)

        dclab = Label(self.dcfrmbt, fg='white', bg='black', text="SEND CATEGORY",
                         font=("Courier", int(screensize[0] / 70)))
        dclab.place(relx=.5, y=self.hmidbox*0.15, anchor="center")

        self.dclabb = Label(self.dcfrmbt, fg='red', bg='black', text="BACK TO HOMEPAGE",
                         font=("Courier", int(screensize[0] / 70)))
        self.dclabb.place(relx=.5, y=self.hmidbox*0.65, anchor="center")

        delete_col_button1 = tk.Button(self.dcfrmbt, text="Send changes",
                                       image = self.lb16, borderwidth = 0, highlightthickness = 0,
                                       command=lambda: self.create_columns_in_temp())
        delete_col_button1.place(relx=.5, y=self.hmidbox*0.35, anchor='center')
        delete_col_button1.image =self.lb16

        delete_col_button2 = tk.Button(self.dcfrmbt, text="Back to homepage", image = self.lb16,
                                       borderwidth = 0, highlightthickness = 0,
                                   command=lambda: controller.show_frame(StartPage, parent))
        delete_col_button2.place(relx=.5, y=self.hmidbox*0.85, anchor='center')
        delete_col_button2.image = self.lb16

        self.delc_listbox.insert(END, *self.names2)
        self.delc_listbox.config(font=("Courier", int(screensize[1] / 52)))
        self.delc_listbox.bind('<<ListboxSelect>>', lambda event: self.selected_col())
        self.dl_list_of_widgets.append(self.delc_meal_lb)
        self.dl_list_of_widgets.append(self.dcfrm)
        self.dl_list_of_widgets.append(self.dcfrmt)
        self.dl_list_of_widgets.append(dclab)
        self.dl_list_of_widgets.append(self.delc_listbox)
        self.dl_list_of_widgets.append(delete_col_button1)
        self.dl_list_of_widgets.append(delete_col_button2)

        self.midbox.append(self.dcfrmbt)
        self.midbox.append(self.dclabb)

    def selected_col(self):
        lbdel_items = self.delc_listbox.curselection()
        self.lbdel_get = self.delc_listbox.get(lbdel_items)

    def create_columns_in_temp(self):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        self.columns_to_stay = [x for x in self.names1 if x not in self.lbdel_get]
        for column in self.columns_to_stay:
            c.execute("""alter table rl_backup add """"" + column + """""")
            conn.commit()
        conn.close()
        self.delete_dicts()

    def delete_dicts(self):
        s = shelve.open('test_shelf.db')
        self.title_deleter = s['title_holder']
        if self.lbdel_get in self.title_deleter:
            del self.title_deleter[self.lbdel_get]
            s = shelve.open('test_shelf.db')
            del s['title_holder']
            s = shelve.open('test_shelf.db')
            s['title_holder'] = self.title_deleter

        s = shelve.open('test_shelf.db')
        self.default_deleter = s['default_holder']
        if self.lbdel_get in self.default_deleter:
            del self.default_deleter[self.lbdel_get]
            s = shelve.open('test_shelf.db')
            del s['default_holder']
            s = shelve.open('test_shelf.db')
            s['default_holder'] = self.default_deleter

        s = shelve.open('test_shelf.db')
        self.options_deleter = s['key1']
        if self.lbdel_get in self.options_deleter:
            del self.options_deleter[self.lbdel_get]
            s = shelve.open('test_shelf.db')
            del s['key1']
            s = shelve.open('test_shelf.db')
            s['key1'] = self.options_deleter
        self.insert_data_into_temp()

    def insert_data_into_temp(self):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        ins_cursor = conn.execute('select * FROM rl_backup')
        inames = list(map(lambda x: x[0], ins_cursor.description))
        inames.pop(0)
        c.execute("""INSERT INTO rl_backup (meal) SELECT meal FROM RecipeList""")
        conn.commit()
        c.execute("""Select meal FROM rl_backup""")
        meals_moved = c.fetchall()
        list_meals_moved = [i[0] for i in meals_moved]
        for meal in list_meals_moved:
            for column in inames:
                c.execute("""UPDATE rl_backup SET (""" + column + """)
                = (SELECT """ + column + """ FROM RecipeList WHERE meal =(?)) WHERE meal == (?)""", (meal, meal))
                conn.commit()
        conn.close()
        self.delete_original()

    def delete_original(self):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute("""BEGIN TRANSACTION""")
        c.execute("""DROP TABLE RecipeList""")
        conn.commit()
        conn.close()
        self.create_new_original()

    def create_new_original(self):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute("""BEGIN TRANSACTION""")
        c.execute("""CREATE TABLE RecipeList (meal)""")
        conn.commit()
        conn.close()
        self.add_rest_of_columns()

    def add_rest_of_columns(self):
        conn = sqlite3.connect('master.db')
        add_cursor = conn.execute('select * FROM rl_backup')
        c = conn.cursor()
        binames = list(map(lambda x: x[0], add_cursor.description))
        binames.pop(0)
        for column in binames:
            c.execute("""alter table RecipeList add """"" + column + """""")
            conn.commit()
        conn.close()
        self.populate_new_original()

    def populate_new_original(self):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute("""BEGIN TRANSACTION""")
        c.execute("""INSERT INTO RecipeList SELECT * FROM rl_backup""")
        conn.commit()
        conn.close()
        self.delete_temp_again()

    def delete_temp_again(self):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute("""BEGIN TRANSACTION""")
        c.execute("""DROP TABLE rl_backup""")
        conn.commit()
        conn.close()
        self.make_back_page()

    def make_back_page(self):
        for widget in self.dl_list_of_widgets:
            widget.place_forget()

        delt_meal_lb = tk.Label(self.dcfrmbt, fg='white', bg='black', text="Column deleted",
                                font=("Courier", int(screensize[0] / 70)))
        delt_meal_lb.place(relx=.5, y=self.hmidbox*.15, anchor="center")

        hp = tk.Button(self.dcfrmbt, text="Back to homepage", image = self.lb16,
                                       borderwidth = 0, highlightthickness = 0,
                                   command=refresh)
        hp.place(relx=.5, y=self.hmidbox*.85, anchor='center')
        hp.image = self.lb16


class AddDefault (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.frame = Frame(self)
        self.frame.pack()
        self.conn = sqlite3.connect('master.db')
        self.c = self.conn.cursor()
        self.s = shelve.open('test_shelf.db')
        self.adt = self.s['title_holder']
        self.add_def_nice_names = list(self.adt.values())
        self.add_def_nice_names1 = self.add_def_nice_names[2:]
        self.cursor = self.conn.execute('select * FROM RecipeList')
        self.names = list(map(lambda x: x[0], self.cursor.description))
        self.conn.close()
        self.names1 = self.names[2:]
        self.frame.pack()
        self.def_dict = {}
        self.ad_list_of_widgets = []
        self.ad1_list_of_widgets = []
        self.TSelection = {}
        self.MSelection = {}
        self.fin_dict = {}
        self.big_dict = {}
        self.handler_dict = {}
        self.opt = {}
        self.lb8 = ImageTk.PhotoImage \
                (Image.open("lbutt.png").resize(
                (int(screensize[1] / 8), int(screensize[1] / 8))))
        self.options_list = set()
        self.starter(controller, parent)

    def starter(self, controller, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute('select meal from RecipeList')
        tester_value = c.fetchall()
        ex_tester = [i for word in tester_value for i in word]
        conn.close()
        if ex_tester == ['EnterRecipe']:
            photow = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
            wa = Label(self, image=photow)
            wa.image = photow
            wa.place(x=0, y=0, relwidth=1, relheight=1)
            frm50 = Frame(self, bg='black', width=wid, height=hei)
            frm50.place(x=xxx, y=yyy)
            frm60 = Frame(frm50, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            frm60.place(x=0)
            frm7 = Frame(frm50, bg='black', width=int(screensize[0] * 2 / 3), height=int(screensize[1] * 2 / 3))
            frm7.place(x=0, y=0)
            ran_empty = Label(frm7, fg='green', bg='black', text="ENTER A RECIPE FIRST",
                              font=("Courier", int(erht_inside)))
            ran_empty.place(relx=0.5, rely=0.25, anchor="center")
            ran_cl = Label(frm7, fg='white', bg='black', text="BACK TO HOMEPAGE",
                           font=("Courier", int(erht_inside)))
            ran_cl.place(relx=0.5, rely=0.5, anchor="center")

            ran_em_button_m = tk.Button(frm7, text="Back to homepage", image=self.lb8, borderwidth=0,
                                        highlightthickness=0, command=lambda: controller.show_frame(StartPage, parent))
            ran_em_button_m.place(relx=0.5, rely=0.75, anchor="center")
            ran_em_button_m.image = self.lb8
        else:
            self.make_def_screen(controller, 0, parent)

    def make_def_screen(self, controller, x, parent):
        for widget in self.ad1_list_of_widgets:
            widget.destroy()
        photow = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
        wa = Label(self, image=photow)
        wa.image = photow
        wa.place(x=0, y=0, relwidth=1, relheight=1)

        owidt_master = int(screensize[0] / 3)
        owidt_wid = int(owidt_master / 3)
        owidt_tit = int(owidt_wid * 2)
        oht_master = int(screensize[1] * 0.8)
        oht_inside = int(oht_master / 13)
        im = int(oht_inside / 2)
        frm_wid_place = owidt_master + owidt_tit
        frm1 = frm_wid_place + owidt_wid
        no_wids = len(self.names1)
        no_wids_1 = no_wids + 2

        self.lbi = ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((im, im)))

        frm_tit = Frame(self, bg='black', width=owidt_tit, height=oht_inside * no_wids_1)
        frm_tit.place(x=int(screensize[0] / 3), y=int(screensize[1] * 0.1))

        frm_wid = Frame(self, bg='black', width=owidt_wid, height=oht_inside * no_wids_1)
        frm_wid.place(x=frm_wid_place, y=int(screensize[1] * 0.1))

        frm_box = Frame(self, bg='black', width=owidt_wid, height=oht_inside * no_wids_1)
        frm_box.place(x=frm1, y=int(screensize[1] * 0.1))

        frmb = Frame(self, bg='black', width=oht_inside * 3.5, height=oht_inside)
        frmb.place(x=int(screensize[0] * 0.4325), y=int((screensize[1] * 0.1) + oht_inside * no_wids_1))

        self.ad1_list_of_widgets.append(frmb)
        self.ad1_list_of_widgets.append(frm_box)
        self.ad1_list_of_widgets.append(frm_tit)
        self.ad1_list_of_widgets.append(frm_wid)

        yy = oht_inside / 4
        yv = oht_inside + (oht_inside / 4)
        cx = 0
        ccx = 0
        colours = ['green', 'black', 'red', 'green', 'black', 'red', 'green', 'black', 'red', 'green']
        coloursw = ['green', 'white', 'red', 'green', 'white', 'red', 'green', 'white', 'red', 'green']

        self.lbel1 = tk.Label(frm_tit, text="Category", bg='black', fg='white',
                                  font=("Courier", int(oht_inside / 4)))
        self.lbel1.place(relx=0, y=yy)
        self.ad1_list_of_widgets.append(self.lbel1)

        self.lbel2 = tk.Label(frm_wid, text="Default Option", bg='black', fg='white',
                                  font=("Courier", int(oht_inside / 4)))
        self.lbel2.place(relx=0, y=yy)
        self.ad1_list_of_widgets.append(self.lbel2)

        self.lbel3 = tk.Label(frm_box, text="Untick for" "\n" "Anything But", bg='black', fg='white',
                                  font=("Courier", int(oht_inside / 4)))
        self.lbel3.place(relx=0, y=yy)
        self.ad1_list_of_widgets.append(self.lbel3)
        yy += oht_inside

        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        for item in self.names1:
            self.def_for_box = []
            c.execute("SELECT " + item + " FROM RecipeList")
            def_every_value_am = [i[0] for i in c.fetchall()]
            # def_every_value_am = c.fetchall()
            self.options_list = set(def_every_value_am)
            self.x = [i for i in self.options_list]

            self.handler_dict = {}
            s = shelve.open('test_shelf.db')
            adt = s['default_holder']
            for self.item1 in adt[item]:
                self.handler_dict = adt[item]
                self.def_for_box = list(self.handler_dict.keys())
            self.MSelection[item] = StringVar()
            self.MSelection[item].set(self.def_for_box)
            def_meal_menu = OptionMenu(frm_wid, self.MSelection[item], *self.x, 'Any')
            def_meal_menu.place(relx=0.25, y=yv)
            def_meal_menu.config(bg=coloursw[ccx], font=("Courier", int(oht_inside / 4)))
            menu = self.nametowidget(def_meal_menu.menuname)
            menu.config(font=("Courier", int(oht_inside / 4)), fg=colours[ccx])
            def_tick = adt[item][self.item1]
            self.TSelection[item] = IntVar()
            self.TSelection[item].set(def_tick)
            checkbutton = Checkbutton(frm_box, variable=self.TSelection[item])
            checkbutton.place(relx=0.5, y=yv)
            yv += oht_inside
            ccx += 1
            self.ad_list_of_widgets.append(def_meal_menu)
            self.ad_list_of_widgets.append(checkbutton)
        conn.close()
        for nice_item in self.add_def_nice_names1:
            self.def_lbel = tk.Label(frm_tit, text=nice_item,
                                     font = ("Courier", int(oht_inside / 3)), bg = 'black', fg = coloursw[cx])
            self.def_lbel.place(relx=0, y=yy)
            self.ad_list_of_widgets.append(self.def_lbel)
            cx += 1
            yy += oht_inside

        labo = Label(frm_tit, fg='red', bg='black', text="SEND", font=("Courier", int(oht_inside / 5)))
        labo.place(relx=.7, y=yv - (0.25 * oht_inside), anchor="center")

        labo2 = Label(frmb, fg='white', bg='black', text="BACK TO HOMEPAGE", font=("Courier", int(oht_inside / 5)))
        labo2.place(relx=.5, rely=0.15, anchor="center")

        am_button1 = tk.Button(frm_tit, text="Send changes", image=self.lbi, borderwidth=0, highlightthickness=0,
                               command=lambda: self.make_big_dict(controller, x, parent))
        am_button1.place(relx=.675, y=yv)
        am_button1.image = self.lbi


        am_button2 = tk.Button(frmb, text="Back to homepage",
                               image=self.lbi, borderwidth=0, highlightthickness=0,
                               command=lambda: controller.show_frame(StartPage, parent))
        am_button2.place(relx=.5, rely=.6, anchor="center")
        am_button2.image = self.lbi

        self.ad_list_of_widgets.append(am_button1)
        self.ad_list_of_widgets.append(am_button2)
        self.ad_list_of_widgets.append(labo)
        self.ad_list_of_widgets.append(labo2)


        if x == 1:
            controller.show_frame(StartPage)

    def make_big_dict(self, controller, x, parent):
        self.big_dict = {}
        s = shelve.open('test_shelf.db')
        self.fin_dict = s['default_holder']
        for self.ite in self.MSelection:
            mvalue = self.MSelection[self.ite].get()
            if mvalue == 'Any':
                tvalue = 'Any'
            else:
                tvalue = mvalue[2:-3]
            self.big_dict[self.ite] = tvalue
        for self.ite in self.big_dict:
            self.ite_key = self.big_dict[self.ite]
            self.ite_val = self.TSelection[self.ite].get()
            self.fin_dict[self.ite] = {self.ite_key: self.ite_val}
        self.make_changes(controller, x, parent)

    def make_changes(self, controller, x, parent):
        for widget in self.ad_list_of_widgets:
            widget.destroy()
        for widget in self.ad1_list_of_widgets:
            widget.destroy()
        s = shelve.open('test_shelf.db')
        del s['default_holder']
        s = shelve.open('test_shelf.db')
        s['default_holder'] = self.fin_dict

        oht_master = int(screensize[1] * 0.8)
        oht_inside = int(oht_master / 13)
        im1 = int(oht_inside)

        self.lbi1 = ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((im1, im1)))
        self.hmidbox=int(screensize[1]/4)

        self.frmend = Frame(self, bg='black', width=int(screensize[0]/4), height=int(screensize[1]/4))
        self.frmend.place(x=int(screensize[0]/3), y=int((screensize[1]/3)))

        def_lb = tk.Label(self.frmend, fg='white', bg='black', text="Default Changed",
                                font=("Courier", int(screensize[0] / 60)))
        def_lb.place(relx=.5, y=self.hmidbox * .15, anchor="center")

        def_lb1 = tk.Label(self.frmend, fg='red', bg='black', text="BACK TO HOMEPAGE",
                          font=("Courier", int(screensize[0] / 60)))
        def_lb1.place(relx=.5, y=self.hmidbox * .45, anchor="center")

        am_buttonx = tk.Button(self.frmend, text="Back to homepage", image=self.lbi1,
                       borderwidth=0, highlightthickness=0,
                       command=refresh)
        am_buttonx.place(relx=.5, y=self.hmidbox * .75, anchor='center')
        am_buttonx.image = self.lbi1
        self.ad1_list_of_widgets.append(def_lb)
        self.ad1_list_of_widgets.append(def_lb1)
        self.ad1_list_of_widgets.append(am_buttonx)
        conn.close()


class AddDeleteOption (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.frame = Frame(self)
        self.frame.pack()
        self.ado_list_of_widgets = []
        self.ado_list_of_widgets1 = []
        self.bth_widgets = []
        self.ta_widgets = []
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        s = shelve.open('test_shelf.db')
        adot = s['title_holder']
        self.ado_def_nice_names = list(adot.values())
        self.ado_def_nice_names1 = self.ado_def_nice_names[2:]
        self.options_list = set()
        cursor = conn.execute('select * FROM RecipeList')
        self.ad_names = list(map(lambda x: x[0], cursor.description))
        conn.close()
        self.ad_names1 = self.ad_names[2:]
        self.ado_add_dict = {}
        self.ado_del_dict = {}
        self.add_to_list = []
        self.lbd8 = ImageTk.PhotoImage \
                (Image.open("lbutt.png").resize(
                (int(diary_height / 8), int(diary_height / 8))))
        self.lb16 = ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((int(screensize[1] / 16), int(screensize[1] / 16))))
        self.to_add = []
        self.to_del = []
        self.list_del = []
        self.opt_entry_dict = {}
        self.Mdel={}
        self.Madd={}
        self.opt_box_dict = {}
        self.make_labels_boxes(controller, 0, parent)

    def make_labels_boxes(self, controller, z, parent):
        for widget in self.ado_list_of_widgets:
            widget.destroy()
        for widge in self.ado_list_of_widgets1:
            widge.destroy()
        for widge in self.ta_widgets:
            widge.destroy()
        for widge in self.bth_widgets:
            widge.destroy()
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        photow = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
        wa = Label(self, image=photow)
        wa.image = photow
        wa.place(x=0, y=0, relwidth=1, relheight=1)

        owidt_master = int(screensize[0] / 3)
        owidt_wid = int(owidt_master / 3)
        owidt_tit = int(owidt_wid * 2)
        oht_master = int(screensize[1] * 0.8)
        self.oht_inside = int(oht_master / 13)
        im = int(self.oht_inside / 2)
        frm_wid_place = owidt_master + owidt_tit
        frm1 = frm_wid_place + owidt_wid
        no_wids = len(self.ad_names1)
        self.no_wids_1 = no_wids+2

        self.lbi = ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((im, im)))

        ofrm_tit = Frame(self, bg='black', width=owidt_tit, height=self.oht_inside * self.no_wids_1)
        ofrm_tit.place(x=int(screensize[0] / 3), y=int(screensize[1] * 0.1))

        ofrm_wid = Frame(self, bg='black', width=owidt_wid, height=self.oht_inside * self.no_wids_1)
        ofrm_wid.place(x=frm_wid_place, y=int(screensize[1] * 0.1))

        ofrm_box = Frame(self, bg='black', width=owidt_wid, height=self.oht_inside * self.no_wids_1)
        ofrm_box.place(x=frm1, y=int(screensize[1] * 0.1))

        self.ofrmb = Frame(self, bg='black', width=self.oht_inside * 3.5, height=self.oht_inside)
        self.ofrmb.place(x=int(screensize[0] * 0.4325), y=int((screensize[1] * 0.1) + self.oht_inside * self.no_wids_1))

        self.ado_list_of_widgets.append(self.ofrmb)
        self.ado_list_of_widgets.append(ofrm_box)
        self.ado_list_of_widgets.append(ofrm_tit)
        self.ado_list_of_widgets.append(ofrm_wid)

        yy = self.oht_inside/4
        yv = self.oht_inside+(self.oht_inside/4)
        cx = 0
        ccx = 0
        colours = ['green', 'black', 'red', 'green', 'black', 'red', 'green', 'black', 'red', 'green']
        coloursw = ['green', 'white', 'red', 'green', 'white', 'red', 'green', 'white', 'red', 'green']

        self.ado_lbel1 = tk.Label(ofrm_tit, text="Category", bg='black', fg='white',
                                  font=("Courier", int(self.oht_inside / 4)))
        self.ado_lbel1.place(relx=0, y=yy)
        self.ado_list_of_widgets.append(self.ado_lbel1)


        self.ado_lbel2 = tk.Label(ofrm_wid, text="Delete Option", bg='black', fg='white',
                                  font=("Courier", int(self.oht_inside / 4)))
        self.ado_lbel2.place(relx=0, y=yy)
        self.ado_list_of_widgets.append(self.ado_lbel2)


        self.ado_lbel3 = tk.Label(ofrm_box, text="Add Option", bg='black', fg='white',
                                  font=("Courier", int(self.oht_inside / 4)))
        self.ado_lbel3.place(relx=0, y=yy)
        self.ado_list_of_widgets.append(self.ado_lbel3)
        yy+=self.oht_inside
        s = shelve.open('test_shelf.db')
        self.testit = s['key1']

        for ado_item in self.ado_def_nice_names1:
            self.ado_lbel = tk.Label(ofrm_tit, text=ado_item,
                                     font=("Courier", int(self.oht_inside / 3)), bg='black', fg=coloursw[cx])
            self.ado_lbel.place(relx=0, y=yy)
            cx+=1
            yy+=self.oht_inside
            self.ado_list_of_widgets.append(self.ado_lbel)

        for ite in self.ad_names1:
            ado_om_var = StringVar()
            ex_o = self.testit[ite]

            self.Mdel[ite] = StringVar()
            self.opt_box_dict[ite] = OptionMenu(ofrm_wid, self.Mdel[ite], *ex_o, "-")
            self.opt_box_dict[ite].config(bg=coloursw[ccx], font=("Courier", int(self.oht_inside / 4)))
            menu = self.nametowidget(self.opt_box_dict[ite].menuname)
            menu.config(font=("Courier", int(self.oht_inside / 4)), fg=colours[ccx])
            self.opt_box_dict[ite].place(relx=0.25, y=yv)

            self.opt_entry_dict[ite] = Entry(ofrm_box,
                                   font=('Courier', int(self.oht_inside / 5)))
            self.opt_entry_dict[ite].place(relx=0, y=yv)
            self.ado_list_of_widgets.append(self.opt_entry_dict[ite])
            yv += self.oht_inside
            ccx += 1
        conn.close()
        labo = Label(ofrm_tit, fg='red', bg='black', text="SEND", font=("Courier", int(self.oht_inside / 5)))
        labo.place(relx=.7, y=yv-(0.25*self.oht_inside), anchor="center")

        self.labo2 = Label(self.ofrmb, fg='white', bg='black', text="BACK TO HOMEPAGE",
                           font=("Courier", int(self.oht_inside / 5)))
        self.labo2.place(relx=.5, rely=0.15, anchor="center")


        ado_button_1 = tk.Button(ofrm_tit, text="Send Changes", image=self.lbi, borderwidth=0, highlightthickness=0,
                                 command=lambda: self.del_store_values(controller, parent))
        ado_button_1.place(relx=.675, y=yv)
        ado_button_1.image = self.lbi

        self.ado_button_2 = tk.Button(self.ofrmb, text="Back to Homepage", image=self.lbi,
                                 borderwidth=0, highlightthickness=0,
                                 command=lambda: self.make_labels_boxes(controller, 1, parent))
        self.ado_button_2.place(relx=.5, rely=.6, anchor="center")
        self.ado_button_2.image = self.lbi
        self.bth_widgets.append(self.ado_button_2)
        self.bth_widgets.append(self.labo2)
        self.ado_list_of_widgets.append(ado_button_1)
        self.ado_list_of_widgets.append(labo)
        if z == 1:
            refresh()

    def del_store_values(self, controller, parent):
        for k in self.opt_box_dict:
            to_del = self.Mdel[k].get()
            if to_del and to_del !='-':
                self.ado_del_dict[k] = to_del
        self.add_store_values(controller, parent)

    def add_store_values(self, controller, parent):
        for k in self.opt_entry_dict:
            to_add = self.opt_entry_dict[k].get()
            if to_add:
                self.ado_add_dict[k] = to_add
        self.op_leng_test(controller, parent)

    def op_leng_test(self, controller, parent):
        rogue_list= []
        for k in self.ado_add_dict:
            if len(self.ado_add_dict[k])>50:
                rogue_list.append(k)
        if rogue_list:
            str1 = ', '.join(rogue_list)
            ad_long_win = tk.Toplevel()
            ad_long_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
            ad_l = Frame(ad_long_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            ad_l.place(x=0)
            adi_l = Frame(ad_long_win, bg='black', width=diary_wid, height=diary_height)
            adi_l.place(x=0, y=0)
            ad_lab = Label(adi_l, fg='red', bg='black',
                           text="Options " "\n" + str1 + "\n" "Must be less than 50 characters",
                           font=("Courier", int(diary_height / 30)))
            ad_lab.place(x=diary_wid * .2, y=int(diary_height * 10 / 32))
            ad_long_lab = Label(adi_l, fg='white', bg='black', text="CLOSE WINDOW",
                                font=("Courier", int(diary_height / 30)))
            ad_long_lab.place(x=diary_wid * .38, y=int(diary_height * 15 / 32))

            ad_long_button = tk.Button(adi_l, text="Close Window", image=self.lbd8,
                                       borderwidth=0, highlightthickness=0, command=ad_long_win.destroy)
            ad_long_button.place(x=diary_wid * .43, y=int(diary_height * 18 / 32))
            ad_long_button.image = self.lbd8
        else:
            self.update_pers_dict(controller, parent)

    def update_pers_dict(self, controller, parent):
        s = shelve.open('test_shelf.db')
        existing = s['key1']
        rogue_list1 = []
        for k in self.ado_add_dict:
            self.to_add = self.ado_add_dict[k]
            self.add_to_list = existing[k]
            if self.to_add in self.add_to_list:
                rogue_list1.append(self.to_add)
        if rogue_list1:
            str2 = ', '.join(rogue_list1)
            ad_long_win = tk.Toplevel()
            ad_long_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
            ad_l = Frame(ad_long_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            ad_l.place(x=0)
            adi_l = Frame(ad_long_win, bg='black', width=diary_wid, height=diary_height)
            adi_l.place(x=0, y=0)
            self.rpbuttimgr = ImageTk.PhotoImage \
                    (Image.open("/Users/james/Pictures/red.png").resize(
                    (int(diary_height / 8), int(diary_height / 8))))
            ad_lab = Label(adi_l, fg='red', bg='black',
                           text=str2 + " Already Exists - Try Again",
                           font=("Courier", int(diary_height / 30)))
            ad_lab.place(x=diary_wid * .2, y=int(diary_height * 10 / 32))
            ad_long_lab = Label(adi_l, fg='white', bg='black', text="CLOSE WINDOW",
                                font=("Courier", int(diary_height / 30)))
            ad_long_lab.place(x=diary_wid * .38, y=int(diary_height * 15 / 32))

            ad_long_button = tk.Button(adi_l, text="Close Window", image=self.rpbuttimgr,
                                       borderwidth=0, highlightthickness=0, command=ad_long_win.destroy)
            ad_long_button.place(x=diary_wid * .43, y=int(diary_height * 18 / 32))
            ad_long_button.image = self.rpbuttimgr

        else:
            self.next_test(controller, parent)

    def next_test(self, controller, parent):
        rogue_list2=[]
        for ke in self.ado_del_dict:
            conn = sqlite3.connect('master.db')
            c = conn.cursor()
            c.execute("SELECT " + ke + " FROM RecipeList")
            if_exists = c.fetchall()
            ex_if_exists = [a for b in if_exists for a in b]
            set_ex_if_exists = set(ex_if_exists)
            if self.ado_del_dict[ke] in set_ex_if_exists:
                rogue_list2.append(self.ado_del_dict[ke])
        if rogue_list2:
            str2 = ', '.join(rogue_list2)
            ad_long_win = tk.Toplevel()
            ad_long_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
            ad_l = Frame(ad_long_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            ad_l.place(x=0)
            adi_l = Frame(ad_long_win, bg='black', width=diary_wid, height=diary_height)
            adi_l.place(x=0, y=0)
            ad_lab = Label(adi_l, fg='red', bg='black',
                           text="You are Using" "\n" + str2 + "\n" "Try Again",
                           font=("Courier", int(diary_height / 30)))
            ad_lab.place(x=diary_wid * .35, y=int(diary_height * 10 / 32))
            ad_long_lab = Label(adi_l, fg='white', bg='black', text="CLOSE WINDOW",
                                font=("Courier", int(diary_height / 30)))
            ad_long_lab.place(x=diary_wid * .38, y=int(diary_height * 15 / 32))

            ad_long_button = tk.Button(adi_l, text="Close Window", image=self.lbd8,
                                       borderwidth=0, highlightthickness=0, command=ad_long_win.destroy)
            ad_long_button.place(x=diary_wid * .43, y=int(diary_height * 18 / 32))
            ad_long_button.image = self.lbd8
        else:
            self.make_the_add_change(parent, controller)

    def make_the_add_change(self, controller, parent):
        s = shelve.open('test_shelf.db', writeback=True)
        for k in self.ado_add_dict:
            existing = s['key1']
            self.to_add = self.ado_add_dict[k]
            self.add_to_list = existing[k]
            list_add = list(self.add_to_list)
            list_add.append(self.to_add)
            existing[k] = list_add
            s = shelve.open('test_shelf.db')
            del s['key1']
            s = shelve.open('test_shelf.db')
            s['key1'] = existing
        s.sync()
        s.close()
        self.ado_add_dict = {}
        self.make_the_del_change(controller, parent)

    def make_the_del_change(self, controller, parent):
        s = shelve.open('test_shelf.db', writeback=True)
        for ke in self.ado_del_dict:
            s = shelve.open('test_shelf.db')
            exi = s['key1']
            self.to_del = self.ado_del_dict[ke]
            self.list_del = exi[ke]
            self.list_del.remove(self.to_del)
            exi[ke] = self.list_del
            s = shelve.open('test_shelf.db')
            del s['key1']
            s = shelve.open('test_shelf.db')
            s['key1'] = exi
        s.sync()
        s.close()
        self.ado_del_dict={}
        self.set_up(controller, parent)

    def set_up(self, controller, parent):
        for widget in self.ado_list_of_widgets:
            widget.destroy()
        for widget in self.ado_list_of_widgets1:
            widget.destroy()
        self.hmidbox = int(screensize[1] / 4)
        self.wmidbox = int(screensize[0] / 4)

        self.dcfrmbt = Frame(self, bg='black', width=self.wmidbox, height=self.hmidbox)
        self.dcfrmbt.place(x=int(screensize[0] / 3), y=int((screensize[1] * .3)))

        dclab = Label(self.dcfrmbt, fg='white', bg='black', text="MAKE ANOTHER CHANGE",
                      font=("Courier", int(screensize[0] / 70)))
        dclab.place(relx=.5, y=self.hmidbox*.15, anchor="center")

        ado_button_3 = tk.Button(self.dcfrmbt, text="Make Another Change",
                                 image=self.lb16, borderwidth=0, highlightthickness=0,
                                 command=lambda: self.make_labels_boxes(controller, 0, parent))
        ado_button_3.place(relx=.5, y=self.hmidbox * 0.35, anchor='center')
        ado_button_3.image = self.lb16
        s = shelve.open('test_shelf.db')
        self.testit = s['key1']
        self.dclabb = Label(self.dcfrmbt, fg='red', bg='black', text="BACK TO HOMEPAGE",
                            font=("Courier", int(screensize[0] / 70)))
        self.dclabb.place(relx=.5, y=self.hmidbox * 0.65, anchor="center")

        ado_button_4 = tk.Button(self.dcfrmbt, text="Back to homepage", image=self.lb16,
                                       borderwidth=0, highlightthickness=0,
                                 command=refresh)
        ado_button_4.place(relx=.5, y=self.hmidbox * 0.85, anchor='center')
        ado_button_4.image = self.lb16

        self.ado_list_of_widgets1.append(dclab)
        self.ado_list_of_widgets1.append(self.dclabb)
        self.ado_list_of_widgets1.append(self.dcfrmbt)
        self.ado_list_of_widgets1.append(ado_button_3)
        self.ado_list_of_widgets1.append(ado_button_4)


class CustomPlan(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.ac_list_of_widgets = []
        self.frame2 = Frame(self)
        self.frame2.pack(side=TOP)
        self.frame3 = Frame(self)
        self.frame3.pack(side=BOTTOM)
        self.days_to_customise = []
        self.noddy = {}
        self.results = {'Monday': '', 'Tuesday': '', 'Wednesday': '', 'Thursday': '',
                        'Friday': '', 'Saturday': '', 'Sunday': ''}
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        cursor = conn.execute('select * FROM RecipeList')
        self.col_names = list(map(lambda x: x[0], cursor.description))
        self.col_names1 = self.col_names[2:]
        self.dict_to_fill = {}
        for item in self.col_names:
            self.dict_to_fill[item] = ""
        self.col_meal = self.col_names[0]
        self.day_attr_val_dict = {}
        self.day_potmeals = {}
        self.no_days = {}
        self.list_days = {}
        self.list_no_days = []
        self.final_pl_display = []
        self.keep_track_widgets_dict = {}
        self.widgets_box_list = []
        self.random_template = {}
        s = shelve.open('test_shelf.db')
        ct = s['title_holder']
        self.cp_nice_names = list(ct.values())
        self.cp_nice_names1 = self.cp_nice_names[2:]
        conn.close()
        self.default_dict = {}
        self.def_dict = {}
        self.to_zip = []
        self.yes_dict = {}
        self.no_dict = {}
        self.yes1_dict = {}
        self.no1_dict = {}
        self.meal_list_after_def = []
        self.custom_list_of_widgets1 = []
        self.set_of_meals = set()
        self.custom_list_of_widgets = []
        self.custom_list_of_widgets_pu = []
        self.template = {}
        self.boxer = {}
        self.hold_list = []
        self.box = {}
        self.special_widgets= []
        self.day_attr_val_dict_hold = {}
        self.cplink_full = {}
        self.lb8 = ImageTk.PhotoImage \
                (Image.open("lbutt.png").resize(
                (int(screensize[1] / 8), int(screensize[1] / 8))))
        self.lb16 = ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((int(screensize[1] / 16), int(screensize[1] / 16))))
        self.lbd8 = ImageTk.PhotoImage \
                (Image.open("lbutt.png").resize(
                (int(diary_height / 8), int(diary_height / 8))))
        self.lwbd8 = ImageTk.PhotoImage \
                (Image.open("lwbutt.png").resize(
                (int(diary_height / 8), int(diary_height / 8))))
        self.c_starter(controller, parent)

    def c_starter(self, controller, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute('select meal from RecipeList')
        tester_value = c.fetchall()
        ex_tester = [i for word in tester_value for i in word]
        conn.close()
        if ex_tester == ['EnterRecipe']:
            photow = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
            wa = Label(self, image=photow)
            wa.image = photow
            wa.place(x=0, y=0, relwidth=1, relheight=1)
            frm50 = Frame(self, bg='black', width=wid, height=hei)
            frm50.place(x=xxx, y=yyy)
            frm60 = Frame(frm50, bg='black', width=int(screensize[0]), height=int(screensize[1]))
            frm60.place(x=0)
            frm7 = Frame(frm50, bg='black', width=int(screensize[0] * 2 / 3), height=int(screensize[1] * 2 / 3))
            frm7.place(x=0, y=0)
            ran_empty = Label(frm7, fg='green', bg='black', text="ENTER A RECIPE FIRST",
                              font=("Courier", int(erht_inside)))
            ran_empty.place(relx=0.5, rely=0.25, anchor="center")
            ran_cl = Label(frm7, fg='white', bg='black', text="BACK TO HOMEPAGE",
                           font=("Courier", int(erht_inside)))
            ran_cl.place(relx=0.5, rely=0.5, anchor="center")

            ran_em_button_m = tk.Button(frm7, text="Back to homepage", image=self.lb8, borderwidth=0,
                                        highlightthickness=0, command=lambda: controller.show_frame(StartPage, parent))
            ran_em_button_m.place(relx=0.5, rely=0.75, anchor="center")
            ran_em_button_m.image = self.lb8
        else:
            self.make_days(controller, 0, parent)

    def make_days(self, controller, z, parent):
        for widge in self.custom_list_of_widgets:
            widge.destroy()

        photoar = ImageTk.PhotoImage(Image.open("ChCur.jpeg").resize((screensize)))
        ara = Label(self, image=photoar)
        ara.image = photoar
        ara.place(x=0, y=0, relwidth=1, relheight=1)
        self.hmidbox = int(screensize[1] / 4)
        self.wmidbox = int(screensize[0] / 4)

        self.frm = Frame(self, bg='black', width=int(screensize[0]/4), height=screensize[1])
        self.frm.place(x=0, y=int(screensize[1]/10))

        self.frmt = Frame(self, bg='black', width=int(screensize[0] /4), height=screensize[1]/10)
        self.frmt.place(x=0, y=0)

        self.frmbt = Frame(self, bg='black', width=self.wmidbox, height=self.hmidbox*.5)
        self.frmbt.place(x=int(screensize[0]/3), y=(int(screensize[1]*.3)+(self.hmidbox*.5)))

        self.labt = Label(self.frmt, fg='white', bg='black', text="Special Days",
                      font=("Courier", int(screensize[1]/ 52)))
        self.labt.place(relx=.5, rely=.5, anchor="center")

        self.labb = Label(self.frmbt, fg='red', bg='black', text="BACK TO HOMEPAGE",
                          font=("Courier", int(screensize[0] / 70)))
        self.labb.place(relx=.5, y=self.hmidbox * .15, anchor="center")

        self.delete_button2 = tk.Button(self.frmbt, text="Back to homepage",image=self.lb16,
                                   borderwidth=0, highlightthickness=0,
                                   command=lambda: self.make_days(controller, 1, parent))
        self.delete_button2.place(relx=.5, y=self.hmidbox*0.35, anchor='center')
        self.delete_button2.image =self.lb16

        self.md_listbox = Listbox(self.frm, selectmode="multiple", height=50, fg = 'white', bg = "black",
                                  borderwidth=0, highlightthickness=0)
        self.md_listbox.place(x=0, y=0)
        self.md_listbox.insert(END, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        self.md_listbox.config(font=("Courier", int(screensize[1] / 52)))
        self.md_listbox.bind('<<ListboxSelect>>', lambda event: self.days_collector(controller, parent))

        self.custom_list_of_widgets.append(self.md_listbox)
        self.custom_list_of_widgets.append(self.frm)
        self.custom_list_of_widgets.append(self.frmt)
        self.custom_list_of_widgets.append(self.frmbt)
        self.custom_list_of_widgets.append(self.labt)
        self.custom_list_of_widgets.append(self.delete_button2)
        self.custom_list_of_widgets.append(self.labb)

        if z == 1:
            controller.show_frame(StartPage, parent)

    def days_collector(self, controller, parent):
        for widge in self.special_widgets:
            widge.destroy()
        self.sort_days = {'Monday': '', 'Tuesday': '', 'Wednesday': '',
                          'Thursday': '', 'Friday': '', 'Saturday': '', 'Sunday': ''}
        self.days_to_do = []
        self.list_sorted = []
        selected_indices = self.md_listbox.curselection()
        list_select = list(selected_indices)
        for day in list_select:
            self.days_to_do.append(self.md_listbox.get(day))
        for days in self.days_to_do:
            for k in self.sort_days:
                if k==days:
                    self.sort_days[k] = days
        self.list_sorted = [k for k, v in self.sort_days.items() if v]
        if self.list_sorted:
            self.frmbt1 = Frame(self, bg='black', width=self.wmidbox, height=self.hmidbox*.5)
            self.frmbt1.place(x=int(screensize[0] / 3), y=int(screensize[1] * .3))
            self.labs = Label(self.frmbt1, fg='white', bg='black', text="SEND DAYS",
                             font=("Courier", int(screensize[0] / 70)))
            self.labs.place(relx=.5, y=self.hmidbox*.15, anchor="center")

            self.md_button = tk.Button(self.frmbt1, text="Send Days",
                                       image=self.lb16, borderwidth=0, highlightthickness=0,
                                       command=lambda: self.make_custom_screen(controller, parent))
            self.md_button.place(relx = .5, y = self.hmidbox*0.35, anchor='center')
            self.md_button.image = self.lb16
            self.special_widgets.append(self.md_button)
            self.special_widgets.append(self.labs)
            self.special_widgets.append(self.frmbt1)

    def make_custom_screen(self, controller, parent):
        for widge in self.custom_list_of_widgets:
            widge.destroy()
        for widge in self.special_widgets:
            widge.destroy()
        self.half={}
        self.TCSelection = {}
        no_days=len(self.days_to_do)
        owidt_master = int(screensize[0]*.8)
        owidt_wid = int((owidt_master /9)*no_days)
        owidt_tit = int((owidt_master /9)*2)
        tit_wid_block = int(owidt_master/9)
        oht_master = int(screensize[1] * 0.8)
        oht_inside = int(oht_master / 14)
        im = int(oht_inside / 1.5)
        frm_wid_place = owidt_master + owidt_tit
        frm1 = frm_wid_place + owidt_wid
        no_wids = len(self.cp_nice_names1)
        no_wids_1 = no_wids+4

        self.lbi = ImageTk.PhotoImage \
            (Image.open("lbutt.png").resize((im, im)))

        ofrm_tit = Frame(self, bg='black', width=owidt_tit, height=oht_inside * no_wids_1)
        ofrm_tit.place(x=int(screensize[0]*.15), y=int(screensize[1] * 0.1))

        ofrm_wid = Frame(self, bg='black', width=owidt_wid, height=oht_inside * no_wids_1)
        ofrm_wid.place(x=(int(screensize[0]*.15)+ owidt_tit), y=int(screensize[1] * 0.1))

        self.custom_list_of_widgets.append(ofrm_tit)
        self.custom_list_of_widgets.append(ofrm_wid)

        tit_ht = int((oht_inside/4)+(oht_inside*2))
        ywd = 0
        box_wid = 0
        cx = 0
        ct=0
        ccx = 0
        colours = ['green', 'black', 'red', 'green', 'black', 'red', 'green', 'black', 'red', 'green']
        coloursw = ['green', 'white', 'red', 'green', 'white', 'red', 'green', 'white', 'red', 'green']

        for nice_de_item in self.cp_nice_names1:
            self.mcs_label = tk.Label(ofrm_tit, text=nice_de_item, bg='black', fg='white',
                                      font=("Courier", int(oht_inside / 4)))
            self.mcs_label.place(x=0, y=tit_ht)
            self.custom_list_of_widgets.append(self.mcs_label)
            tit_ht+=oht_inside
        self.mcs_label1 = tk.Label(ofrm_tit, text="Untick to leave day blank", bg='black', fg='white',
                                      font=("Courier", int(oht_inside / 4)))
        self.mcs_label1.place(x=0, y=(int(oht_inside /4)+oht_inside))
        self.custom_list_of_widgets.append(self.mcs_label1)
        for de_dy in self.list_sorted:
            widg_ht = (int(oht_inside / 4) + (oht_inside * 2))
            self.hold_list = []
            self.vard = de_dy

            self.de_label = tk.Label(ofrm_wid, text=self.vard, bg='black', fg=coloursw[cx],
                                      font=("Courier", int(oht_inside / 4)))
            self.de_label.place(x=ywd, y=0)
            self.custom_list_of_widgets.append(self.de_label)
            self.TCSelection[de_dy] = IntVar()
            self.TCSelection[de_dy].set(1)
            self.tickbox = Checkbutton(ofrm_wid, variable=self.TCSelection[de_dy], bg = coloursw[cx])
            self.TCSelection[de_dy].trace("w", lambda name, index, mode,
                                        day1=de_dy, svari=self.TCSelection[de_dy]: self.make_no_dict(day1, svari))
            self.tickbox.place(x=ywd, y=(int(oht_inside /4)+oht_inside))
            self.custom_list_of_widgets.append(self.tickbox)
            conn = sqlite3.connect('master.db')
            c = conn.cursor()
            cx+=1
            for de_item in self.col_names1:
                c.execute("SELECT " + de_item + " FROM RecipeList")
                fetch_col_contents = [i[0] for i in c.fetchall()]
                chosen_var = StringVar()
                chosen_var.set("Any")
                unique_options_list = set(fetch_col_contents)
                chosen_var.trace("w", lambda name, index, mode, item=de_item, dy=de_dy,
                                             sv=chosen_var: self.populate_custom_dict(sv, dy, item))
                self.box[de_dy] = OptionMenu(ofrm_wid, chosen_var, *unique_options_list, "Any")
                self.box[de_dy].place(x=ywd, y=widg_ht)
                self.box[de_dy].config(bg=coloursw[ccx], font=("Courier", int(oht_inside / 6)))
                menu = self.nametowidget(self.box[de_dy].menuname)
                menu.config(font=("Courier", int(oht_inside / 4)), fg=colours[ccx])
                widg_ht+=oht_inside
                n = (self.box[de_dy])
                self.hold_list.append(n)
                self.boxer[de_dy] = self.hold_list
                self.widgets_box_list.append(self.box[de_dy])
                self.custom_list_of_widgets.append(self.box[de_dy])
            ywd += tit_wid_block
            ccx += 1
            conn.close()
            self.keep_track_widgets_dict[de_dy] = self.widgets_box_list

        labo1 = Label(ofrm_tit, fg='red', bg='black', text="SHOW PLAN", font=("Courier", int(oht_inside / 4)))
        labo1.place(x=0.5*tit_wid_block, y=int((oht_inside * no_wids_1) - (oht_inside*1.25)), anchor="center")

        cust_button_m = tk.Button(ofrm_tit, text= "Show Results", image=self.lbi, borderwidth=0, highlightthickness=0,
                                  command=lambda: self.make_default_dict(controller, parent))
        cust_button_m.place(x=int(0.5*tit_wid_block), y=int((oht_inside * no_wids_1) - (oht_inside*.5)),
                            anchor = 'center')
        cust_button_m.image=self.lbi

        labo3 = Label(ofrm_wid, fg='white', bg='black', text="HOMEPAGE", font=("Courier", int(oht_inside / 4)))
        labo3.place(x=int(owidt_wid-(.7*tit_wid_block)),
                    y=int((oht_inside * no_wids_1) - (oht_inside*1.25)), anchor="center")

        de_button_m2 = tk.Button(ofrm_wid, text="Back to Homepage", image=self.lbi, borderwidth=0, highlightthickness=0,
                                 command=lambda: self.make_days(controller, 1, parent))
        de_button_m2.place(x=int(owidt_wid-(.75*tit_wid_block)),
                           y=int((oht_inside * no_wids_1) - (oht_inside * .5)), anchor="center")
        de_button_m2.image = self.lbi

        self.custom_list_of_widgets.append(cust_button_m)
        self.custom_list_of_widgets.append(de_button_m2)
        self.custom_list_of_widgets_pu.append(cust_button_m)
        self.custom_list_of_widgets_pu.append(de_button_m2)
        self.custom_list_of_widgets_pu.append(labo1)
        self.custom_list_of_widgets_pu.append(labo3)

    def make_no_dict(self, day1, svari):
        val = svari.get()
        self.no_days[day1] = val
        if val == 0:
            a = self.boxer[day1]
            for each in a:
                each.configure(state='disabled')
        else:
            b = self.boxer[day1]
            for every in b:
                every.configure(state='normal')


    def populate_custom_dict (self, sv, dy, item):
        pcd_val = sv.get()
        if dy not in self.day_attr_val_dict:
            self.noddy[item] = pcd_val
            self.day_attr_val_dict[dy] = self.noddy
        else:
            self.noddy = self.day_attr_val_dict[dy]
            self.noddy[item]=pcd_val
            if pcd_val == 'Any':
                del self.noddy[item]
            self.day_attr_val_dict[dy] = self.noddy
            if not self.day_attr_val_dict[dy]:
                del self.day_attr_val_dict[dy]
        self.noddy={}


    def make_default_dict(self, controller, parent):
        holder_list = []
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        s = shelve.open('test_shelf.db')
        self.default_dict = s['default_holder']
        self.def_dict = self.default_dict
        for citem in self.def_dict:
            for opt in self.def_dict[citem]:
                if opt == 'Any':
                    holder_list.append(citem)
        for hitem in holder_list:
            del self.def_dict[hitem]
        for citem in self.def_dict:
            for opt in self.def_dict[citem]:
                if self.def_dict[citem][opt] == 1:
                    self.yes_dict[citem] = self.def_dict[citem]
                if self.def_dict[citem][opt] == 0:
                    self.no_dict[citem] = self.def_dict[citem]
        abc = 0
        for yitem in self.yes_dict:
            ygap = (map(list, self.yes_dict.values()))
            ygap1 = (list(ygap))
            ygap2 = ygap1[abc]
            abc += 1
            self.yes1_dict[yitem] = ygap2[0]
        self.yes_dict =self.yes1_dict
        xyz = 0
        for nitem in self.no_dict:
            ngap = (map(list, self.no_dict.values()))
            ngap1 = (list(ngap))
            ngap2 = ngap1[xyz]
            xyz += 1
            self.no1_dict[nitem] = ngap2[0]
        self.no_dict = self.no1_dict
        print(self.no_dict)
        for key in self.yes_dict:
            valy = self.yes_dict[key]
            c.execute("select meal from RecipeList WHERE " + key + "=?", (valy,))
            yes = c.fetchall()
            self.meal_list_after_def.append(yes)
        for key in self.no_dict:
            valn = self.no_dict[key]
            c.execute("select meal from RecipeList WHERE " + key + "!=?", (valn,))
            no = c.fetchall()
            self.meal_list_after_def.append(no)
        conn.close()
        exploded_deff_meals = ([item for t in self.meal_list_after_def for item in t])
        self.ssset_of_meals = set(exploded_deff_meals)
        self.set_of_meals = ([item for t in self.ssset_of_meals for item in t])
        if not self.set_of_meals:
            conn = sqlite3.connect('master.db')
            c = conn.cursor()
            c.execute('select meal from RecipeList')
            no_deff = c.fetchall()
            self.set_of_meals = ([item for t in no_deff for item in t])
            conn.close()
        self.calc_pot_meals_custom(controller, parent)

    def calc_pot_meals_custom(self, controller, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        cunter = 0
        for k in self.no_days:
            if self.no_days[k] == 0:
                self.list_no_days.append(k)
        for day in self.day_attr_val_dict:
            if day in self.list_no_days:
                del self.day_attr_val_dict[day]
            self.day = day
            self.cp_potential_meals = []
            self.attr_val = self.day_attr_val_dict[day]
            x = len(self.attr_val)
            for attr in self.attr_val:
                if attr in self.dict_to_fill.keys():
                    self.dict_to_fill[attr] = self.attr_val[attr]
            c.execute('select * from RecipeList')
            final_list = list(self.dict_to_fill.values())
            for row in c.fetchall():
                make_row_a_list = list(row)
                mapped = zip(make_row_a_list, final_list)
                counter = 0
                for i in mapped:
                    if i[0] == i[1]:
                        counter += 1
                if counter == x:
                    self.cp_potential_meals.append(row[0])
            self.day_potmeals[self.day] = self.cp_potential_meals
            if len(self.cp_potential_meals) != 0:
                cunter += 1
            if len(self.cp_potential_meals) == 0:
                sday = str(day)
                diary_day_win = tk.Toplevel()
                diary_day_win.title("Random Plan Results")
                diary_day_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
                frmd_day = Frame(diary_day_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
                frmd_day.place(x=0)
                frmdi_day = Frame(frmd_day, bg='black', width=diary_wid, height=diary_height)
                frmdi_day.place(x=0)
                self.ne_label = tk.Label(frmdi_day, text='No meals for ' + sday + '\n' 'close window and try again',
                                    fg='white', bg='black', font=("Courier", int(diary_height / 30)))
                self.ne_label.place(relx=0.25, rely=0.3)
                cust_button_ta = tk.Button(frmdi_day, text="CLOSE WINDOW", image=self.lbd8,
                                            borderwidth=0, highlightthickness=0, command=diary_day_win.destroy)
                cust_button_ta.place(relx=0.5, rely=0.5)
                cust_button_ta.image = self.lbd8
        conn.close()
        breaker1 = list(self.day_attr_val_dict.keys())
        if cunter == len(breaker1):
            self.gen_week(controller, parent)

    def gen_week(self, controller, parent):
        tups = []
        day = []
        for k in sorted(self.day_potmeals, key=lambda k: len(self.day_potmeals[k])):
            tups.append(self.day_potmeals[k])
            day.append(k)
        thebig = []
        cnt = 0
        for list_meals in tups:
            dy = day[cnt]
            dd = str(dy)
            cnt += 1
            for meal in list_meals:
                if meal in thebig:
                    list_meals.remove(meal)
                    if len(list_meals) == 0:
                        diary_day_win1 = tk.Toplevel()
                        diary_day_win1.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
                        frmd_day1 = Frame(diary_day_win1, bg='black',
                                          width=int(screensize[0]), height=int(screensize[1]))
                        frmd_day1.place(x=0)
                        frmdi_day1 = Frame(frmd_day1, bg='black', width=diary_wid, height=diary_height)
                        frmdi_day1.place(x=0)
                        self.ne_label1 = tk.Label(frmdi_day1,
                                                 text='No meals for ' + dd + ' without having same meal' '\n'
                                                  'Close window and try again',
                                                 fg='white', bg='black', font=("Courier", int(diary_height / 30)))
                        self.ne_label1.place(relx=0.02, rely=0.3)
                        cust_button_ta1 = tk.Button(frmdi_day1, text="CLOSE WINDOW", image=self.lbd8,
                                                   borderwidth=0, highlightthickness=0, command=diary_day_win1.destroy)
                        cust_button_ta1.place(relx=0.45, rely=0.5)
                        cust_button_ta1.image = self.lbd8
            if len(list_meals) != 0:
                thebig.append(random.choice(list_meals))
            self.template = dict(zip(day, thebig))
        if len(day) == len(thebig):
            self.make_dict_full(parent, controller)

    def make_dict_full(self, parent, controller):
        end_crit_dict = {'Monday': '', 'Tuesday': '', 'Wednesday': '', 'Thursday': '',
                         'Friday': '', 'Saturday': '', 'Sunday': ''}
        for i in self.template:
            if i == 'Monday':
                end_crit_dict['Monday'] = self.template[i]
            if i == 'Tuesday':
                end_crit_dict['Tuesday'] = self.template[i]
            if i == 'Wednesday':
                end_crit_dict['Wednesday'] = self.template[i]
            if i == 'Thursday':
                end_crit_dict['Thursday'] = self.template[i]
            if i == 'Friday':
                end_crit_dict['Friday'] = self.template[i]
            if i == 'Saturday':
                end_crit_dict['Saturday'] = self.template[i]
            if i == 'Sunday':
                end_crit_dict['Sunday'] = self.template[i]
        self.pop_results(parent, controller, **end_crit_dict)

    def pop_results(self, parent, controller, **kwargs):
        if 'Monday' in self.list_no_days:
            kwargs['Monday'] = 'N/A'
        if 'Tuesday' in self.list_no_days:
            kwargs['Tuesday'] = 'N/A'
        if 'Wednesday' in self.list_no_days:
            kwargs['Wednesday'] = 'N/A'
        if 'Thursday' in self.list_no_days:
            kwargs['Thursday'] = 'N/A'
        if 'Friday' in self.list_no_days:
            kwargs['Friday'] = 'N/A'
        if 'Saturday' in self.list_no_days:
            kwargs['Saturday'] = 'N/A'
        if 'Sunday' in self.list_no_days:
            kwargs['Sunday'] = 'N/A'
        self.calc_results(parent, controller, **kwargs)

    def calc_results(self, parent, controller, **kwargs):
        existing_meals = list(kwargs.values())
        self.final_meal_list = [x for x in self.set_of_meals if x not in existing_meals]
        self.pop_upper(parent, controller, **kwargs)

    def pop_upper(self, parent, controller, **kwargs):
        ct = 0
        for k, v in kwargs.items():
            if not v:
                if len(self.final_meal_list) == 0:
                    ct += 1
                    diary_day_win2 = tk.Toplevel()
                    diary_day_win2.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
                    frmd_day2 = Frame(diary_day_win2, bg='black',
                                      width=int(screensize[0]), height=int(screensize[1]))
                    frmd_day2.place(x=0)
                    frmdi_day2 = Frame(frmd_day2, bg='black', width=diary_wid, height=diary_height)
                    frmdi_day2.place(x=0)
                    self.ne_label2 = tk.Label(frmdi_day2,
                                              text='Not enough meals to make a plan,' '\n' 
                                                   'Add recipes or make your default less picky',
                                              fg='white', bg='black', font=("Courier", int(diary_height / 30)))
                    self.ne_label2.place(relx=0.05, rely=0.3)
                    cust_button_ta2 = tk.Button(frmdi_day2, text="CLOSE WINDOW", image=self.lbd8,
                                                borderwidth=0, highlightthickness=0, command=diary_day_win2.destroy)
                    cust_button_ta2.place(relx=0.45, rely=0.5)
                    cust_button_ta2.image = self.lbd8
                if len(self.final_meal_list) != 0:
                    kwargs[k] = random.choice(self.final_meal_list)
            if kwargs[k] in self.final_meal_list:
                self.final_meal_list.remove(kwargs[k])

        colourd = ['red', 'black', 'green', 'red', 'black', 'green', 'red']
        ccount = 0
        diary_win = tk.Toplevel()
        diary_win.title("Random Plan Results")
        diary_win.geometry('{}x{}+{}+{}'.format(diary_wid, diary_height, diary_x, diary_y))
        frmd = Frame(diary_win, bg='black', width=int(screensize[0]), height=int(screensize[1]))
        frmd.place(x=0)
        frmdi = Frame(frmd, bg='black', width=diary_wid, height=diary_height)
        frmdi.place(x=0, y=0)
        left_y_count = 1
        right_y_count = 1
        dir_pic = ImageTk.PhotoImage \
            (Image.open("diary.png").resize((diary_wid, diary_height)))
        dim = Label(frmdi, image=dir_pic)
        dim.image = dir_pic
        dim.place(x=0, y=0, relwidth=1, relheight=1)
        for key in kwargs:
            if kwargs[key] != 'N/A':
                jeff = kwargs[key]
                self.cplink_full[key] = Label(frmdi, text=jeff, fg='black',
                                           bg='white', font=("Courier", int(diary_height / 40)), cursor="hand2")
                self.cplink_full[key].bind("<Button-1>", lambda event, key=key,
                                                                jeff=jeff: self.cplink_open(event, jeff, key))
                if left_y_count < 8:
                    self.cplink_full[key].place(x=diary_wid * 0.05, y=int(diary_height / 8) * left_y_count)
                    left_y_count += 2
                    ccount += 1
                else:
                    self.cplink_full[key].place(x=diary_wid * .55, y=int(diary_height / 8) * right_y_count)
                    right_y_count += 2
                    ccount += 1
            if kwargs[key] == 'N/A':
                nlab = tk.Label(frmdi, text='No Meal Needed',  fg='black',
                                           bg='white', font=("Courier", int(diary_height / 40)), cursor="hand2")
                if left_y_count < 8:
                    nlab.place(x=diary_wid * 0.05, y=int(diary_height / 8) * left_y_count)
                    left_y_count += 2
                    ccount += 1
                else:
                    nlab.place(x=diary_wid * .55, y=int(diary_height / 8) * right_y_count)
                    right_y_count += 2
                    ccount += 1
        ran_lab = Label(frmdi, fg='red', bg='white', text="CLOSE WINDOW",
                        font=("Courier", int(diary_height / 45)))
        ran_lab.place(x=diary_wid * .66, y=int(diary_height * 25 / 32))

        ran_pl_button_m = tk.Button(frmdi, text="Close Window", image=self.lwbd8,
                                    borderwidth=0, highlightthickness=0, command=diary_win.destroy)
        ran_pl_button_m.place(x=diary_wid * .70, y=int(diary_height * 27 / 32))
        ran_pl_button_m.image = self.lwbd8

    def cplink_open(self, event, jeff, key):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute("select link from RecipeList WHERE meal =?", (jeff,))
        ln = c.fetchall()
        conn.close()
        ln1 = [item for t in ln for item in t]
        if ln1[0][:4] == "http":
            webbrowser.open_new(ln1[0])
        else:
            self.cplink_full[key]['text'] = (jeff + " - " + ln1[0])


vp_start_gui()
