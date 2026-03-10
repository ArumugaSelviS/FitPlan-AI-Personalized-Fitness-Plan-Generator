import sqlite3
import pandas as pd

conn = sqlite3.connect("fitplan_users.db")

df = pd.read_sql_query("SELECT * FROM users", conn)

conn.close()

df
