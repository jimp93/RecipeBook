import tkinter as tk
from tkinter import *
import sqlite3
import random
import re

conn = sqlite3.connect('master.db')
c = conn.cursor()

# CREATE ORIGINAL


c.execute("""CREATE TABLE IF NOT EXISTS Recipe_List_Custom (
    meal text,
    MainIngredient text,
    expense text,
    PrepTime text
    )""")
conn.commit()


# RECIPE BOOK

def slicer(n):
    return n[:3]

criteria = {}
line = []
recipe_dict = {}
cursor = conn.execute('select * FROM Recipe_List_Custom')
customised_rows = list(map(lambda x: x[0], cursor.description))
count = len(customised_rows)
customised_rows_low = [x.lower() for x in customised_rows]
abbrev_customised_rows = map(slicer, customised_rows_low)
custom_dict = dict(zip(abbrev_customised_rows, customised_rows))
for i in customised_rows_low:
    recipe_dict[i] = ''


def create_columns_in_temp():
    new_column = input('what other factor do you want to add ?' '\n')
    c.execute("""alter table Recipe_Tester add """"" + new_column + """""")

    def update_new_column():
        c.execute("SELECT * FROM Recipe_Tester")
        for row in c.fetchall():
            print(row[0])
            what_to = input('new ' + new_column + ' value? ')
            c.execute("UPDATE Recipe_Tester SET " + new_column + " = (?) WHERE meal = (?)", (what_to, row[0]))
            conn.commit()
    update_new_column()


def view_all_recipes():

    c.execute("""SELECT meal FROM Recipe_List_Custom""")
    print(c.fetchall())
    # for row in c.fetchall():
    #     return" ".join(map(str, row))


def custom_view_recipes():
    attributer_val = ()
    main_choice = ()
    attributer = input('Enter first three letters of attribute?' '\n').lower()
    attributer_val = custom_dict[attributer]
    main_choice = input('which category do you want to view?' '\n').lower()
    c.execute("""SELECT meal FROM Recipe_List_Custom WHERE (""" + attributer_val + """) = (?)""", (main_choice,))
    for row in c.fetchall():
        print(" ".join(map(str, row)))


def dynamic_data_entry():
    for k in recipe_dict:
        recipe_dict[k] = input(k + "? ").lower()
    column = list(recipe_dict.keys())
    values = list(recipe_dict.values())
    c.execute("""INSERT INTO Recipe_List_Custom VALUES(" + ",".join(count * ["?"]""", (values,))
    conn.commit()
    and_then = input("Do you want to add another recipe?" '\n').lower()
    if and_then == 'y':
        dynamic_data_entry()
    # if and_then == 'n':
    else:
        print('Try again! ' '\n')
        dynamic_data_entry()


def delete_entries():
    if input('To clear the whole book, click "x", to clear one entry, click "d"' '\n').lower() == 'x':
        if input('Are you sure you want to clear the whole book? y/n' '\n').lower() == 'y':
            c.execute("""DELETE FROM Recipe_List_Custom""")
            conn.commit()
    meal_to_delete = input('Which meal is getting the chop?' '\n').lower()
    c.execute("DELETE FROM Recipe_List_Custom WHERE meal =?", (meal_to_delete,))
    conn.commit()



def amend_entries():
    def add_it_in():
        c.execute("UPDATE Recipe_List_Custom SET " + parameter + " = (?) WHERE meal = (?)", (what_to, meal_to_change))
        conn.commit()
    meal_to_change = input('Which meal do you want to change?' '\n').lower()
    attribute = input("Enter first three letters of the attribute to change "'\n').lower()
    what_to = input('What do you want to change it to?' '\n').lower()
    parameter = custom_dict[attribute]
    add_it_in()


# def recipe_next_move():
#     the_next_thing = input('To view recipe book, type "v"' '\n'
#             'To add to recipe book, type "a"' '\n'
#             'To delete from recipe book, type "d"' '\n'
#             'To tweak a recipe, type "t"' '\n'
#             'To add a new column type "c').lower()
#     if the_next_thing == 'v':
#         view_recipes()
#     if the_next_thing == 'a':
#         dynamic_data_entry()
#     if the_next_thing == 'd':
#         delete_entries()
#     if the_next_thing == 't':
#         amend_entries()
#     if the_next_thing == 'c':
#         create_columns_in_temp()
#     else:
#         print('Try again! ' '\n')
#         recipe_next_move()

