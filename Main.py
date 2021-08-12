import sqlite3
import random

conn = sqlite3.connect('master.db')
c = conn.cursor()

# CREATE ORIGINAL


def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS RecipeList (
    meal text,
    MainIngredient text,
    ease text,
    freezability text,
    scalability text
    )""")
    conn.commit()


# RECIPE BOOK

def view_recipes():
    if input('To see the full recipe, type "f"' '\n'
             'To search by attribute, type "a"' '\n').lower() == 'f':
        c.execute("""SELECT meal FROM RecipeList""")
        for row in c.fetchall():
            print(" ".join(map(str, row)))
        opener()
    attribute = input('Which attribute?' '\n'
                      'For main ingredient type "m"' '\n'
                      'For freezability type "f"' '\n'
                      'For expense type "e"' '\n'
                      'For preparation time type "p"' '\n'
                      'For ').lower()
    if attribute == 'm':
        main_choice = input('Which ingredient do you want to search by?' '\n').lower()
        c.execute("""SELECT meal FROM RecipeList WHERE MainIngredient=?""", (main_choice,))
        for row in c.fetchall():
            print(" ".join(map(str, row)))
    if attribute == 'e':
        main_choice = input('Normal cost or push the boat out?' '\n'
                            'For normal type "n"' '\n'
                            'For something fancy type "p"' '\n').lower()
        c.execute("""SELECT meal FROM RecipeList WHERE expense=?""", (main_choice,))
        for row in c.fetchall():
            print(" ".join(map(str, row)))
    if attribute == 'f':
        c.execute("""SELECT meal FROM RecipeList WHERE freezability='y'""")
        for row in c.fetchall():
            print(" ".join(map(str, row)))
    if attribute == 'p':
        main_choice = input('How long to prepare?' '\n'
                            'For quick type "q"' '\n'
                            'For normal type "n"' '\n'
                            'For something time-consuming type "t"' '\n').lower()
        c.execute("""SELECT meal FROM RecipeList WHERE PrepTime=?""", (main_choice,))
        for row in c.fetchall():
            print(" ".join(map(str, row)))
    opener()


def dynamic_data_entry():
    meal = input('Name of the meal''\n').lower()
    main_ingredient = input('What is the main ingredient? ''\n').lower()
    freezability = input('is it freezable?''\n').lower()
    expense = input('How expensive is it? ''\n'
                    '\n'
                    'For normal type "n"' '\n'
                    'For something posh type "p"' '\n').lower()
    preptime = input('How long does it take to prepare? ''\n'
                     '\n'
                     'For quick type "q"' '\n'
                     'For normal type "n"' '\n'
                     'For something time-consuming type "t"' '\n').lower()
    c.execute("""INSERT INTO RecipeList VALUES (?, ?, ?, ?, ?
    )""", (meal, main_ingredient, freezability, expense, preptime))
    conn.commit()
    and_then = input("Do you want to add another recipe?" '\n').lower()
    if and_then == 'y':
        dynamic_data_entry()
    else:
        opener()


def delete_entries():
    if input('To clear the whole book, click "x", to clear one entry, click "d"' '\n').lower() == 'x':
        if input('Are you sure you want to clear the whole book? y/n' '\n').lower() == 'y':
            c.execute("""DELETE FROM RecipeList""")
            conn.commit()
            opener()
        opener()
    meal_to_delete = input('Which meal is getting the chop?' '\n').lower()
    c.execute("DELETE FROM RecipeList WHERE meal =?", (meal_to_delete,))
    conn.commit()
    opener()


def amend_entries():
    def add_it_in():
        c.execute("UPDATE RecipeList SET " + parameter + " = (?) WHERE meal = (?)", (what_to, meal_to_change))
        conn.commit()
    meal_to_change = input('Which meal do you want to change?' '\n').lower()
    attribute = input('To change main ingredient, type "m"' '\n'
                      'To change freezability, type "f"' '\n'
                      'To change expense, type "e"' '\n'
                      'To change p, type "p"' '\n'
                      ).lower()
    what_to = input('What do you want to change it to?' '\n').lower()
    if attribute == 'm':
        parameter = 'MainIngredient'
    if attribute == 'f':
        parameter = 'freezability'
    if attribute == 'e':
        parameter = 'expense'
    if attribute == 'p':
        parameter = 'PrepTime'
    add_it_in()


def recipe_next_move():
    the_next_thing = input('To view recipe book, type "v"' '\n'
            'To add to recipe book, type "a"' '\n' 
            'To delete from recipe book, type "d"' '\n'
            'To tweak a recipe, type "t"' '\n').lower()
    if the_next_thing == 'v':
        view_recipes()
    elif the_next_thing == 'a':
        dynamic_data_entry()
    elif the_next_thing == 'd':
        delete_entries()
    elif the_next_thing == 't':
        amend_entries()
    opener()

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
        c.execute("""SELECT meal FROM RecipeList WHERE expense ='p'""")
        expenser = c.fetchall()
        c.execute("""SELECT meal FROM RecipeList WHERE PrepTime ='t'""")
        prepper = c.fetchall()
        expenser.append(prepper)
        for i in expenser:
            if i not in too_posh:
                too_posh.append(i)
        c.execute("""SELECT meal FROM RecipeList""")
        the_lot = c.fetchall()
        raw_meal_list = [x for x in the_lot if x not in too_posh]
        exploded_raw_meal_list = [i[0] for i in raw_meal_list]
        existing_meals = list(kwargs.values())
        final_meal_list = [x for x in exploded_raw_meal_list if x not in existing_meals]
        c.execute("""SELECT meal FROM RecipeList WHERE MainIngredient IN ('veg', 'pasta', 'fish')""")
        raw_meal_list_veg = c.fetchall()
        exploded_raw_meal_list_veg = [i[0] for i in raw_meal_list_veg]
        final_meal_veg = [x for x in exploded_raw_meal_list_veg if x not in existing_meals]

        def veg_default():
            for k, v in kwargs.items():
                if not v:
                    if k == 'Monday':
                        kwargs['Monday'] = random.choice(final_meal_veg)
                        if kwargs[k] in final_meal_veg:
                            final_meal_veg.remove(kwargs[k])
                            final_meal_list.remove(kwargs[k])
                    if k == 'Tuesday':
                        kwargs['Tuesday'] = random.choice(final_meal_veg)
                        if kwargs[k] in final_meal_veg:
                            final_meal_veg.remove(kwargs[k])
                            final_meal_list.remove(kwargs[k])
                    if k == 'Wednesday':
                        kwargs['Wednesday'] = random.choice(final_meal_veg)
                        if kwargs[k] in final_meal_veg:
                            final_meal_veg.remove(kwargs[k])
                            final_meal_list.remove(kwargs[k])
                    if k == 'Thursday':
                        kwargs['Thursday'] = random.choice(final_meal_veg)
                        if kwargs[k] in final_meal_veg:
                            final_meal_veg.remove(kwargs[k])
                            final_meal_list.remove(kwargs[k])

            def this_is_the_end():
                for k, v in kwargs.items():
                    if not v:
                        kwargs[k] = random.choice(final_meal_list)
                    if kwargs[k] in final_meal_list:
                        final_meal_list.remove(kwargs[k])
                for k, v in kwargs.items():
                    print(k, '--', v, '\n')
                opener()
            this_is_the_end()
        veg_default()
    ta_da_defs()


# INPUT REQUIREMENTS

def opener():
    def pick_or_not():
        results = {'Monday': '', 'Tuesday': '', 'Wednesday': '', 'Thursday': '',
                'Friday': '', 'Saturday': '', 'Sunday': ''}

        def special_days_input():
            criteria = {}
            day_meals = {}
            pick = input("To make a detailed search, type 'd'" '\n'
                         "for random search type 'r' \n").lower()
            if pick == 'r':
                pop_results(**results)

            def enter_days():
                c.execute('select * from RecipeList')
                days = input("Which day requires special instruction" '\n').lower()

                def enter_reqs():
                    dmeal = input("Name of " + days + " meal?" '\n').lower()
                    dmain_ingredient = input("Main Ingredient?" '\n').lower()
                    dfreezable = input("Freezable?"'\n').lower()
                    dexpense = input('Normal cost or push the boat out?' '\n'
                                    'For normal (default) type "n"' '\n'
                                    'For something posh type "p"' '\n').lower()
                    dpreptime = input('How long to prepare?' '\n'
                            'For quick type "q"' '\n'
                            'For normal (default) type "n"' '\n'
                            'For something time-consuming type "t"' '\n').lower()

                    def set_calc(criteria):
                        criteria = {'M': dmeal, 'MI': dmain_ingredient, 'F': dfreezable,
                                    'E': dexpense, 'P': dpreptime}
                        if criteria['E'] == 'p':
                            if not criteria['P']:
                                criteria['P'] = ''
                        if criteria['P'] == 't':
                            if not criteria['E']:
                                criteria['E'] = ''
                        if not criteria['E']:
                            if criteria['P'] != 't':
                                criteria['E'] = 'n'
                        if not criteria['P']:
                            if criteria['E'] != 'p':
                                criteria['P'] = 'n'
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
                            c.execute('select * from RecipeList')

                            for row in c.fetchall():
                                counter = 0
                                if row[0] == criteria['M']:
                                    counter += 1
                                if row[1] == criteria['MI']:
                                    counter += 1
                                if row[2] == criteria['F']:
                                    counter += 1
                                if row[3] == criteria['E']:
                                    counter += 1
                                if row[4] == criteria['P']:
                                    counter += 1
                                if counter == x:
                                    potential_meals.append(row[0])
                                    day_meals[days] = potential_meals
                            if input('Do you want to add another day? ''\n').lower() == 'y':
                                enter_days()
                            else:
                                gen_week()
                        checktable()
                    set_calc(criteria)
                enter_reqs()
            enter_days()
        special_days_input()
    welcome = input('To view or update recipe book, press "r"' '\n' 'to plan your week, press "p"' '\n').lower()
    if welcome == 'r':
        recipe_next_move()
    else:
        pick_or_not()


create_table()
opener()


c.close()
conn.close()









