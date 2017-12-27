import sqlite3
import sql_functions

db_name = "alice.db"
table_name = "Admins"

sql_functions.create_table(db_name, table_name, sql_admins)
user_id = int(input("Enter the ID: "))
