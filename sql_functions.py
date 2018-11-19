import sqlite3


def create_table(db_name, table_name, sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        sql_exec = "select name from sqlite_master where name=\'"+table_name+"\'"
        cursor.execute(sql_exec)
        result = cursor.fetchall()
        if len(result) == 0:
            cursor.execute(sql)
            print("Table " + table_name + " created.")
            db.commit()
        else:
            print("Using existing table", table_name)


def check_user(db_name, table_name, user_id):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("select ID from \'"+table_name +
                       "\' where ID="+str(user_id))
        result = cursor.fetchall()
        if len(result) == 1:
            return True
        else:
            return False


def add_user(db_name, table_name, user_id, user_name, user_class):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        sql_exec = "insert into "+table_name + \
            "(ID,Name,Class)"+"\nvalues("+str(user_id) + \
            ",\'"+user_name+"\',\'"+user_class+"\')"
        cursor.execute(sql_exec)
        print(user_name, "added\n")


def add_admin(db_name, table_name, user_id):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        sql_exec = "select ID from "+table_name+" where ID="+str(user_id)
        cursor.execute(sql_exec)
        result = cursor.fetchall()
        if len(result) == 0:
            sql_exec = "insert into "+table_name + \
                "(ID)"+"\nvalues("+str(user_id)+")"
            cursor.execute(sql_exec)
            print(user_id, "added\n")
        else:
            print("User is already an Admin.\n")

def addReminder(db_name, reminder):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        sql_exec = "insert into Reminders(ID, title, description, date)"+"\nvalues(\'" + \
            reminder['ID']+"\',\'"+reminder['Title']+"\',\'" + \
            reminder['Description']+"\',\'"+reminder['DueDate']+"\')"
        cursor.execute(sql_exec)

def getReminded(db_name, reminder):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        sql_exec = "select ID from Reminders where DueDate >= DATE(NOW())"
        cursor.execute(sql_exec)
        result = cursor.fetchall()
        return result[0]

def add_docs(db_name, docs):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        sql_exec = "insert into Docs(ID, Subject, Module, Department)"+"\nvalues(\'" + \
            docs['id']+"\',\'"+docs['subject']+"\',\'" + \
            str(docs['module'])+"\',\'"+docs['dept']+"\')"
        cursor.execute(sql_exec)


def get_docs(db_name, docs):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        sql_exec = "select ID from Docs where Subject=\'" + \
            docs['subject']+"\' AND Module=" + \
            str(docs['module'])+" AND Department=\'"+docs['dept']+"\'"
        cursor.execute(sql_exec)
        result = cursor.fetchall()
        return result[0]

def add_feedback(db_name, table_name, name, text):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        sql_exec = "insert into "+table_name + \
            "(name, content)"+"\nvalues(\'"+name+"\',\'"+text+"\')"
        cursor.execute(sql_exec)
        print("feedback recorded")


def read_feedback(db_name, table_name):
    try:
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            sql_exec = "select ID from \'"+table_name+"\'"
            cursor.execute(sql_exec)
            result = cursor.fetchall()
            return result[0]
    except Exception as e:
        return False


def feedback_fetch(db_name, table_name, entry):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        sql_exec = "select content from \'"+table_name+" where ID="+str(entry)
        cursor.execute(sql_exec)
        result = cursor.fetchall()[0][0]
        return result

def reminder_fetch(db_name, table_name, entry):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        sql_exec = "select Description from \'" +table_name+" where ID="+str(entry)
        cursor.execute(sql_exec)
        result = cursor.fetchall()[0][0]
        return result