# MEAL CALCULATOR


def pop_results(**kwargs):
    days_to_pop = input("Are there any days that don't need filling? " '\n')
    days_to_pop_list = list(days_to_pop.split(','))
    days_to_pop_low = [item.lower() for item in days_to_pop_list]
    if 'mon' in days_to_pop_low or 'monday' in days_to_pop_low:
        kwargs['Monday'] = 'N/A'
    if 'tue' in days_to_pop_low or 'tues' in days_to_pop_low or 'tuesday' in days_to_pop_low:
        kwargs['Tuesday'] = 'N/A'
    if 'wed' in days_to_pop_low or 'wednesday' in days_to_pop_low:
        kwargs['Wednesday'] = 'N/A'
    if 'thu' in days_to_pop_low or 'thurs' in days_to_pop_low or 'thursday' in days_to_pop_low:
        kwargs['Thursday'] = 'N/A'
    if 'fri' in days_to_pop_low or 'friday' in days_to_pop_low:
        kwargs['Friday'] = 'N/A'
    if 'sat' in days_to_pop_low or 'saturday' in days_to_pop_low:
        kwargs['Saturday'] = 'N/A'
    if 'sun' in days_to_pop_low or 'sunday' in days_to_pop_low:
        kwargs['Sunday'] = 'N/A'

    def ta_da_defs():
        too_posh = []
        c.execute("""SELECT meal FROM Recipe_List_Custom WHERE expense ='p'""")
        expenser = c.fetchall()
        c.execute("""SELECT meal FROM Recipe_List_Custom WHERE PrepTime ='t'""")
        prepper = c.fetchall()
        expenser.append(prepper)
        for i in expenser:
            if i not in too_posh:
                too_posh.append(i)
        c.execute("""SELECT meal FROM Recipe_List_Custom""")
        the_lot = c.fetchall()
        raw_meal_list = [x for x in the_lot if x not in too_posh]
        exploded_raw_meal_list = [i[0] for i in raw_meal_list]
        existing_meals = list(kwargs.values())
        final_meal_list = [x for x in exploded_raw_meal_list if x not in existing_meals]

        def this_is_the_end():
            for k, v in kwargs.items():
                if not v:
                    kwargs[k] = random.choice(final_meal_list)
                if kwargs[k] in final_meal_list:
                    final_meal_list.remove(kwargs[k])
            for k, v in kwargs.items():
                print(k, '--', v, '\n')
            # opener()
        this_is_the_end()
    ta_da_defs()


# INPUT REQUIREMENTS

