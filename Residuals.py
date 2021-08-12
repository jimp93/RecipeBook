# for k in self.ado_del_dict:
#     to_del = self.ado_del_dict[k]
#     del_from_list = existing[k]
#     del_from_list.remove(to_del)
#     existing[k] = del_from_list
# s = shelve.open('test_shelf.db')
# dog = s['key1']
# print(dog)

# def make_it_work(self, controller):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     for k in self.ado_del_dict:
#         value = self.ado_del_dict[k]
#         c.execute("SELECT " + k + " FROM RecipeList")
#         if_exists = c.fetchall()
#         ex_if_exists = [a for b in if_exists for a in b]
#         set_ex_if_exists = set(ex_if_exists)
#         if self.ado_del_dict[k] in set_ex_if_exists:
#             for widget in self.ado_list_of_widgets:
#                 widget.destroy()
#             for widget in self.ado_list_of_widgets1:
#                 widget.destroy()
#             self.ado_lbel_wrong = tk.Label(self.frame,
#                                 text="You are using that value, change recipes and try again", font=LARGE_FONT)
#             self.ado_lbel_wrong.pack()
#             ado_button_5 = tk.Button(self, text="Back to Homepage",
#                                      command=lambda: self.make_labels_boxes(controller, 1))
#             ado_button_5.pack()
#             self.ado_list_of_widgets1.append(ado_button_5)
#             self.ado_list_of_widgets1.append(self.ado_lbel_wrong)
#         else:
#             c.execute("DELETE FROM RecipeListOptions WHERE " + k + "=(?)", (value,))
#             conn.commit()
#     for ke in self.ado_add_dict:
#         evalue=self.ado_add_dict[ke]
#         c.execute("SELECT " + ke + " FROM RecipeListOptions")
#         if_exists_a = c.fetchall()
#         ex_if_exists_a = [a for b in if_exists_a for a in b]
#         if self.ado_add_dict[ke] in ex_if_exists_a:
#             for widget in self.ado_list_of_widgets:
#                 widget.destroy()
#             for widget in self.ado_list_of_widgets1:
#                 widget.destroy()
#             self.ado_lbel_exist = tk.Label(self.frame,
#                                            text="That option already exist, try again", font=LARGE_FONT)
#             self.ado_lbel_exist.pack()
#             ado_button_6 = tk.Button(self, text="Back to Homepage",
#                                      command=lambda: self.make_labels_boxes(controller, 1))
#             ado_button_6.pack()
#             self.ado_list_of_widgets1.append(ado_button_6)
#             self.ado_list_of_widgets1.append(self.ado_lbel_exist)
#         else:
#             c.execute("INSERT INTO RecipeListOptions (" + ke + ") VALUES (?)", (evalue,))
#             conn.commit()
#     conn.close()
#     for widget in self.ado_list_of_widgets:
#         widget.destroy()
#     ado_button_3 = tk.Button(self, text="Make another change",
#                              command=lambda: self.make_labels_boxes(controller, 0))
#     ado_button_3.pack()
#     ado_button_4 = tk.Button(self, text="Back to Homepage", command=lambda: self.make_labels_boxes(controller, 1))
#     ado_button_4.pack()
#     self.ado_list_of_widgets1.append(ado_button_3)
#     self.ado_list_of_widgets1.append(ado_button_4)


# def make_it_work(self, controller):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     for k in self.ado_del_dict:
#         value = self.ado_del_dict[k]
#         c.execute("SELECT " + k + " FROM RecipeList")
#         if_exists = c.fetchall()
#         ex_if_exists = [a for b in if_exists for a in b]
#         set_ex_if_exists = set(ex_if_exists)
#         if self.ado_del_dict[k] in set_ex_if_exists:
#             for widget in self.ado_list_of_widgets:
#                 widget.destroy()
#             for widget in self.ado_list_of_widgets1:
#                 widget.destroy()
#             self.ado_lbel_wrong = tk.Label(self.frame,
#                                 text="You are using that value, change recipes and try again", font=LARGE_FONT)
#             self.ado_lbel_wrong.pack()
#             ado_button_5 = tk.Button(self, text="Back to Homepage",
#                                      command=lambda: self.make_labels_boxes(controller, 1))
#             ado_button_5.pack()
#             self.ado_list_of_widgets1.append(ado_button_5)
#             self.ado_list_of_widgets1.append(self.ado_lbel_wrong)
#         else:
#             c.execute("DELETE FROM RecipeListOptions WHERE " + k + "=(?)", (value,))
#             conn.commit()

