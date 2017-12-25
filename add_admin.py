import sqlite3
import sql_functions

db_name = "alice.db"
table_name = "Admins"
sql_admins = """create table Admins(
        ID integer,
        primary key(ID))"""

sql_functions.create_table(db_name, table_name, sql_admins)
user_id = int(input("Enter the ID: "))

with sqlite3.connect(db_name) as db:
    cursor = db.cursor()
    sql_exec = "select ID from "+table_name+" where ID="+str(user_id)
    cursor.execute(sql_exec)
    result = cursor.fetchall()
    if len(result) == 0:
        sql_exec = "insert into "+table_name+"(ID)"+"\nvalues("+str(user_id)+")"
        cursor.execute(sql_exec)
        print(user_id,"added\n")
    else:
        print("User is already an Admin.\n")
