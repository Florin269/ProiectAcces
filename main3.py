import os
import mysql.connector
import shutil
import time
import csv
import re
from const import *
from dateutil import parser
from datetime  import datetime



class MySqlConnection:
    def __init__(self):
        self.mydb = mysql.connector.connect(host ='localhost', user='root', password = password, database ='cladire')
        self.cursor =self.mydb.cursor()

    def selecteaza_din_baza_de_date(self,query):
        self.cursor.execute(query,multi=True)
        rezultat = self.cursor.fetchall()
        return rezultat

mysqlcon=MySqlConnection()



class Monitorizare():
    def __init__(self):
        self.date_acces={}
        
    def salveaza_in_fisier_csv(self):
        with open(folder_intrari + '/' + self.numepoarta, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Data si Ora', 'Sens'])

            for id_persoana, records in self.date_acces.items():
                for record in records:
                    writer.writerow(record)

    def extragere_date(self):
        data_curenta = datetime.now().strftime('%Y-%m-%d')
        inceput_zi = datetime.strptime(f'{data_curenta} 00:00:00', '%Y-%m-%d %H:%M:%S')
        sfarsit_zi = datetime.strptime(f'{data_curenta} 23:59:59', '%Y-%m-%d %H:%M:%S')
        query = f"SELECT persoane.Nume, SUM(CASE WHEN AC.Sens = 'out' THEN 1 WHEN AC.Sens = 'in' THEN  -1 END * HOUR(AC.Data)) as OreLucrate FROM `cladire`.`acces` AC JOIN persoane ON AC.ID_Persoana = persoane.ID  WHERE AC.Data BETWEEN '{inceput_zi}' AND '{sfarsit_zi}' GROUP BY persoane.Nume; '"
        rezultate = mysqlcon.selecteaza_din_baza_de_date(query)
        rezultat = rezultate.fetchall()
        print(rezultat)
    



    
    def calculeaza_ore(self):
        ore_lucrate=[]
        for rezultat in rezultate:
            angajat_id,intrare,iesire = rezultat
            durata = iesire - intrare
            ore = durata.total_seconds() / 3600 

            if angajat_id not in ore_lucrate:
                ore_lucrate[angajat_id]=0 
            ore_lucrate[angajat_id] += ore


monitor = Monitorizare()
extragere=monitor.extragere_date()
print(extragere)