#     for ke in self.ado_add_dict:
#         evalue=self.ado_add_dict[ke]
#         c.execute("SELECT " + ke + " FROM RecipeListOptions")
#         if_exists_a = c.fetchall()
#         ex_if_exists_a = [a for b in if_exists_a for a in b]
#         if self.ado_add_dict[ke] in ex_if_exists_a:
#             for widget in self.ado_list_of_widgets:
#                 widget.destroy()
#             for widget in self.ado_list_of_widgets1:
#                 widget.destroy()
#             self.ado_lbel_exist = tk.Label(self.frame,
#                                            text="That option already exist, try again", font=LARGE_FONT)
#             self.ado_lbel_exist.pack()
#             ado_button_6 = tk.Button(self, text="Back to Homepage",
#                                      command=lambda: self.make_labels_boxes(controller, 1))
#             ado_button_6.pack()
#             self.ado_list_of_widgets1.append(ado_button_6)
#             self.ado_list_of_widgets1.append(self.ado_lbel_exist)
#         else:
#             c.execute("INSERT INTO RecipeListOptions (" + ke + ") VALUES (?)", (evalue,))
#             conn.commit()
#     conn.close()
#     for widget in self.ado_list_of_widgets:
#         widget.destroy()
#     ado_button_3 = tk.Button(self, text="Make another change",
#                              command=lambda: self.make_labels_boxes(controller, 0))
#     ado_button_3.pack()
#     ado_button_4 = tk.Button(self, text="Back to Homepage", command=lambda: self.make_labels_boxes(controller, 1))
#     ado_button_4.pack()
#     self.ado_list_of_widgets1.append(ado_button_3)
#     self.ado_list_of_widgets1.append(ado_button_4)


# c.execute("""CREATE TABLE IF NOT EXISTS RecipeListTitleHolder (
#     meal text,
#     MainIngredient text,
#     expense text,
#     PrepTime text
#     )""")
# conn.commit()

# c.execute("""SELECT meal FROM RecipeListTitleHolder""")
# start_up_checker = c.fetchall()
#
# if len(start_up_checker) == 0:
#     print('nope')
#     c.execute("""INSERT INTO RecipeListTitleHolder VALUES  (?, ?, ?, ?
#         )""", ("Meal", "Main Ingredient", "Expense", "Prep Time"))
#     conn.commit()
#

# c.execute("""CREATE TABLE IF NOT EXISTS RecipeListDefault (
#     meal text,
#     MainIngredient text,
#     expense text,
#     PrepTime text
#     )""")
# conn.commit()
#
# c.execute("""SELECT meal FROM RecipeListDefault""")
# start_up_checker1 = c.fetchall()
#
# if len(start_up_checker1) == 0:
#     c.execute("""INSERT INTO RecipeListDefault VALUES  (?, ?, ?, ?)""", ("Meal", "any", "any", "any"))
#     conn.commit()
#
# c.execute("""CREATE TABLE IF NOT EXISTS RecipeListOptions (meal text, MainIngredient text,
#         expense text,
#         PrepTime text
#         )""")
# conn.commit()

# c.execute("""SELECT expense FROM RecipeListOptions""")
# start_up_checker_opt = c.fetchall()
#
# if len(start_up_checker_opt) == 0:
#     def data_entry_m():
#         c.execute("INSERT INTO RecipeListOptions(meal) VALUES(?)", ('Empty',))
#         conn.commit()
#         data_entry_mi()
#     def data_entry_mi():
#         mi_list = ["veg", "pasta", "chicken", "beef", "pork", "lamb"]
#         for item in mi_list:
#             c.execute("INSERT INTO RecipeListOptions(MainIngredient) VALUES(?)", (item,))
#             conn.commit()
#         data_entry_e()
#     def data_entry_e():
#         e_list = ["cheap", "normal", "expensive"]
#         for item in e_list:
#             c.execute("INSERT INTO RecipeListOptions(expense) VALUES(?)", (item,))
#             conn.commit()
#         data_entry_pt()
#     def data_entry_pt():
#         pt_list = ["quick", "normal", "long time"]
#         for item in pt_list:
#             c.execute("INSERT INTO RecipeListOptions(PrepTime) VALUES(?)", (item,))
#             conn.commit()
#     data_entry_m()

