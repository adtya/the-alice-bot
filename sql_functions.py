import sqlite3

def create_table(db_name, table_name, sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        sql_exec = "select name from sqlite_master where name=\'"+table_name+"\'"
        cursor.execute(sql_exec)
        result = cursor.fetchall()
        if len(result) == 0:
            cursor.execute(sql)
            print("Table "+ table_name +" created.")
            db.commit();
        else:
            print("Using existing table", table_name)

def check_user(db_name, table_name, user_id):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("select ID from \'"+table_name+"\' where ID="+str(user_id))
        result = cursor.fetchall()
        if len(result) == 1:
            return True
        else:
            return False

def add_user(db_name, table_name, user_id, user_name):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        sql_exec = "insert into "+table_name+"(ID,Name)"+"\nvalues("+str(user_id)+",\'"+user_name+"\')"
        cursor.execute(sql_exec)
        print(user_name,"added\n")

def add_admin(db_name, table_name, user_id):
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
