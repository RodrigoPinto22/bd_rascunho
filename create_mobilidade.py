import sqlite3
import random

A=["carro","pé","autocarro","comboio","bicicleta"]
num_entries = 1000

#Conectar à BD

conn = sqlite3.connect("Recintos.db")
cursor =conn.cursor()

#Criar uma tabela

cursor.execute('''
CREATE TABLE IF NOT EXISTS mobilidade (
        cidadao INT,
        tempo TEXT,
        transporte TEXT,
        foreign key (cidadao) references cidadao(id)) ''')

#Commit - garante que a tabela seja criada

conn.commit()

#Inserir dados na tabela

for cid in range(num_entries):

    #Escolhe de forma aleatória quantos transportes vai usar
    num_transportes = random.randint(1,5)

    for _ in range(num_transportes):

        tempo = random.randint(1,60)
        transporte = random.choice(A)

        cursor.execute('''
            Insert into mobilidade (cidadao,tempo,transporte)
            Values (?,?,?)
        ''', (cid,tempo,transporte))

conn.commit()
conn.close()