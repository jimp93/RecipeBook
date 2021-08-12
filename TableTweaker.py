import sqlite3
import shelve

s = shelve.open('test_shelf.db')
del s['default_holder']
s = shelve.open('test_shelf.db')
del s['title_holder']
s = shelve.open('test_shelf.db')
del s['key1']
# default_dict = {'MainIngredient': {'Any': 1}, 'onions': {'Any': 1}}
# s = shelve.open('test_shelf.db')
# s['default_holder'] = default_dict
# #
# # conn = sqlite3.connect('master.db')
# # c = conn.cursor()
# # c.execute("""DROP TABLE RecipeListOptions""")
# # conn.commit()
# # conn.close()
# #
#
conn = sqlite3.connect('master.db')
c = conn.cursor()
c.execute("""DROP TABLE RecipeList""")
conn.commit()
conn.close()

# conn = sqlite3.connect('master.db')
# c = conn.cursor()
# c.execute("""DROP TABLE RecipeListDefault""")
# conn.commit()
# conn.close()
#
# conn = sqlite3.connect('master.db')
# c = conn.cursor()
# c.execute("""DROP TABLE RecipeListTitleHolder""")
# conn.commit()
# conn.close()

# conn = sqlite3.connect('master.db')
# c = conn.cursor()
# c.execute("""DROP TABLE rl_backup""")
# conn.commit()
# conn.close()
#
# conn = sqlite3.connect('master.db')
# c = conn.cursor()
# c.execute("""DROP TABLE rlt_backup""")
# conn.commit()
# conn.close()
#
# conn = sqlite3.connect('master.db')
# c = conn.cursor()
# c.execute("""DROP TABLE rld_backup""")
# conn.commit()
# conn.close()
#
# conn = sqlite3.connect('master.db')
# c = conn.cursor()
# c.execute("""DROP TABLE rlo_backup""")
# conn.commit()
# conn.close()

#
# # c.execute("""INSERT INTO  - VALUES()""")
# # conn.commit()
# #
#
# # c.execute("""CREATE TABLE Recipe_List_Custom (
# #     meal text,
# #     MainIngredient text,
# #     freezability text,
# #     expense text,
# #     PrepTime text
#     )""")


# START OF DELETE COLUMN LOOP

# def delete_temp():
#     conn = sqlite3.connect('testpad.db')
#     c = conn.cursor()
#     c.execute("""DROP TABLE IF EXISTS tester_backup""")
#     conn.commit()
#     c.close()
#     conn.close()
#     delete_starter()
#
# def delete_starter():
#     def create_temp():
#         print(3)
#         c.execute("""BEGIN TRANSACTION""")
#         c.execute("""CREATE TABLE tester_backup (meal)""")
#         conn.commit()
#         c.close()
#         conn.close()
#         columns_to_stay(names)
#     conn = sqlite3.connect('testpad.db')
#     c = conn.cursor()
#     cursor = conn.execute('select * FROM Recipe_Tester')
#     names = list(map(lambda x: x[0], cursor.description))
#     create_temp()
#
#
# def columns_to_stay(names):
#     conn = sqlite3.connect('testpad.db')
#     c = conn.cursor()
#     column_to_remove = input('Which attribute needs removing?' '\n')
#     columns_to_stay = [x for x in names if x not in column_to_remove]
#     columns_to_stay.pop(0)
#     c.close()
#     conn.close()
#     create_columns_in_temp(columns_to_stay)
#
#
# def create_columns_in_temp(columns_to_stay):
#     conn = sqlite3.connect('testpad.db')
#     c = conn.cursor()
#     for column in columns_to_stay:
#         c.execute("""alter table tester_backup add """"" + column + """""")
#         conn.commit()
#     c.close()
#     conn.close()
#     insert_data_into_temp()
#
#
# def insert_data_into_temp():
#     conn = sqlite3.connect('testpad.db')
#     c = conn.cursor()
#     cursor = conn.execute('select * FROM tester_backup')
#     inames = list(map(lambda x: x[0], cursor.description))
#     inames.pop(0)
#     c.execute("""INSERT INTO tester_backup (meal) SELECT meal FROM Recipe_Tester""")
#     conn.commit()
#     c.execute("""Select meal FROM tester_backup""")
#     meals_moved = c.fetchall()
#     list_meals_moved = [i[0] for i in meals_moved]
#     for meal in list_meals_moved:
#         for column in inames:
#             c.execute("""UPDATE tester_backup SET (""" + column + """)
#             = (SELECT """ + column + """ FROM Recipe_Tester WHERE meal =(?)) WHERE meal == (?)""", (meal, meal))
#             conn.commit()
#     c.close()
#     conn.close()
#     delete_original()
#
#
# def delete_original():
#     conn = sqlite3.connect('testpad.db')
#     c = conn.cursor()
#     c.execute("""DROP TABLE Recipe_Tester""")
#     conn.commit()
#     c.close()
#     conn.close()
#     create_new_original()
#
#
# def create_new_original():
#     conn = sqlite3.connect('testpad.db')
#     c = conn.cursor()
#     c.execute("""BEGIN TRANSACTION""")
#     c.execute("""CREATE TABLE Recipe_Tester (meal)""")
#     conn.commit()
#     c.close()
#     conn.close()
#     add_rest_of_columns()
#
#
# def add_rest_of_columns():
#     print(4)
#     conn = sqlite3.connect('testpad.db')
#     cursor = conn.execute('select * FROM tester_backup')
#     binames = list(map(lambda x: x[0], cursor.description))
#     binames.pop(0)
#     c = conn.cursor()
#     for column in binames:
#         c.execute("""alter table Recipe_Tester add """"" + column + """""")
#         conn.commit()
#     c.close()
#     conn.close()
#     populate_new_original()
#
#
# def populate_new_original():
#     conn = sqlite3.connect('testpad.db')
#     c = conn.cursor()
#     c.execute("""INSERT INTO Recipe_Tester SELECT * FROM tester_backup""")
#     conn.commit()
#     c.close()
#     conn.close()
#     delete_temp_again()
#
#
# def delete_temp_again():
#     conn = sqlite3.connect('testpad.db')
#     c = conn.cursor()
#     c.execute("""DROP TABLE tester_backup""")
#     conn.commit()
#     conn.close()
#
# delete_temp()

# END OF LOOP

    #     copy_data_to_new_original()
    # create_new_original()
#
#             insert_data_into_temp()
#         create_columns_in_temp()
#     columns_to_stay()
# list_of_columns()


# cursor.close()
# conn.close()
