from . import db


def add_item(item, quantity):
    database = db.get_db()
    sql = "insert into item_tab (item, quantity) values (%s, %s)"
    return database.insert(sql, (item, quantity))


def get_all_items():
    database = db.get_db()
    sql = "select * from item_tab"
    return database.select_more(sql)