# c.execute("""alter table RecipeListTitleHolder add """"" + not_nice_new_column + """""")
# c.execute("UPDATE RecipeListTitleHolder SET " + not_nice_new_column + " = (?) "
#                                                                    "WHERE meal = Meal", (new_column,))
# c.execute("""alter table RecipeListDefault add """"" + not_nice_new_column + """""")
# c.execute("UPDATE RecipeListDefault SET " + not_nice_new_column + " = 'any'")
#
# c.execute("""alter table RecipeListOptions add """"" + not_nice_new_column + """""")
# for thing in options_menu:
#     c.execute("INSERT INTO RecipeListOptions(" + not_nice_new_column + ") VALUES(?)", (thing,))
#     conn.commit()
# conn.commit()
# conn.close()

# def create_temp_d(self, controller):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     c.execute("""BEGIN TRANSACTION""")
#     c.execute("""CREATE TABLE IF NOT EXISTS rld_backup (meal)""")
#     conn.commit()
#     conn.close()
#     self.create_temp_t(controller)
#
# def create_temp_t(self, controller):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     c.execute("""BEGIN TRANSACTION""")
#     c.execute("""CREATE TABLE IF NOT EXISTS rlt_backup (meal)""")
#     conn.commit()
#     conn.close()
#     self.create_temp_o(controller)
#
# def create_temp_o(self, controller):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     c.execute("""BEGIN TRANSACTION""")
#     c.execute("""CREATE TABLE IF NOT EXISTS rlo_backup (meal)""")
#     conn.commit()
#     conn.close()
#     self.cols_to_stay(controller)

# def create_columns_in_temp_d(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     self.columns_to_stay = [x for x in self.names if x not in self.lbdel_get]
#     for column in self.columns_to_stay:
#         c.execute("""alter table rld_backup add """"" + column + """""")
#         conn.commit()
#     conn.close()
#     self.create_columns_in_temp_t()
#
# def create_columns_in_temp_t(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     self.columns_to_stay = [x for x in self.names if x not in self.lbdel_get]
#     for column in self.columns_to_stay:
#         c.execute("""alter table rlt_backup add """"" + column + """""")
#         conn.commit()
#     conn.close()
#     self.create_columns_in_temp_o()
#
# def create_columns_in_temp_o(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     self.columns_to_stay = [x for x in self.names if x not in self.lbdel_get]
#     for column in self.columns_to_stay:
#         c.execute("""alter table rlo_backup add """"" + column + """""")
#         conn.commit()
#     conn.close()
#     self.insert_data_into_temp()

# def insert_data_into_temp_d(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     ins_cursor = conn.execute('select * FROM rld_backup')
#     inames = list(map(lambda x: x[0], ins_cursor.description))
#     inames.pop(0)
#     c.execute("""INSERT INTO rld_backup (meal) SELECT meal FROM RecipeListDefault""")
#     conn.commit()
#     c.execute("""Select meal FROM rld_backup""")
#     meals_moved = c.fetchall()
#     list_meals_moved = [i[0] for i in meals_moved]
#     for meal in list_meals_moved:
#         for column in inames:
#             c.execute("""UPDATE rld_backup SET (""" + column + """)
#             = (SELECT """ + column + """ FROM RecipeListDefault WHERE meal =(?)) WHERE meal == (?)""", (meal, meal))
#             conn.commit()
#     conn.close()
#     self.insert_data_into_temp_t()
#
# def insert_data_into_temp_t(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     ins_cursor = conn.execute('select * FROM rlt_backup')
#     inames = list(map(lambda x: x[0], ins_cursor.description))
#     inames.pop(0)
#     c.execute("""INSERT INTO rlt_backup (meal) SELECT meal FROM RecipeListTitleHolder""")
#     conn.commit()
#     c.execute("""Select meal FROM rlt_backup""")
#     meals_moved = c.fetchall()
#     list_meals_moved = [i[0] for i in meals_moved]
#     for meal in list_meals_moved:
#         for column in inames:
#             c.execute("""UPDATE rlt_backup SET (""" + column + """)
#             = (SELECT """ + column + """ FROM RecipeListTitleHolder
#              WHERE meal =(?)) WHERE meal == (?)""", (meal, meal))
#             conn.commit()
#     conn.close()
#     self.insert_data_into_temp_o()
#
# def insert_data_into_temp_o(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     ins_cursor = conn.execute('select * FROM rlo_backup')
#     inames = list(map(lambda x: x[0], ins_cursor.description))
#     inames.pop(0)
#     c.execute("INSERT INTO rlo_backup(meal) VALUES(?)", ('Empty',))
#     conn.commit()
#     for column in inames:
#         c.execute("select " + column + " FROM RecipeListOptions")
#         col_contents = c.fetchall()
#         list_col_contents = [i[0] for i in col_contents]
#         set_list = set(list_col_contents)
#         self.options_dict[column] = set_list
#     for k in self.options_dict:
#         vals = self.options_dict[k]
#         self.insert_step(vals, k)
#     conn.close()
#     self.delete_original()

