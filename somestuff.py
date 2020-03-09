import sqlite3
# from flask import jsonify


conn = sqlite3.connect("otaku.db")

cursor = conn.cursor()


# for i in cursor.execute("SELECT * FROM Posts;"):
#     print(i)
#     list.append(i)

# print(str(list))

def dict_factory(cursor, row):
    d = {}
    for index, col in enumerate(cursor.description):
        d[col[0]] = row[index]

    return d

def top_posts_from_list(someList):
    # conn, cur = Connect_to_db(need_dicts_factory=True)
    conn = sqlite3.connect('otaku.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    top_scoring_posts = cur.execute("SELECT * FROM Posts \
                                     WHERE post_id IN {} \
                                     ORDER BY karma DESC;".format(tuple(someList))).fetchall()
    # Close_db(conn, cur)
    cur.close()
    conn.close()

    return top_scoring_posts



var=top_posts_from_list([1200, 787])

print(var)
