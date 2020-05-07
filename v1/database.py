import sqlite3
from parse import *

def Connect_to_db(option, need_dicts_factory = False):
    conn = None
    # Which Database to access
    if option == 'Votes':
        conn = sqlite3.connect('vote.db')
    elif option == 'Posts':
        conn = sqlite3.connect('post.db')

    # How to parse the data
    if need_dicts_factory:
        conn.row_factory = dict_factory
    else:
        conn.row_factory = list_dicts_factory

    cur = conn.cursor()    

    return conn, cur

def Close_db(conn, cur):
    try: 
        cur.close()
        conn.close()
    except: 
        return False

    return True