# def insert_step(self, vals, k):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     for item in vals:
#         if item != None:
#             c.execute("INSERT INTO rlo_backup(" + k + ") VALUES(?)", (item,))
#             conn.commit()

# def delete_original_d(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     c.execute("""BEGIN TRANSACTION""")
#     c.execute("""DROP TABLE RecipeListDefault""")
#     conn.commit()
#     conn.close()
#     self.delete_original_t()
#
# def delete_original_t(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     c.execute("""BEGIN TRANSACTION""")
#     c.execute("""DROP TABLE RecipeListTitleHolder""")
#     conn.commit()
#     conn.close()
#     self.delete_original_o()
#
# def delete_original_o(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     c.execute("""BEGIN TRANSACTION""")
#     c.execute("""DROP TABLE RecipeListOptions""")
#     conn.commit()
#     conn.close()
#     self.create_new_original()
#
# def create_new_original_d(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     c.execute("""BEGIN TRANSACTION""")
#     c.execute("""CREATE TABLE RecipeListDefault (meal)""")
#     conn.commit()
#     conn.close()
#     self.create_new_original_t()
#
# def create_new_original_t(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     c.execute("""BEGIN TRANSACTION""")
#     c.execute("""CREATE TABLE RecipeListTitleHolder (meal)""")
#     conn.commit()
#     conn.close()
#     self.create_new_original_o()
#
# def create_new_original_o(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     c.execute("""BEGIN TRANSACTION""")
#     c.execute("""CREATE TABLE RecipeListOptions (meal)""")
#     conn.commit()
#     conn.close()
#     self.add_rest_of_columns()
#
# def add_rest_of_columns_d(self):
#     conn = sqlite3.connect('master.db')
#     add_cursor = conn.execute('select * FROM rld_backup')
#     c = conn.cursor()
#     binames = list(map(lambda x: x[0], add_cursor.description))
#     binames.pop(0)
#     for column in binames:
#         c.execute("""alter table RecipeListDefault add """"" + column + """""")
#         conn.commit()
#     conn.close()
#     self.add_rest_of_columns_t()
#
# def add_rest_of_columns_t(self):
#     conn = sqlite3.connect('master.db')
#     add_cursor = conn.execute('select * FROM rlt_backup')
#     c = conn.cursor()
#     binames = list(map(lambda x: x[0], add_cursor.description))
#     binames.pop(0)
#     for column in binames:
#         c.execute("""alter table RecipeListTitleHolder add """"" + column + """""")
#         conn.commit()
#     conn.close()
#     self.add_rest_of_columns_o()
#
# def add_rest_of_columns_o(self):
#     conn = sqlite3.connect('master.db')
#     add_cursor = conn.execute('select * FROM rlo_backup')
#     c = conn.cursor()
#     binames = list(map(lambda x: x[0], add_cursor.description))
#     binames.pop(0)
#     for column in binames:
#         c.execute("""alter table RecipeListOptions add """"" + column + """""")
#         conn.commit()
#     conn.close()
#     self.populate_new_original()
# def populate_new_original_d(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     c.execute("""BEGIN TRANSACTION""")
#     c.execute("""INSERT INTO RecipeListDefault SELECT * FROM rld_backup""")
#     conn.commit()
#     conn.close()
#     self.populate_new_original_t()
#
# def populate_new_original_t(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     c.execute("""BEGIN TRANSACTION""")
#     c.execute("""INSERT INTO RecipeListTitleHolder SELECT * FROM rlt_backup""")
#     conn.commit()
#     conn.close()
#     self.populate_new_original_o()
#
# def populate_new_original_o(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     insi_cursor = conn.execute('select * FROM rlo_backup')
#     inamesi = list(map(lambda x: x[0], insi_cursor.description))
#     inamesi.pop(0)
#     for col in inamesi:
#         c.execute("INSERT INTO RecipeListOptions (" + col + ") SELECT (" + col + ") FROM rlo_backup")
#         conn.commit()
#     conn.close()
#     self.delete_temp_again()
# def delete_temp_again_d(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     c.execute("""BEGIN TRANSACTION""")
#     c.execute("""DROP TABLE rld_backup""")
#     conn.commit()
#     conn.close()
#     for widget in self.dl_list_of_widgets:
#         widget.destroy()
#     delt_meal_lb = tk.Label(self.frame, text="Column deleted", font=LARGE_FONT)
#     delt_meal_lb.pack()
#     self.delete_temp_again_t()
#
# def delete_temp_again_t(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     c.execute("""BEGIN TRANSACTION""")
#     c.execute("""DROP TABLE rlt_backup""")
#     conn.commit()
#     conn.close()
#     for widget in self.dl_list_of_widgets:
#         widget.destroy()
#     delt_meal_lb = tk.Label(self.frame, text="Column deleted", font=LARGE_FONT)
#     delt_meal_lb.pack()
#     self.delete_temp_again_o()
#
# def delete_temp_again_o(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
#     c.execute("""BEGIN TRANSACTION""")
#     c.execute("""DROP TABLE rlo_backup""")
#     conn.commit()
#     conn.close()
#     for widget in self.dl_list_of_widgets:
#         widget.destroy()
#     delt_meal_lb = tk.Label(self.frame, text="Column deleted", font=LARGE_FONT)
#     delt_meal_lb.pack()

