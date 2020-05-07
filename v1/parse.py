#CHANGE TO ONLY GIVE A DICT (UPDATE: THIS IS NOT NEEDED ANYMORE)
def list_dicts_factory(cursor, row):
    list = {}

    d = {}
    for index, col in enumerate(cursor.description):
        d[col[0]] = row[index]

    return list

#USE this only
def dict_factory(cursor, row):
    d = {}
    for index, col in enumerate(cursor.description):
        d[col[0]] = row[index]

    return d