def pick_or_not():
    results = {'Monday': '', 'Tuesday': '', 'Wednesday': '', 'Thursday': '',
            'Friday': '', 'Saturday': '', 'Sunday': ''}

    def special_days_input():
        day_meals = {}
        pick = input("To make a detailed search, type 'd'" '\n'
                     "for random search type 'r' \n").lower()
        if pick == 'r':
            pop_results(**results)
        if pick != 'd':
            print('Try again! ' '\n')
            special_days_input()

        def enter_days():
            c.execute('select * from Recipe_List_Custom')
            days = input("Which day requires special instruction" '\n').lower()

            def enter_reqs():
                rx = re.compile(r'(?<=[a-z])(?=[A-Z])')
                for_entry = [rx.sub(' ', string_meal) for string_meal in customised_rows]
                for string_meal in for_entry:
                    criteria[string_meal] = input(string_meal + "? " '\n')

                def set_calc(criteria):
                    if criteria['expense'] == 'p':
                        if not criteria['Prep Time']:
                            criteria['Prep Time'] = ''
                    if criteria['Prep Time'] == 't':
                        if not criteria['expense']:
                            criteria['expense'] = ''
                    if not criteria['expense']:
                        if criteria['Prep Time'] != 't':
                            criteria['expense'] = 'n'
                    if not criteria['Prep Time']:
                        if criteria['expense'] != 'p':
                            criteria['Prep Time'] = 'n'
                    demand = {k: v for k, v in criteria.items() if v}
                    x = len(demand)

                    def checktable():
                        def gen_week():
                            tups = []
                            day = []
                            for k in sorted(day_meals, key=lambda k: len(day_meals[k])):
                                tups.append(day_meals[k])
                                day.append(k)
                            day = [k.lower() for k in day]
                            day = [w.replace('mon', 'Monday') for w in day]
                            day = [w.replace('tue', 'Tuesday') for w in day]
                            day = [w.replace('wed', 'Wednesday') for w in day]
                            day = [w.replace('thu', 'Thursday') for w in day]
                            day = [w.replace('fri', 'Friday') for w in day]
                            day = [w.replace('sat', 'Saturday') for w in day]
                            day = [w.replace('sun', 'Sunday') for w in day]
                            thebig = []
                            for list_meals in tups:
                                for meal in list_meals:
                                    if meal in thebig:
                                        list_meals.remove(meal)
                                thebig.append(random.choice(list_meals))
                                template = dict(zip(day, thebig))

                            def make_dict_full():
                                end_crit_dict = {'Monday': '', 'Tuesday': '', 'Wednesday': '', 'Thursday': '',
                                                     'Friday': '', 'Saturday': '', 'Sunday': ''}
                                for i in template:
                                    if i == 'Monday':
                                        end_crit_dict['Monday'] = template[i]
                                    if i == 'Tuesday':
                                        end_crit_dict['Tuesday'] = template[i]
                                    if i == 'Wednesday':
                                        end_crit_dict['Wednesday'] = template[i]
                                    if i == 'Thursday':
                                        end_crit_dict['Thursday'] = template[i]
                                    if i == 'Friday':
                                        end_crit_dict['Friday'] = template[i]
                                    if i == 'Saturday':
                                        end_crit_dict['Saturday'] = template[i]
                                    if i == 'Sunday':
                                        end_crit_dict['Sunday'] = template[i]
                                pop_results(**end_crit_dict)
                            make_dict_full()

                        potential_meals = []
                        c.execute('select * from Recipe_List_Custom')
                        crit_lit = list(criteria.values())
                        for row in c.fetchall():
                            mapped = zip(row, crit_lit)
                            counter = 0
                            for i in mapped:
                                if i[0] == i[1]:
                                    counter += 1
                            if counter == x:
                                potential_meals.append(row[0])
                        day_meals[days] = potential_meals
                        another_day = input('Do you want to add another day? ''\n').lower()
                        if another_day == 'y':
                            enter_days()
                        if another_day == 'n':
                            gen_week()
                        else:
                            print('Try again! ' '\n')
                            checktable()
                    checktable()
                set_calc(criteria)
            enter_reqs()
        enter_days()
    special_days_input()




LARGE_FONT = ("Verdana", 12)


class MenuQ(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        master = tk.Frame(self)
        master.pack(side="top", fill="both", expand=True)
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, RecipeBookStartPage, FullList, CustomSearch, AddRecipe, DeleteRecipe,
                  SelectRecipeToChange, AddColumn, CustomSearchResults, ChangeRecipe, UpdateWNewAttribute, MealPlanner,
                  RandomPlanner, CustomPlanner, CustomPlannerResults):
            frame = F(master, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text="Recipe Book", command = lambda: controller.show_frame(RecipeBookStartPage))
        button1.pack()
        button2 = tk.Button(self, text="Meal Planner", command = lambda: controller.show_frame(MealPlanner))
        button2.pack()