# m_lbel = tk.Label(self.frame, text='Meal', font=LARGE_FONT)
# m_lbel.pack()
# mi_lbel = tk.Label(self.frame, text='Main Ingredient', font=LARGE_FONT)
# mi_lbel.pack()
# e_lbel = tk.Label(self.frame, text='Expense', font=LARGE_FONT)
# e_lbel.pack()
# pt_lbel = tk.Label(self.frame, text='Prep Time', font=LARGE_FONT)
# pt_lbel.pack()
# self.first_meal_var = StringVar()
# self.first_meal_entry = Entry(self.frame, textvariable=self.first_meal_var)
# self.first_meal_entry.pack()
# self.mi_var = StringVar()
# self.mi_var.set("Empty")
# self.mi_box = OptionMenu(self.frame, self.mi_var, "veg", "pasta", "chicken", "beef", "pork", "lamb")
# self.mi_box.pack()
# self.e_var = StringVar()
# self.e_var.set("Empty")
# self.e_box = OptionMenu(self.frame, self.e_var, "cheap", "normal", "expensive")
# self.e_box.pack()
# self.pt_var = StringVar()
# self.pt_var.set("Empty")
# self.pt_box = OptionMenu(self.frame, self.pt_var, "quick", "normal", "long time")
# self.pt_box.pack()

# def rmake_default_dict(self):
#     conn = sqlite3.connect('master.db')
#     c = conn.cursor()
    # cursor = conn.execute('select * FROM RecipeList')
    # rdef_col_names = list(map(lambda x: x[0], cursor.description))
    # rdef_col_names1 = rdef_col_names[1:]
    # c.execute('select * FROM RecipeListDefault')
    # for row in c.fetchall():
    #     rdef_make_row_a_list = list(row)
    #     self.rto_zip = rdef_make_row_a_list[1:]
    # self.rdefault_dict = dict(zip(rdef_col_names1, self.rto_zip))
    # self.rdef_dict = {key:value for (key, value) in self.rdefault_dict.items() if value != 'any'}