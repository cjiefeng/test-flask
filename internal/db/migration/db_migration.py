import os

from internal.db import db


def init_db():
    path = './internal/db/migration/sql'
    database = db.get_db(multi=True)
    files = [f for f in os.listdir(path) if _filter_sql_file(path, f)]
    sorted_files = sorted(files)
    for f in sorted_files:
        sql = open(os.path.join(path, f), "r").read()
        print(sql)
        rows_affected = database.execute_multi(sql)
        database.commit()  # commit after every file
        output_list = list(map(lambda x: str(x) + ' row(s) affected.', rows_affected))  # format output
        for output in output_list:
            print(output)


def _filter_sql_file(path, f):
    return os.path.isfile(os.path.join(path, f)) and f.endswith('.sql')