class RecipeBookStartPage (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        button1 = tk.Button(self, text="See all recipes", command =lambda: controller.show_frame(FullList))
        button1.pack()
        button2 = tk.Button(self, text="Custom Search", command=lambda: controller.show_frame(CustomSearch))
        button2.pack()
        button3 = tk.Button(self, text="Add a new recipe", command=lambda: controller.show_frame(AddRecipe))
        button3.pack()
        button4 = tk.Button(self, text="Delete a recipe", command=lambda: controller.show_frame(DeleteRecipe))
        button4.pack()
        button5 = tk.Button(self, text="Change a recipe", command=lambda: controller.show_frame(SelectRecipeToChange))
        button5.pack()
        button6 = tk.Button(self, text="Add your own search attribute", command=lambda:
                            controller.show_frame(AddColumn))
        button6.pack()


class FullList (tk.Frame):
    def tryit(self):
        view_all_recipes()


    # def __init__(self, parent, controller):
        view_all_recipes()

        # tk.Frame.__init__(self, parent)
        # variable=StringVar()
        # variable = view_all_recipes
        # label = tk.Label(self, text=line, font=LARGE_FONT, textvariable = variable)
        # label.pack(pady=10, padx=10)
        # button1 = tk.Button(self, text="Back to homepage", command=lambda: controller.show_frame(StartPage))
        # button1.pack()


class CustomSearch (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # DROP DOWN MENU OF ATTRIBUTES
        button1 = tk.Button(self, text="See Results", command=lambda: controller.show_frame(CustomSearchResults))
        button1.pack()


class CustomSearchResults (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # DISPLAY RESULTS
        button1 = tk.Button(self, text="Back to homepage", command=lambda: controller.show_frame(StartPage))
        button1.pack()


class AddRecipe (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # BOXES TO FILL IN RECIPE
        # button1 = tk.Button(self, text="Send to recipe book", command=execute)
        # button1.pack()
        button2 = tk.Button(self, text="Back to homepage", command=lambda: controller.show_frame(StartPage))
        button2.pack()


class DeleteRecipe(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # DROP DOWN LIST OF RECIPES, PICK ONE TO DELETE
        # button1 = tk.Button(self, text="Delete", command=execute)
        # button1.pack()
        button2 = tk.Button(self, text="Back to homepage", command=lambda: controller.show_frame(StartPage))
        button2.pack()


class SelectRecipeToChange(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # DROP DOWN LIST OF RECIPES, PICK ONE TO CHANGE
        # button1 = tk.Button(self, text="Change this recipe", command=execute)
        # button1.pack()
        button2 = tk.Button(self, text="Back to homepage", command=lambda: controller.show_frame(StartPage))
        button2.pack()


class ChangeRecipe(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # DROP DOWN LIST OF CRITERIA
        # button1 = tk.Button(self, text="Make the changes", command=execute)
        # button1.pack()
        button2 = tk.Button(self, text="Back to homepage", command=lambda: controller.show_frame(StartPage))
        button2.pack()


class AddColumn(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # TEXT BOX TO ADD NEW ATTRIBUTE
        # button1 = tk.Button(self, text="Click to add", command=execute)
        # button1.pack()
        button2 = tk.Button(self, text="Update the recipes", command=lambda: controller.show_frame(UpdateWNewAttribute))
        button2.pack()


class UpdateWNewAttribute(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # TEXT BOX TO ADD NEW VALUES
        # button1 = tk.Button(self, text="Click to update", command=execute)
        button2 = tk.Button(self, text="Back to homepage", command=lambda: controller.show_frame(StartPage))
        button2.pack()


class MealPlanner (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text="Random Planner", command=lambda: controller.show_frame(RandomPlanner))
        button1.pack()
        button2 = tk.Button(self, text="Custom Planner", command=lambda: controller.show_frame(CustomPlanner))
        button2.pack()


class RandomPlanner (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # DISPLAY PLAN
        # button1 = tk.Button(self, text="Search again", command=execute function))
        # button1.pack()
        button2 = tk.Button(self, text="Back to homepage", command=lambda: controller.show_frame(StartPage))
        button2.pack()


class CustomPlanner (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # DISPLAY DAYS AND ATTRIBUTES
        button1 = tk.Button(self, text="Send", command=lambda: controller.show_frame(CustomPlannerResults))
        button1.pack()


class CustomPlannerResults (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # DISPLAY RESULTS
        button1 = tk.Button(self, text="Try again", command=lambda: controller.show_frame(CustomPlannerResults))
        button1.pack()
        button2 = tk.Button(self, text="Back to homepage", command=lambda: controller.show_frame(StartPage))
        button2.pack()


app = MenuQ()
app.mainloop()

c.close()
conn.close()

