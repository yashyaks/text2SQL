import sqlite3
import pandas as pd

## Connectt to SQlite
connection=sqlite3.connect("data/llmdb")

## Create cursor object to do CRUD
cursor=connection.cursor()
data=cursor.execute('''Select * from llmdata limit 10''')
for row in data:
    print(row)