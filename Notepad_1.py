import sqlite3
import shelve


start_options_dict = {'MainIngredient': {'beef', 'pork', 'veg', 'pasta', 'lamb', 'chicken'},
                    'expense': {'expensive', 'normal', 'cheap'},
                    'PrepTime': {'normal', 'long time', 'quick'}}

def insert_data_into_temp_o():
    options_dict={}
    def shelver(options_dict):
        s = shelve.open('test_shelf.db')
        s['key1'] = options_dict
        existing = s['key1']
        print(existing)
    conn = sqlite3.connect('master.db')
    c = conn.cursor()
    ins_cursor = conn.execute('select * FROM RecipeListOptions')
    inames = list(map(lambda x: x[0], ins_cursor.description))
    inames.pop(0)
    for column in inames:
        c.execute("select " + column + " FROM RecipeListOptions")
        col_contents = c.fetchall()
        list_col_contents = [i[0] for i in col_contents]
        set_list = set(list_col_contents)
        options_dict[column] = set_list
    conn.close()
    shelver(options_dict)

insert_data_into_temp_o()