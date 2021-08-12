import tkinter as tk
from tkinter import *
import sqlite3
import shelve
import random


def make_tables():
    conn = sqlite3.connect('master.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS RecipeList (
        meal text,
        MainIngredient text,
        expense text,
        PrepTime text
        )""")
    conn.commit()

    c.execute("""SELECT meal FROM RecipeList""")
    start_up_rl_checker = c.fetchall()

    if len(start_up_rl_checker) == 0:
        start_options_dict = {'MainIngredient': {'beef', 'pork', 'veg', 'pasta', 'lamb', 'chicken'},
                              'expense': {'expensive', 'normal', 'cheap'},
                              'PrepTime': {'normal', 'long time', 'quick'}}
        s = shelve.open('test_shelf.db')
        s['key1'] = start_options_dict

        title_holder_dict = {'Meal': 'Meal,', 'MainIngredient': 'Main Ingredient', 'expense': 'Expense',
                             'PrepTime': 'Prep Time'}
        s = shelve.open('test_shelf.db')
        s['title_holder'] = title_holder_dict

        default_dict = {'Meal': 'Meal,', 'MainIngredient': 'any', 'expense': 'any',
                             'PrepTime': 'any'}
        s = shelve.open('test_shelf.db')
        s['default_holder'] = default_dict

        c.execute("""INSERT INTO RecipeList VALUES  (?, ?, ?, ?
            )""", ("EnterRecipe", "EnterRecipe", "EnterRecipe", "EnterRecipe"))
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

LARGE_FONT = ("Verdana", 12)


class MenuQ(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        master = tk.Frame()
        master.pack(side="top", fill="both", expand=True)
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, RecipeBookStartPage, CustomSearch, AmendRecipe, AddRecipe, DeleteRecipe,
                  PlannerStartPage, CustomPlan, AddColumn, DeleteColumn, AddDefault, AddDeleteOption):
            frame = F(master, self)
            self.frames[F] = frame
            print(self.frames)
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage, master)

    def show_frame(self, cont, master):
        frame = self.frames[cont]
        app = cont(master, self)
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = 'blue')
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text="Recipe Book",
                            command = lambda: controller.show_frame(RecipeBookStartPage, parent))
        button1.pack()
        button2 = tk.Button(self, text="Planner", command=lambda: controller.show_frame(PlannerStartPage, parent))
        button2.pack()


class PlannerStartPage (tk.Frame):

    ryes_dict = {}
    rno_dict = {}
    rmeal_list_after_def = []
    rto_zip = []
    rdefault_dict = {}
    rdef_dict = {}
    random_template = {}
    full_list = []
    random_search_widgets = []

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.make_widges(controller, 0, parent)

    def make_widges(self, controller, x, parent):
        ps_button = tk.Button(self, text="Random planner", command=self.random_opener)
        ps_button.pack()
        ps2_button = tk.Button(self, text="Custom planner", command=lambda: controller.show_frame(CustomPlan, parent))
        ps2_button.pack()
        back_button = tk.Button(self, text="Back to homepage", command=lambda: self.sweeper_upper(controller, parent))
        back_button.pack()
        self.random_search_widgets.append(ps_button)
        self.random_search_widgets.append(ps2_button)
        self.random_search_widgets.append(back_button)
        self.rset_of_meals = []
        self.ryes_dict = {}
        self.rno_dict = {}
        self.rmeal_list_after_def = []

        if x == 1:
            controller.show_frame(StartPage, parent)

    def sweeper_upper(self, controller, parent):
        for widget in self.random_search_widgets:
            widget.destroy()
        self.make_widges(controller, 1, parent)

    def random_opener(self):
        self.random_template = {'Monday': '', 'Tuesday': '', 'Wednesday': '', 'Thursday': '',
                           'Friday': '', 'Saturday': '', 'Sunday': ''}
        self.rmake_default_dict()

    def rmake_default_dict(self):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        # cursor = conn.execute('select * FROM RecipeList')
        # rdef_col_names = list(map(lambda x: x[0], cursor.description))
        # rdef_col_names1 = rdef_col_names[1:]
        # c.execute('select * FROM RecipeListDefault')
        # for row in c.fetchall():
        #     rdef_make_row_a_list = list(row)
        #     self.rto_zip = rdef_make_row_a_list[1:]
        # self.rdefault_dict = dict(zip(rdef_col_names1, self.rto_zip))
        # self.rdef_dict = {key:value for (key, value) in self.rdefault_dict.items() if value != 'any'}

        s = shelve.open('test_shelf.db')
        self.rdefault_dict = s['default_holder']
        self.rdef_dict = {key: value for (key, value) in self.rdefault_dict.items() if value != 'any'}
        for key in self.rdef_dict:
            if self.rdef_dict[key][0:3] != 'not':
                self.ryes_dict[key] = self.rdef_dict[key]
            if self.rdef_dict[key][0:3] == 'not':
                self.rno_dict[key] = self.rdef_dict[key]
        for key in self.ryes_dict:
            rvaly = self.ryes_dict[key]
            c.execute("select meal from RecipeList WHERE " + key + "=?", (rvaly,))
            ryes = c.fetchall()
            self.rmeal_list_after_def.append(ryes)
        for key in self.rno_dict:
            rvaln = self.ryes_dict[key]
            c.execute("select meal from RecipeList WHERE " + key + "!=?", (rvaln,))
            rno = c.fetchall()
            self.rmeal_list_after_def.append(rno)
        exploded_def_meals = ([item for t in self.rmeal_list_after_def for item in t])
        self.rset_of_meals=set(exploded_def_meals)
        if not self.rset_of_meals:
            c.execute('select meal from RecipeList')
            self.rset_of_meals = c.fetchall()
            self.rcalc_results(**self.random_template)
            conn.close()
        if len(self.rset_of_meals) < 7:
            ln = len(self.rset_of_meals)
            sln = str(ln)
            short = 7-ln
            sshort = str(short)
            not_enough_lbl = tk.Label(self, text ="Only " + sln + " meals fit the bill, "
                                               "change the default or use custom search for " + sshort + " meal")
            not_enough_lbl.pack()
            self.random_search_widgets.append(not_enough_lbl)
            conn.close()
        else:
            conn.close()
            self.rcalc_results(**self.random_template)

    def rcalc_results(self, **kwargs):
        rand_exploded_raw_meal_list = [i[0] for i in self.rset_of_meals]
        rand_existing_meals = list(kwargs.values())
        self.rand_final_meal_list = [x for x in rand_exploded_raw_meal_list if x not in rand_existing_meals]
        self.rpop_upper(**kwargs)

    def rpop_upper(self, **kwargs):
        if not self.rand_final_meal_list:
            print(2)
        for k, v in kwargs.items():
            if not v:
                kwargs[k] = random.choice(self.rand_final_meal_list)
            if kwargs[k] in self.rand_final_meal_list:
                self.rand_final_meal_list.remove(kwargs[k])
        rand_pl_win = tk.Toplevel()
        rand_pl_win.title("Random Plan Results")
        monday_lbl = tk.Label(rand_pl_win, text=kwargs["Monday"], font=LARGE_FONT)
        monday_lbl.pack(side=TOP)
        tuesday_lbl = tk.Label(rand_pl_win, text=kwargs["Tuesday"], font=LARGE_FONT)
        tuesday_lbl.pack(side=TOP)
        wednesday_lbl = tk.Label(rand_pl_win, text=kwargs["Wednesday"], font=LARGE_FONT)
        wednesday_lbl.pack(side=TOP)
        thursday_lbl = tk.Label(rand_pl_win, text=kwargs["Thursday"], font=LARGE_FONT)
        thursday_lbl.pack(side=TOP)
        friday_lbl = tk.Label(rand_pl_win, text=kwargs["Friday"], font=LARGE_FONT)
        friday_lbl.pack(side=TOP)
        saturday_lbl = tk.Label(rand_pl_win, text=kwargs["Saturday"], font=LARGE_FONT)
        saturday_lbl.pack(side=TOP)
        sunday_lbl = tk.Label(rand_pl_win, text=kwargs["Sunday"], font=LARGE_FONT)
        sunday_lbl.pack(side=TOP)
        rand_pl_button_m = tk.Button(rand_pl_win, text="Close Window", command=rand_pl_win.destroy)
        rand_pl_button_m.pack()


class RecipeBookStartPage (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        full_button = tk.Button(self, text="See all recipes", command = lambda: self.view_full_list())
        full_button.pack()
        custom_button = tk.Button(self, text="Custom Search",
                                  command=lambda: controller.show_frame(CustomSearch, parent))
        custom_button.pack()
        amend_button = tk.Button(self, text="Change a recipe",
                                 command=lambda: controller.show_frame(AmendRecipe, parent))
        amend_button.pack()
        add_recipe_button = tk.Button(self, text="Add a recipe",
                                      command=lambda: controller.show_frame(AddRecipe, parent))
        add_recipe_button.pack()
        delete_recipe_button = tk.Button(self, text="Delete a recipe",
                                         command=lambda: controller.show_frame(DeleteRecipe, parent))
        delete_recipe_button.pack()
        add_column_button = tk.Button(self, text="Add a new attribute",
                                         command=lambda: controller.show_frame(AddColumn, parent))
        add_column_button.pack()
        delete_column_button = tk.Button(self, text="Delete an attribute",
                                      command=lambda: controller.show_frame(DeleteColumn, parent))
        delete_column_button.pack()
        add_default_button = tk.Button(self, text="Add or change a default value",
                                      command=lambda: controller.show_frame(AddDefault, parent))
        add_default_button.pack()
        add_del_option_button = tk.Button(self, text="Add or delete and option",
                                       command=lambda: controller.show_frame(AddDeleteOption, parent))
        add_del_option_button.pack()
        back_button = tk.Button(self, text="Back to homepage", command=lambda: controller.show_frame(StartPage, parent))
        back_button.pack()

    def view_full_list(self):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        full_win = tk.Toplevel()
        full_win.wm_title("Full Recipe Book")
        c.execute("""SELECT meal FROM RecipeList""")
        full_book = c.fetchall()
        exploded_list = ([item for t in full_book for item in t])
        final_display = ("\n".join(exploded_list))
        z = StringVar()
        z.set(final_display)
        full_lbl = tk.Label(full_win, text="", font=LARGE_FONT)
        full_lbl.pack(pady=10, padx=10)
        full_lbl.configure(text=final_display)
        full_button_m = tk.Button(full_win, text="Close Window", command=full_win.destroy)
        full_button_m.pack()
        conn.close()


class CustomSearch (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='orange')
        self.cs_widgets_list = []
        self.ct_widgets_list = []
        self.dict_to_use = {}
        self.temp_dict = {}
        self.potential_meals = []
        self.make_dict(controller, 0, parent)

    def make_dict_to_use(self, sv, item):
        val = sv.get()
        vali = val[2:-3]
        self.temp_dict = {str(item): vali}
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
            cut_off_meal = make_row_a_list[1:]
            mapped = zip(cut_off_meal, final_list)
            counter = 0
            for i in mapped:
                if i[0] == i[1]:
                    counter += 1
            if counter == x:
                self.potential_meals.append(row[0])
        conn.close()

    def pop_upper(self):
        cust_win_m = tk.Toplevel()
        cust_win_m.wm_title("Custom Search Results")
        cust_lbl = tk.Label(cust_win_m, text="", font=LARGE_FONT)
        cust_lbl.pack(pady=10, padx=10)
        final_display = ("\n".join(self.potential_meals))
        cust_lbl.configure(text=final_display)
        cust_button_m = tk.Button(cust_win_m, text="Close Window", command=cust_win_m.destroy)
        cust_button_m.pack()
        if len(self.potential_meals) == 0:
            custn_lbl = tk.Label(cust_win_m, text="No matches", font=LARGE_FONT)
            custn_lbl.pack(pady=10, padx=10)

    def make_dict(self, controller, x, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        cursor = conn.execute('select * FROM RecipeList')
        names = list(map(lambda x: x[0], cursor.description))
        names1 = names[1:]
        s = shelve.open('test_shelf.db')
        cst = s['title_holder']
        nice_names = list(cst.values())
        nice_names1 = nice_names[1:]
        # for widget in self.cs_widgets_list:
        #     widget.destroy()
        # for widget in self.ct_widgets_list:
        #     widget.destroy()
        for item in names1:
            self.dict_to_use[item] = ""

        for nice_item in nice_names1:
            self.lbel = tk.Label(self, text=nice_item, font=LARGE_FONT)
            self.lbel.pack()
            print(nice_item)
            self.cs_widgets_list.append(self.lbel)
        for item in names1:
            c.execute("SELECT " + item + " FROM RecipeList")
            fetch = c.fetchall()
            ohfetch = StringVar()
            sfetch = set(fetch)
            ohfetch.trace("w", lambda name, index, mode, item =item, sv=ohfetch: self.make_dict_to_use(sv, item))
            self.box = OptionMenu(self, ohfetch, 'Empty', *sfetch)
            self.box.pack()
            self.cs_widgets_list.append(self.box)
        conn.close()
        cust_button_m = tk.Button(self, text="Show Results", command=self.pop_upper)
        cust_button_m.pack()
        # cust_button_m2 = tk.Button(self, text="Back to Homepage",
        #                            command=lambda: self.make_dict(controller, 1, parent))
        cust_button_m2 = tk.Button(self, text="Back to Homepage",
                                   command=lambda: self.home(controller, parent))
        cust_button_m2.pack()
        self.ct_widgets_list.append(cust_button_m)
        self.ct_widgets_list.append(cust_button_m2)

    def home(self, controller, parent):
        for widget in self.cs_widgets_list:
            widget.destroy()
        for widget in self.ct_widgets_list:
            widget.destroy()
        controller.show_frame(StartPage, parent)

        # if x == 1:
        #     controller.show_frame(StartPage, parent)


class AmendRecipe (tk.Frame):
    conn = sqlite3.connect('master.db')
    c = conn.cursor()
    cursor = conn.execute('select * FROM RecipeList')
    names = list(map(lambda x: x[0], cursor.description))
    names1 = names[1:]
    meal = names[0]
    meal_cut = meal[2:-2]
    # c.execute('select * from RecipeListTitleHolder')
    s = shelve.open('test_shelf.db')
    at = s['title_holder']
    am_nice_names = list(at.values())
    conn.close()
    am_nice_names1 = am_nice_names[1:]
    amend_recipe_dict = {}
    holding_dict = {}
    holding_dict_meal = {}

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.list_of_widgets = []
        self.f1list_of_widgets = []
        self.clist_of_widgets = []
        self.frame = Frame(self)
        self.frame.place(x=5, y=5)
        self.frame2 = Frame(self)
        self.frame2.pack()
        self.meal_box_maker(controller, 0, parent)

    def meal_box_maker(self, controller, x, parent):
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
        self.mlistbox = Listbox(self.frame, width=70, height=50)
        self.mlistbox.pack(side='left', fill='y')
        scrollbar = Scrollbar(self.frame, orient="vertical", command=self.mlistbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.f1list_of_widgets.append(scrollbar)
        self.mlistbox.insert(END, *am_exploded_list)
        self.mlistbox.config(yscrollcommand=scrollbar.set)
        mbm_button1 = tk.Button(self.frame2, text="Select Meal", command=lambda: self.to_stop_crash(controller, parent))
        mbm_button1.pack()
        mam_button2 = tk.Button(self.frame2, text="Back to homepage",
                                command=lambda: self.meal_box_maker(controller, 1, parent))
        mam_button2.pack()
        self.f1list_of_widgets.append(self.mlistbox)
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
        self.e = Entry(self.frame2)
        self.e.insert(END, self.value)
        self.e.pack()
        for nice_item in self.am_nice_names1:
            self.lbel = tk.Label(self.frame2, text=nice_item, font=LARGE_FONT)
            self.lbel.pack(side=LEFT)
            self.list_of_widgets.append(self.lbel)
        for item in self.names1:
            c.execute("SELECT " + item + " FROM RecipeList")
            every_value_am = c.fetchall()
            selected_var_am = StringVar()
            c.execute("SELECT " + item + " FROM RecipeList WHERE meal = (?)", (self.value,))
            current_value_for_meal = c.fetchall()
            selected_var_am.set(current_value_for_meal)
            options_list = set(every_value_am)
            selected_var_am.trace("w", lambda name, index, mode, item = item,
                                      sv=selected_var_am: self.store_values(sv, item))
            self.box = OptionMenu(self.frame2, selected_var_am, "Empty", *options_list)
            self.box.pack(side=LEFT)
            self.list_of_widgets.append(self.box)
        conn.close()
        am_button1 = tk.Button(self.frame2, text="Send changes", command=lambda: self.make_changes(controller, parent))
        am_button1.pack()
        am_button2 = tk.Button(self.frame2, text="Back to homepage",
                               command=lambda: self.meal_box_maker(controller, 1, parent))
        am_button2.pack()
        am_button3 = tk.Button(self.frame2, text="Back a page",
                               command=lambda: self.meal_box_maker(controller, 0, parent))
        am_button3.pack()
        self.list_of_widgets.append(am_button1)
        self.list_of_widgets.append(am_button2)
        self.list_of_widgets.append(am_button3)
        self.list_of_widgets.append(self.e)

    def store_values(self, sv, item):
        self.ctit= item
        self.vtit = sv.get()
        self.vtiti = self.vtit[2:-3]
        self.holding_dict[item] = self.vtiti

    def make_changes(self, controller, parent):
        self.new_meal_title = self.e.get()
        self.holding_dict_meal["new meal"] = self.new_meal_title
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
        conn.close()
        self.holding_dict_meal = {}
        self.holding_dict = {}
        for widget in self.list_of_widgets:
            widget.destroy()
        cam_button1 = tk.Button(self.frame2, text="Change another recipe",
                                command=lambda: self.meal_box_maker(controller, 0, parent))
        cam_button1.pack()
        cam_button2 = tk.Button(self.frame2, text="Back to homepage",
                                command=lambda: self.meal_box_maker(controller, 1, parent))
        cam_button2.pack()
        self.clist_of_widgets.append(cam_button1)
        self.clist_of_widgets.append(cam_button2)


class AddRecipe(tk.Frame):
    final_dict = {}
    holding_dict_meal = {}
    holding_dict = {}
    holding_dict_new = {}
    holding_dict_meal_new = {}
    final_first_dict = {}
    conn = sqlite3.connect('master.db')
    c = conn.cursor()
    cursor = conn.execute('select * FROM RecipeList')
    names = list(map(lambda x: x[0], cursor.description))
    names1 = names[1:]
    meal = names[0]
    optos = []
    conn.close()
    s = shelve.open('test_shelf.db')
    art = s['title_holder']
    add_nice_names = list(art.values())
    add_nice_names1 = add_nice_names[1:]
    first_meal = []

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
        for widget in self.opening_widgets:
            widget.destroy()
        first_meal_var = StringVar()
        first_meal_var.trace("w", lambda name, index, mode,
                                         msv1=first_meal_var: self.new_meal_maker(msv1, controller, parent))
        self.first_meal_entry = Entry(self.frame, textvariable=first_meal_var)
        self.first_meal_entry.pack()
        self.opening_widgets.append(self.first_meal_entry)
        for nice_item in self.add_nice_names1:
            a_lbel = tk.Label(self.frame, text=nice_item, font=LARGE_FONT)
            a_lbel.pack()
            self.opening_widgets.append(a_lbel)
        for name in self.names1:
            s = shelve.open('test_shelf.db')
            opto_stage = s['key1']
            self.optos = opto_stage[name]
            mi_var = StringVar()
            mi_var.set("Empty")
            self.mi_box = OptionMenu(self.frame, mi_var, 'Empty', *self.optos)
            mi_var.trace("w", lambda name, index, mode, ite=name,
                                              svm=mi_var: self.store_r_values(svm, ite, controller, parent))
            self.mi_box.pack()
            self.opening_widgets.append(self.mi_box)
        first_button2 = tk.Button(self.frame, text="Back to homepage",
                                  command=lambda: self.first_recipe(controller, 1, parent))
        first_button2.pack()
        self.opening_widgets.append(first_button2)
        if y == 1:
            controller.show_frame(StartPage, parent)

    def button_func(self, controller, parent):
        for widget in self.opening_widgets_sb:
            widget.destroy()
        self.ln1 = len(self.names)
        self.ln2 = len(self.first_meal)
        self.ln3 = len(self.final_first_dict.values())
        if self.ln2 != 0 and self.ln1 == self.ln3 and 'Empty' not in (self.final_first_dict.values()):
            first_button1 = tk.Button(self.frame, text="Send Recipe",
                                      command=lambda: self.make_first_changes(controller, parent))
            first_button1.pack()
            self.opening_widgets_sb.append(first_button1)

    def new_meal_maker(self, msv1, controller, parent):
        self.first_meal = msv1.get()
        self.holding_dict_meal_new['meal'] = self.first_meal
        self.button_func(controller, parent)

    def store_r_values(self, svm, ite, controller, parent):
        for widget in self.opening_widgets_sb:
            widget.destroy()
        self.knrec = ite
        self.vnrec = svm.get()
        self.holding_dict_new[ite] = self.vnrec
        self.final_first_dict = dict(self.holding_dict_meal_new, **self.holding_dict_new)
        self.button_func(controller, parent)

    def make_first_changes(self, controller, parent):
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
        first_button3 = tk.Button(self.frame, text="Add another recipe?",
                                  command=lambda: self.box_maker(controller, 0, parent))
        first_button3.pack()
        first_button4 = tk.Button(self.frame, text="Back to homepage",
                                  command=lambda: self.box_maker(controller, 1, parent))
        first_button4.pack()
        self.opening_widgets2.append(first_button3)
        self.opening_widgets2.append(first_button4)

    def box_maker(self, controller, x, parent):
        for widget in self.opening_widgets2:
            widget.destroy()
        for widget in self.list_of_widgets:
            widget.destroy()
        for widget in self.opening_widgets_sbn:
            widget.destroy()
        meal_var = StringVar()
        meal_var.trace("w", lambda name, index, mode, sv1=meal_var: self.make_meal_dict(sv1, controller, parent))
        meal_entry = Entry(self.frame, textvariable=meal_var)
        meal_entry.pack()
        for nice_item in self.add_nice_names1:
            self.lbel = tk.Label(self.frame, text=nice_item, font=LARGE_FONT)
            self.lbel.pack()
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
            self.box = OptionMenu(self.frame, selected_var_am, "Empty", *options_list)
            self.box.pack()
            self.list_of_widgets.append(self.box)
        conn.close()
        am_button2 = tk.Button(self.frame, text="Back to homepage",
                               command=lambda: self.box_maker(controller, 1, parent))
        am_button2.pack()
        self.list_of_widgets.append(am_button2)
        self.list_of_widgets.append(meal_entry)
        if x == 1:
            controller.show_frame(StartPage, parent)

    def button_norm_func(self, controller, parent):
        for widget in self.opening_widgets_sbn:
            widget.destroy()
        self.ln1 = len(self.names1)
        self.ln2 = len(self.new_meal_title)
        self.ln3 = len(self.holding_dict.values())
        if self.ln2 != 0 and self.ln1 == self.ln3 and 'Empty' not in (self.holding_dict.values()):
            am_button1 = tk.Button(self.frame, text="Send Recipe",
                                      command=lambda: self.make_changes(controller, parent))
            am_button1.pack()
            self.opening_widgets_sbn.append(am_button1)

    def make_cat_dict(self, sv, item, controller, parent):
        self.ctit= item
        self.vtit = sv.get()
        self.holding_dict[item] = self.vtit
        self.button_norm_func(controller, parent)

    def make_meal_dict(self, sv1, controller, parent):
        self.new_meal_title = sv1.get()
        self.holding_dict_meal["meal"] = self.new_meal_title
        self.button_norm_func(controller, parent)

    def make_changes(self, controller, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        self.final_dict = dict(self.holding_dict_meal, **self.holding_dict)
        fin_values = list(self.final_dict.values())
        count = len(fin_values)
        sql = "INSERT INTO RecipeList VALUES(" + ",".join(count * ["?"]) + ")"
        c.execute(sql, fin_values)
        conn.commit()
        conn.close()
        self.holding_dict_meal = {}
        self.holding_dict = {}
        self.final_dict = {}
        self.box_maker(controller, 0, parent)


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
        self.meal_box_maker(controller, 0, parent)

    def meal_box_maker(self, controller, x, parent):
        for widget in self.f1list_of_widgets:
            widget.destroy()
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute("""SELECT meal FROM RecipeList""")
        am_full_book = c.fetchall()
        conn.close()
        am_exploded_list = ([item for t in am_full_book for item in t])
        self.listbox = Listbox(self.frame, selectmode = "multiple", width=70, height=50)
        self.listbox.pack(side='left', fill='y')
        scrollbar = Scrollbar(self.frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        delete_button1 = tk.Button(self.frame2, text="Send changes",
                                   command=lambda: self.delete_meal(controller, parent))
        delete_button1.pack()
        delete_button2 = tk.Button(self.frame2, text="Back to homepage",
                                   command=lambda: self.meal_box_maker(controller, 1, parent))
        delete_button2.pack()
        # delete_button3 = tk.Button(self, text="Refresh List",
        #                            command=lambda: self.meal_box_maker(controller, 0, parent))
        # delete_button3.pack()
        self.listbox.insert(END, *am_exploded_list)
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind('<<ListboxSelect>>', lambda event: self.list_of_selected())
        self.f1list_of_widgets.append(self.listbox)
        self.f1list_of_widgets.append(delete_button1)
        self.f1list_of_widgets.append(delete_button2)
        # self.f1list_of_widgets.append(delete_button3)
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
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        for i in self.ones_to_go:
            c.execute("DELETE FROM RecipeList WHERE meal =?", (i,))
            conn.commit()
        conn.close()
        self.meal_box_maker(controller, 0, parent)


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
        self.options_to_add = {}
        self.create_widgets(controller, 0, parent)

    def create_widgets(self, controller, x, parent):
        for widget in self.ac_list_of_widgets:
            widget.destroy()
        self.cwlbel = tk.Label(self.frame, text="Enter new attribute", font=LARGE_FONT)
        self.cwlbel.pack()
        self.new_column_box = Entry(self.frame)
        self.new_column_box.pack()
        self.cwlbel1 = tk.Label(self.frame, text="Enter options to choose from, please use a comma between"
                                                 " the options, eg - 'y, n'", font=LARGE_FONT)
        self.cwlbel1.pack()
        self.new_column_box1 = Entry(self.frame)
        self.new_column_box1.pack()
        self.new_col_button1 = tk.Button(self.frame2, text="Send new attribute",
                                    command=lambda: self.add_the_column(controller, parent))
        self.new_col_button1.pack()
        self.new_col_button2 = tk.Button(self.frame2, text="Back to homepage",
                                   command=lambda: self.create_widgets(controller, 1, parent))
        self.new_col_button2.pack()
        self.ac_list_of_widgets.append(self.cwlbel)
        self.ac_list_of_widgets.append(self.cwlbel1)
        self.ac_list_of_widgets.append(self.new_column_box)
        self.ac_list_of_widgets.append(self.new_column_box1)
        self.ac_list_of_widgets.append(self.new_col_button1)
        self.ac_list_of_widgets.append(self.new_col_button2)
        if x==1:
            controller.show_frame(StartPage, parent)

    def add_the_column(self, controller, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        new_column = self.new_column_box.get()
        not_nice_new_column = new_column.replace(" ", "")
        options_menu = self.new_column_box1.get().split(", ")
        options_menu_tester = len(options_menu)
        new_column_tester = len(new_column)
        if options_menu_tester == 0 or new_column_tester == 0:
            self.atclbel = tk.Label(self.frame, text="Please fill both boxes", font=LARGE_FONT)
            self.atclbel.pack()
            self.ac_list_of_widgets.append(self.atclbel)
            self.create_widgets(controller, 0)
        else:
            c.execute("""alter table RecipeList add """"" + not_nice_new_column + """""")
            conn.commit()
            conn.close()

            self.title_to_add = {not_nice_new_column: new_column}
            s = shelve.open('test_shelf.db')
            self.title_adder = s['title_holder']
            self.title_adder.update(self.title_to_add)
            s = shelve.open('test_shelf.db')
            del s['title_holder']
            s = shelve.open('test_shelf.db')
            s['title_holder'] = self.title_adder

            self.default_to_add = {not_nice_new_column: 'Any'}
            s = shelve.open('test_shelf.db')
            self.default_adder = s['default_holder']
            self.default_adder.update(self.default_to_add)
            s = shelve.open('test_shelf.db')
            del s['default_holder']
            s = shelve.open('test_shelf.db')
            s['default_holder'] = self.default_adder

            self.options_to_add = {not_nice_new_column: options_menu}
            s = shelve.open('test_shelf.db')
            self.options_adder = s['key1']
            self.options_adder.update(self.options_to_add)
            s = shelve.open('test_shelf.db')
            del s['key1']
            s = shelve.open('test_shelf.db')
            s['key1'] = self.options_adder
            self.destroy_create(not_nice_new_column, options_menu, controller, parent)

    def destroy_create(self, not_nice_new_column, options_menu, controller, parent):
        for widget in self.ac_list_of_widgets:
            widget.destroy()
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        c.execute("SELECT meal FROM RecipeList")
        self.meal_for_new_values = c.fetchall()
        conn.close()
        for m in self.meal_for_new_values:
            self.make_widgets(*m, options_menu, not_nice_new_column)
        self.dc_meal_lb = tk.Label(self.frame, text="Book updated", font=LARGE_FONT)
        self.dc_meal_lb.pack()
        self.dc_button = tk.Button(self.frame2, text="Back to homepage",
                                   command=lambda: controller.show_frame(StartPage, parent))
        self.dc_button.pack()

    def make_widgets(self, m, options_menu, not_nice_new_column):
        self.mw_meal_lb = tk.Label(self.frame, text=m, font=LARGE_FONT)
        self.mw_meal_lb.pack()
        var = StringVar()
        self.mw_box = OptionMenu(self.frame, var, *options_menu)
        self.mw_box.pack()
        wait_var = tk.IntVar()
        self.mw_button = tk.Button(self.frame, text="Send", command=lambda: wait_var.set(1))
        self.mw_button.pack()
        wait_var = tk.IntVar()
        self.mw_button.wait_variable(wait_var)
        self.ac_list_of_widgets.append(self.mw_meal_lb)
        self.ac_list_of_widgets.append(self.mw_box)
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


class DeleteColumn(tk.Frame):
    one_to_del = []
    names = []
    lbdel_get = []
    columns_to_stay = []
    dl_list_of_widgets = []
    options_dict = {}
    set_list = set()
    title_deleter = {}
    default_deleter = {}
    options_deleter = {}

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.ac_list_of_widgets = []
        self.frame = Frame(self)
        self.frame.place(x=5, y=5)
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
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        del_cursor = conn.execute('select * FROM RecipeList')
        self.names = list(map(lambda x: x[0], del_cursor.description))
        conn.close()
        self.names.pop(0)
        self.delc_meal_lb = tk.Label(self.frame, text="Select attribute to delete", font=LARGE_FONT)
        self.delc_meal_lb.pack()
        self.delc_listbox = Listbox(self.frame, selectmode="single", width=70, height=50)
        self.delc_listbox.pack(side='left', fill='y')
        delete_col_button1 = tk.Button(self.frame, text="Send changes",
                                       command=lambda: self.create_columns_in_temp())
        delete_col_button1.pack()
        delete_col_button2 = tk.Button(self.frame, text="Back to homepage",
                                   command=lambda: controller.show_frame(StartPage, parent))
        delete_col_button2.pack()
        self.delc_listbox.insert(END, *self.names)
        self.delc_listbox.bind('<<ListboxSelect>>', lambda event: self.selected_col())
        self.dl_list_of_widgets.append(self.delc_meal_lb)
        self.dl_list_of_widgets.append(self.delc_listbox)
        self.dl_list_of_widgets.append(delete_col_button1)

    def selected_col(self):
        lbdel_items = self.delc_listbox.curselection()
        self.lbdel_get = self.delc_listbox.get(lbdel_items)

    def create_columns_in_temp(self):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        self.columns_to_stay = [x for x in self.names if x not in self.lbdel_get]
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
        for widget in self.dl_list_of_widgets:
            widget.destroy()
        delt_meal_lb = tk.Label(self.frame, text="Column deleted", font=LARGE_FONT)
        delt_meal_lb.pack()


class AddDefault (tk.Frame):
    conn = sqlite3.connect('master.db')
    c = conn.cursor()
    s = shelve.open('test_shelf.db')
    adt = s['title_holder']
    add_def_nice_names = list(adt.values())
    add_def_nice_names1 = add_def_nice_names[1:]
    options_list = set()
    cursor = conn.execute('select * FROM RecipeList')
    names = list(map(lambda x: x[0], cursor.description))
    conn.close()
    names1 = names[1:]
    def_dict = {}
    ad_list_of_widgets = []
    ad1_list_of_widgets = []

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.frame = Frame(self)
        self.frame.pack()
        self.make_def_screen(controller, 0, parent)

    def make_def_screen (self, controller, x, parent):
        for widget in self.ad1_list_of_widgets:
            widget.destroy()
        self.def_lbel2 = tk.Label(self.frame, text="Enter either what you want, o"
                                                   "r what you don't want, eg beef or not beef "
                                                   "-- use 'any' if you're not bother", font=LARGE_FONT)
        self.def_lbel2.pack()
        self.ad_list_of_widgets.append(self.def_lbel2)
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        for item in self.names1:
            c.execute("SELECT " + item + " FROM RecipeList")
            def_every_value_am = c.fetchall()
            self.options_list = set(def_every_value_am)
            self.x = [i for i in self.options_list]
            s = shelve.open('test_shelf.db')
            adt = s['default_holder']
            self.d = adt[item]
            self.def_lbel1 = tk.Label(self.frame, text=self.x, font=LARGE_FONT)
            self.def_lbel1.pack()
            self.ad_list_of_widgets.append(self.def_lbel1)
            def_meal_var = StringVar()
            def_meal_var.set(self.d)
            def_meal_var.trace("w", lambda name, index, mode,
                                           item=item, sv1=def_meal_var: self.make_def_dict(sv1, item))
            def_meal_entry = Entry(self.frame, textvariable=def_meal_var)
            def_meal_entry.pack()
            self.ad_list_of_widgets.append(def_meal_entry)
        conn.close()
        for nice_item in self.add_def_nice_names1:
            self.def_lbel = tk.Label(self.frame, text=nice_item, font=LARGE_FONT)
            self.def_lbel.pack()
            self.ad_list_of_widgets.append(self.def_lbel)
        am_button1 = tk.Button(self.frame, text="Send changes",
                               command=lambda: self.make_def_changes(controller, parent))
        am_button1.pack()
        am_button2 = tk.Button(self.frame, text="Back to homepage",
                               command=lambda: controller.show_frame(StartPage, parent))
        am_button2.pack()
        self.ad_list_of_widgets.append(am_button1)
        self.ad_list_of_widgets.append(am_button2)
        if x == 1:
            controller.show_frame(StartPage)

    def make_def_dict(self, sv1, item):
        self.def_dict[item] = sv1.get().lower()

    def make_def_changes(self, controller, parent):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        for key in self.def_dict:
            c.execute("SELECT " + key + " FROM RecipeList")
            check_value = c.fetchall()
            set_checker = set(check_value)
            explode_check = [item for t in set_checker for item in t]
            check_val = self.def_dict[key]
            if check_val not in explode_check:
                for widget in self.ad_list_of_widgets:
                    widget.destroy()
                self.def_lbel3 = tk.Label(self.frame, text="That does not exist! Try again, check typos",
                                          font=LARGE_FONT)
                self.def_lbel3.pack()
                am_button3 = tk.Button(self.frame, text="Try again",
                                       command=lambda: self.make_def_screen(controller, 0, parent))
                am_button3.pack()
                self.ad1_list_of_widgets.append(self.def_lbel3)
            else:
                for widget in self.ad_list_of_widgets:
                    widget.destroy()
                for key in self.def_dict:
                    valval=self.def_dict[key]
                    s = shelve.open('test_shelf.db')
                    ud = s['default_holder']
                    ud[key] = valval
                    s = shelve.open('test_shelf.db')
                    del s['default_holder']
                    s = shelve.open('test_shelf.db')
                    s['default_holder'] = ud
                am_button4 = tk.Button(self.frame, text="Change another default",
                                       command=lambda: self.make_def_screen(controller, 0, parent))
                am_button4.pack()
                am_buttonx = tk.Button(self.frame, text="Back to homepage",
                                       command=lambda: self.make_def_screen(controller, 1, parent))
                am_buttonx.pack()
                self.ad1_list_of_widgets.append(am_button4)
                self.ad1_list_of_widgets.append(am_buttonx)
        conn.close()


class AddDeleteOption (tk.Frame):
    conn = sqlite3.connect('master.db')
    c = conn.cursor()
    s = shelve.open('test_shelf.db')
    adot = s['title_holder']
    ado_def_nice_names = list(adot.values())
    ado_def_nice_names1 = ado_def_nice_names[1:]
    options_list = set()
    cursor = conn.execute('select * FROM RecipeList')
    ad_names = list(map(lambda x: x[0], cursor.description))
    conn.close()
    ad_names1 = ad_names[1:]
    ado_add_dict = {}
    ado_del_dict = {}
    # ado_list_of_widgets = []
    # ado_list_of_widgets1 = []
    add_to_list = []
    to_add = []
    to_del = []
    list_del = []

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.frame = Frame(self)
        self.frame.pack()
        self.ado_list_of_widgets = []
        self.ado_list_of_widgets1 = []
        self.make_labels_boxes(controller, 0, parent)

    def make_labels_boxes(self, controller, z, parent):
        for widget in self.ado_list_of_widgets:
            widget.destroy()
        for widge in self.ado_list_of_widgets1:
            widge.destroy()
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        self.ado_lbel1 = tk.Label(self.frame, text="Category", font=LARGE_FONT)
        self.ado_lbel1.pack(side=LEFT)
        self.ado_list_of_widgets.append(self.ado_lbel1)
        self.ado_lbel2 = tk.Label(self.frame, text="Delete Option", font=LARGE_FONT)
        self.ado_lbel2.pack(side=LEFT)
        self.ado_list_of_widgets.append(self.ado_lbel2)
        self.ado_lbel3 = tk.Label(self.frame, text="Add Option", font=LARGE_FONT)
        self.ado_lbel3.pack(side=LEFT)
        self.ado_list_of_widgets.append(self.ado_lbel3)
        for ado_item in self.ado_def_nice_names1:
            self.ado_lbel = tk.Label(self.frame, text=ado_item, font=LARGE_FONT)
            self.ado_lbel.pack(side=LEFT)
            self.ado_list_of_widgets.append(self.ado_lbel)
        for ite in self.ad_names1:
            ado_om_var = StringVar()
            s = shelve.open('test_shelf.db')
            existing = s['key1']
            ex_o = existing[ite]
            ado_om_var.trace("w", lambda name, index, mode, item=ite,
                                              sv=ado_om_var: self.del_store_values(sv, item))
            self.box_ado = OptionMenu(self.frame, ado_om_var, "Empty", *ex_o)
            self.box_ado.pack(side=LEFT)
            self.ado_list_of_widgets.append(self.box_ado)
            ado_entry_var = StringVar()
            ado_entry_var.trace("w", lambda name, index, mode, item1=ite,
                                         sv1=ado_entry_var: self.add_store_values(sv1, item1))
            self.ado_entry = Entry(self.frame, textvariable=ado_entry_var)
            self.ado_entry.pack()
            self.ado_list_of_widgets.append(self.ado_entry)
        conn.close()
        ado_button_1 = tk.Button(self, text="Send Changes",
                                 command=lambda: self.update_pers_dict(controller, parent))
        ado_button_1.pack()
        ado_button_2 = tk.Button(self, text="Back to Homepage",
                                 command=lambda: self.make_labels_boxes(controller, 1, parent))
        ado_button_2.pack()
        self.ado_list_of_widgets.append(ado_button_1)
        self.ado_list_of_widgets.append(ado_button_2)
        if z == 1:
            controller.show_frame(StartPage, parent)

    def del_store_values(self, sv, item):
        ado_del = sv.get()
        self.ado_del_dict[item] = ado_del

    def add_store_values(self, sv1, item1):
        ado_add = sv1.get()
        self.ado_add_dict[item1] = ado_add

    def update_pers_dict(self, controller, parent):
        s = shelve.open('test_shelf.db')
        existing = s['key1']
        for k in self.ado_add_dict:
            self.to_add = self.ado_add_dict[k]
            self.add_to_list = existing[k]
            if self.to_add in self.add_to_list:
                for widget in self.ado_list_of_widgets:
                    widget.destroy()
                for widget in self.ado_list_of_widgets1:
                    widget.destroy()
                self.ado_lbel_exist = tk.Label(self.frame,
                                               text="That option already exist", font=LARGE_FONT)
                self.ado_lbel_exist.pack()
                ado_button_7 = tk.Button(self, text="Try Again",
                                         command=lambda: self.make_labels_boxes(controller, 0, parent))
                ado_button_7.pack()
                ado_button_6 = tk.Button(self, text="Back to Homepage",
                                         command=lambda: self.make_labels_boxes(controller, 1, parent))
                ado_button_6.pack()
                self.ado_list_of_widgets1.append(ado_button_6)
                self.ado_list_of_widgets1.append(ado_button_7)
                self.ado_list_of_widgets1.append(self.ado_lbel_exist)
            else:
                list_add = list(self.add_to_list)
                list_add.append(self.to_add)
                existing[k] = list_add
                s = shelve.open('test_shelf.db')
                del s['key1']
                s = shelve.open('test_shelf.db')
                s['key1'] = existing

        for ke in self.ado_del_dict:
            conn = sqlite3.connect('master.db')
            c = conn.cursor()
            c.execute("SELECT " + ke + " FROM RecipeList")
            if_exists = c.fetchall()
            ex_if_exists = [a for b in if_exists for a in b]
            set_ex_if_exists = set(ex_if_exists)
            if self.ado_del_dict[ke] in set_ex_if_exists:
                for widget in self.ado_list_of_widgets:
                    widget.destroy()
                for widget in self.ado_list_of_widgets1:
                    widget.destroy()
                self.ado_lbel_wrong = tk.Label(self.frame,
                                    text="You are using that value, change recipes and try again", font=LARGE_FONT)
                self.ado_lbel_wrong.pack()
                ado_button_5 = tk.Button(self, text="Back to Homepage",
                                         command=lambda: self.make_labels_boxes(controller, 1, parent))
                ado_button_5.pack()
                self.ado_list_of_widgets1.append(ado_button_5)
                self.ado_list_of_widgets1.append(self.ado_lbel_wrong)
            else:
                self.to_del = self.ado_del_dict[ke]
                self.list_del = existing[ke]
                self.list_del.remove(self.to_del)
                existing[ke] = self.list_del
                s = shelve.open('test_shelf.db', writeback=True)
                del s['key1']
                s = shelve.open('test_shelf.db', writeback=True)
                s['key1'] = existing
            conn.close()
            self.ado_del_dict={}
            self.ado_add_dict={}
            for widget in self.ado_list_of_widgets:
                widget.destroy()
            for widget in self.ado_list_of_widgets1:
                widget.destroy()
            ado_button_3 = tk.Button(self, text="Make another change",
                                     command=lambda: self.make_labels_boxes(controller, 0, parent))
            ado_button_3.pack()
            ado_button_4 = tk.Button(self, text="Back to Homepage",
                                     command=lambda: self.make_labels_boxes(controller, 1, parent))
            ado_button_4.pack()
            self.ado_list_of_widgets1.append(ado_button_3)
            self.ado_list_of_widgets1.append(ado_button_4)


class CustomPlan(tk.Frame):
    conn = sqlite3.connect('master.db')
    c = conn.cursor()
    cursor = conn.execute('select * FROM RecipeList')
    col_names = list(map(lambda x: x[0], cursor.description))
    col_names1 = col_names[1:]
    col_meal = col_names[0]
    day_attr_val_dict = {}
    dict_to_fill = {}
    day_potmeals = {}
    no_days = {}
    list_days = {}
    list_no_days = []
    final_pl_display = []
    keep_track_widgets_dict = {}
    widgets_box_list = []
    random_template = {}
    s = shelve.open('test_shelf.db')
    ct = s['title_holder']
    cp_nice_names = list(ct.values())
    conn.close()
    default_dict = {}
    def_dict = {}
    to_zip = []
    yes_dict = {}
    no_dict = {}
    meal_list_after_def = []
    set_of_meals = set()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        for item in self.col_names:
            self.dict_to_fill[item] = ""
        self.ac_list_of_widgets = []
        self.frame = Frame(self)
        self.frame.pack(side=LEFT)
        self.frame2 = Frame(self)
        self.frame2.pack(side=TOP)
        self.frame3 = Frame(self)
        self.frame3.pack(side=BOTTOM)
        self.days_to_customise = []
        self.results = {'Monday': '', 'Tuesday': '', 'Wednesday': '', 'Thursday': '',
                        'Friday': '', 'Saturday': '', 'Sunday': ''}
        self.make_days(controller, parent)

    def make_days(self, controller, parent):
        self.md_listbox = Listbox(self.frame, selectmode="multiple", width=70, height=50)
        self.md_listbox.pack(side='left', fill='y')
        self.md_listbox.insert(END, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        self.md_listbox.bind('<<ListboxSelect>>', lambda event: self.days_collector())
        self.md_button = tk.Button(self.frame, text="Send Days",
                                   command=lambda: self.make_custom_screen(controller, parent))
        self.md_button.pack()

    def days_collector(self):
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

    def make_custom_screen(self, controller, parent):
        self.md_listbox.destroy()
        self.md_button.destroy()
        for nice_de_item in self.cp_nice_names:
            self.mcs_label = tk.Label(self.frame2, text=nice_de_item, font=LARGE_FONT)
            self.mcs_label.pack(side=LEFT)
        self.mcs_label1 = tk.Label(self.frame2, text="Tick to leave day blank", font=LARGE_FONT)
        self.mcs_label.pack(side=LEFT)
        for de_dy in self.list_sorted:
            self.vard = de_dy
            self.de_label = tk.Label(self.frame, text=self.vard, font=LARGE_FONT)
            self.de_label.pack(side=TOP)
            frame_factory = Frame(self)
            frame_factory.pack()
            yesno = BooleanVar()
            self.tickbox = tk.Checkbutton(frame_factory, variable=yesno)
            yesno.trace("w", lambda name, index, mode, day1=de_dy, svari=yesno: self.make_no_dict(day1, svari))
            self.tickbox.pack(side=LEFT)
            conn = sqlite3.connect('master.db')
            c = conn.cursor()
            for de_item in self.col_names:
                c.execute("SELECT " + de_item + " FROM RecipeList")
                fetch_col_contents = c.fetchall()
                chosen_var = StringVar()
                chosen_var.set(de_dy)
                unique_options_list = set(fetch_col_contents)
                chosen_var.trace("w", lambda name, index, mode, item=de_item, dy=de_dy,
                                             sv=chosen_var: self.populate_custom_dict(sv, dy, item))
                self.box = OptionMenu(frame_factory, chosen_var, *unique_options_list)
                self.box.pack(side=LEFT)
                self.widgets_box_list.append(self.box)
            conn.close()
            self.keep_track_widgets_dict[de_dy] = self.widgets_box_list
        cust_button_m = tk.Button(self, text="Show Results", command=lambda: self.make_default_dict())
        cust_button_m.pack()
        de_button_m2 = tk.Button(self, text="Back to Homepage",
                                 command=lambda: controller.show_frame(StartPage, parent))
        de_button_m2.pack(side=BOTTOM)

    def make_no_dict(self, day1, svari):
        val = svari.get()
        self.no_days[day1] = val

    def populate_custom_dict (self, sv, dy, item):
        pcd_val = sv.get()
        pcd_val_usable = pcd_val[2:-3]
        self.day_attr_val_dict[dy] = {str(item): pcd_val_usable}

    def make_default_dict(self):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        cursor = conn.execute('select * FROM RecipeList')
        def_col_names = list(map(lambda x: x[0], cursor.description))
        def_col_names1 = def_col_names[1:]
        s = shelve.open('test_shelf.db')
        self.default_dict = s['default_holder']
        self.def_dict = {key:value for (key, value) in self.default_dict.items() if value != 'any'}
        for key in self.def_dict:
            if self.def_dict[key][0:3] != 'not':
                self.yes_dict[key] = self.def_dict[key]
            if self.def_dict[key][0:3] == 'not':
                self.no_dict[key] = self.def_dict[key]
        for key in self.yes_dict:
            valy = self.yes_dict[key]
            c.execute("select meal from RecipeList WHERE " + key + "=?", (valy,))
            yes = c.fetchall()
            self.meal_list_after_def.append(yes)
        for key in self.no_dict:
            valn = self.yes_dict[key]
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
            c.execute('select * from RecipeList')
            no_deff = c.fetchall()
            self.set_of_meals = ([item for t in no_deff for item in t])
            conn.close()
        self.calc_pot_meals_custom()

    def calc_pot_meals_custom(self):
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        for k in self.no_days:
            if [k]:
                self.list_no_days.append(k)
        for day in self.day_attr_val_dict:
            if [day] in self.list_no_days:
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
                # c.execute('select * from RecipeList WHERE meal = (?)', (meal,))
                # row = c.fetchall()
                make_row_a_list = list(row)
                mapped = zip(make_row_a_list, final_list)
                counter = 0
                for i in mapped:
                    if i[0] == i[1]:
                        counter += 1
                if counter == x:
                    self.cp_potential_meals.append(row[0])
            self.day_potmeals[self.day] = self.cp_potential_meals
        conn.close()
        self.gen_week()

    def gen_week(self):
        tups = []
        day = []
        for k in sorted(self.day_potmeals, key=lambda k: len(self.day_potmeals[k])):
            tups.append(self.day_potmeals[k])
            day.append(k)
        thebig = []
        for list_meals in tups:
            for meal in list_meals:
                if meal in thebig:
                    list_meals.remove(meal)
            thebig.append(random.choice(list_meals))
            self.template = dict(zip(day, thebig))
        self.make_dict_full()

    def make_dict_full(self):
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
        self.pop_results(**end_crit_dict)

    def pop_results(self, **kwargs):
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
        self.calc_results(**kwargs)

    def calc_results(self, **kwargs):
        existing_meals = list(kwargs.values())
        self.final_meal_list = [x for x in self.set_of_meals if x not in existing_meals]
        self.pop_upper(**kwargs)

    def pop_upper(self, **kwargs):
        for k, v in kwargs.items():
            if not v:
                kwargs[k] = random.choice(self.final_meal_list)
            if kwargs[k] in self.final_meal_list:
                self.final_meal_list.remove(kwargs[k])
        cust_pl_win = tk.Toplevel()
        cust_pl_win.title("Custom Plan Results")
        monday_lbl = tk.Label(cust_pl_win, text=kwargs["Monday"], font=LARGE_FONT)
        monday_lbl.pack(side=TOP)
        tuesday_lbl = tk.Label(cust_pl_win, text=kwargs["Tuesday"], font=LARGE_FONT)
        tuesday_lbl.pack(side=TOP)
        wednesday_lbl = tk.Label(cust_pl_win, text=kwargs["Wednesday"], font=LARGE_FONT)
        wednesday_lbl.pack(side=TOP)
        thursday_lbl = tk.Label(cust_pl_win, text=kwargs["Thursday"], font=LARGE_FONT)
        thursday_lbl.pack(side=TOP)
        friday_lbl = tk.Label(cust_pl_win, text=kwargs["Friday"], font=LARGE_FONT)
        friday_lbl.pack(side=TOP)
        saturday_lbl = tk.Label(cust_pl_win, text=kwargs["Saturday"], font=LARGE_FONT)
        saturday_lbl.pack(side=TOP)
        sunday_lbl = tk.Label(cust_pl_win, text=kwargs["Sunday"], font=LARGE_FONT)
        sunday_lbl.pack(side=TOP)
        cust_pl_button_m = tk.Button(cust_pl_win, text="Close Window", command=cust_pl_win.destroy)
        cust_pl_button_m.pack()


app = MenuQ()
app.mainloop()
#
# MenuQ()
# mainloop()

