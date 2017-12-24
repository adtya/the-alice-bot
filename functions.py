import sqlite3

def create_table(db_name, table_name, sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("select name from sqlite_master where name=?", (table_name,))
        result = cursor.fetchall()
        if len(result) == 0:
            cursor.execute(sql)
            print("Table "+ table_name +" created")
            db.commit();
