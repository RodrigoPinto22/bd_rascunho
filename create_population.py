import sqlite3
from faker import Faker
from datetime import datetime
import random

fake = Faker(["pt_PT"])
num_entries = 100
min_birthdate = datetime(1930, 1, 1)

conn = sqlite3.connect("Recintos.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cidadao (
        id INTEGER PRIMARY KEY ,
        nome TEXT,
        data_nascimento DATE,
        sexo varchar(1)
    )
''')

conn.commit()

for _ in range(100):
    id = random.randint(10000000, 99999999)
    name = fake.simple_profile()["name"]
    address = fake.simple_profile()["address"]
    birthdate = fake.simple_profile()["birthdate"]
    sex = fake.simple_profile()["sex"]

    formatted_birthdate = birthdate.strftime("%Y-%m-%d")

    # Inserir dados na tabela
    cursor.execute('''
        INSERT INTO cidadao (id, nome, data_nascimento, sexo)
        VALUES (?, ?, ?, ?)
    ''', (id, name, formatted_birthdate, sex))

conn.commit()

conn.close()
