import os
import mysql.connector
import shutil
import time
import csv
import re
from const import *
from dateutil import parser
import datetime


class Monitorizare():
    def __init__(self,nume_poarta):
        self.date_acces=[]
        self.numepoarta =nume_poarta
        


    def valideaza_acces(self,id_persoana,sens):
        data_ora_acces =  datetime.datetime.now()
        if id_persoana not in self.date_acces:
            self.date_acces[id_persoana] = []
            self.date_acces[id_persoana].append({'data_ora': data_ora_acces,
                                                 'sens':sens})
            

    def salveaza_in_csv(self):
        try:
            with open(os.path.join(folder_intrari,self.numepoarta)) as file:
                scriere_csv = csv.writer(file)
                for id_persoana, date in self.date_acces.items():
                    for acces in date:
                        linie = [id_persoana, acces['data_ora'], acces['sens']]
                        scriere_csv(linie)
            print(f'Datele au fost salvate in fisierul CSV: {folder_intrari}')

        except Exception as e:
            print(f"Eroare la salvarea in fisierul CSV: {e}")

            
monitor=Monitorizare(nume_poarta='Poarta1.csv')
monitor.valideaza_acces(1,'intrare')
monitor.salveaza_in_csv()


class MySqlConnection:
    def __init__(self):
        self.mydb = mysql.connector.connect(host ='localhost', user='root', password = password, database ='curs29')
        self.cursor =self.mydb.cursor()

    def adauga_in_baza_de_date(self,query):
        self.cursor.execute(query)
        self.mydb.commit()


def determina_tip_fisier(fisier):
    extensie = fisier.split('.')[-1].lower()

    if extensie == 'csv':
        return 'csv'
    elif extensie == 'txt':
        return 'txt'
    else:
        return None
    

def formatare_data(data_originala):
    data_obj = parser.parse(data_originala)
    data_formatata = data_obj.strftime('%Y-%m-%d %H:%M:%S')
    return data_formatata


def move_file(fisier):
    try:
        fisiere = [f for f in os.listdir(folder_intrari) if os.path.isfile(os.path.join(folder_intrari, f))]
        for fisier in fisiere:
            cale_intrare = os.path.join(folder_intrari,fisier)
            cale_iesire = os.path.join(folder_backup_intrari)
            shutil.move(cale_intrare,cale_iesire)
            print(f"Fisierul'{cale_intrare} a fost mutat la {cale_iesire}")

    except Exception as e: 
        print(f"Eroare la mutarea tuturor fisierlor din folder: {e}")




def extrage_id(nume_fisier):
    return nume_fisier[6]


class citesteFisiere:
    def __init__(self):
        pass


    def citeste_csv(self,fisier):
        try:
            with open(os.path.join(folder_intrari,fisier), 'r') as file:
                    cititor_csv = csv.reader(file)
                    next(cititor_csv)
                    continut =[linie for linie in cititor_csv]
                    return continut
        except Exception as e:
            print(f'Eroare la citirea fisierului CSV : {e}')
            return None
    

    def citeste_txt(self, fisier):
        try:
            with open(os.path.join(folder_intrari,fisier), 'r') as file:
                cititor_txt = file.readlines()
                continut = [linie.strip().split(',') for linie in cititor_txt]
                return continut
        except Exception as e:
            print(f'Eroare la citirea fisierul text: {e}')
            return None
            




mysqlcon=MySqlConnection()
citestefisier = citesteFisiere()

    
def verifica_fisiere(folder_intrari):
    if not os.path.exists(folder_intrari):
        print(f'Folderul {folder_intrari} nu exista')
        return 
    
    files =[ f for f in os.listdir(folder_intrari) if os.path.isfile(os.path.join(folder_intrari,f))]
    if not files:
        print(f'Nu exista fisiere in folderul {folder_intrari}')
    else:
        for file in files:
            if determina_tip_fisier(file) =='csv':
                for line in citestefisier.citeste_csv(file):
                        query=f"INSERT INTO `cladire`.`acces`VALUES(null,'{line[0]}','{formatare_data(line[1])}','{line[2]}','{extrage_id(file)}');"
                        mysqlcon.adauga_in_baza_de_date(query)
                        print('A fost adaugat in SQL')
                        move_file(file)
            elif determina_tip_fisier(file) == 'txt':
                for line in citestefisier.citeste_txt(file):
                        query=f"INSERT INTO `cladire`.`acces`VALUES(null,'{line[0]}','{formatare_data(line[1])}','{line[2]}','{extrage_id(file)}');"
                        mysqlcon.adauga_in_baza_de_date(query)
                        print('A fost adaugat in SQL')
                        move_file(file)
            else:
                print('Introduceti un document de tipul CSV sau TEXT')


            
                    
                    

# while True:
#     verifica_fisiere(folder_intrari)
#     time.sleep(5)