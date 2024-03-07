import os
import mysql.connector
import shutil
import time
import csv
import re
from const import *
from dateutil import parser
from datetime  import datetime
import os.path


#Functie de conectare la baza de date.

class MySqlConnection:
    def __init__(self):
        self.mydb = mysql.connector.connect(host ='localhost', user='root', password = password, database = bazadate)
        self.cursor =self.mydb.cursor()

    def adauga_in_baza_de_date(self,query):
        self.cursor.execute(query)
        self.mydb.commit()

    def selecteaza_din_baza_de_date(self,query):
        self.cursor.execute(query)
        rezultat = self.cursor.fetchall()
        return rezultat

mysqlcon=MySqlConnection()




#Functie redenumire fisier

def redenumeste_fisier(fisier,folder_intrari):
    if os.path.exists(folder_intrari + '/' + fisier):
         data_curenta = datetime.now().strftime("%Y-%m-%d")
         nume_fisier, extensie = os.path.splitext(fisier)
         nume_nou =f'{nume_fisier}{data_curenta}{extensie}'
         cale_noua = os.path.join(folder_intrari, nume_nou)
         cale_veche = os.path.join(folder_intrari, fisier)
         os.rename(cale_veche,cale_noua)

#Functie determina tip fisier ( csv sau txt)
      
def determina_tip_fisier(fisier):
    extensie = fisier.split('.')[-1].lower()

    if extensie == 'csv':
        return 'csv'
    elif extensie == 'txt':
        return 'txt'
    else:
        return None
    
#functie formatare data
    
def formatare_data(data_originala):
    data_obj = parser.parse(data_originala)
    data_formatata = data_obj.strftime('%Y-%m-%d %H:%M:%S')
    return data_formatata

#functie mutare fisier

def move_file(fisier,folder_intrari):
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

#clasa pentru citirea fisierelor

class citesteFisiere:
    def __init__(self):
        pass


    def citeste_csv(self,fisier,folder_intrari):
        try:
            with open(os.path.join(folder_intrari,fisier), 'r') as file:
                    cititor_csv = csv.reader(file)
                    next(cititor_csv)
                    continut =[linie for linie in cititor_csv]
                    return continut
        except Exception as e:
            print(f'Eroare la citirea fisierului CSV : {e}')
            return None
    

    def citeste_txt(self, fisier,folder_intrari):
        try:
            with open(os.path.join(folder_intrari,fisier), 'r') as file:
                cititor_txt = file.readlines()
                continut = [linie.strip().split(',') for linie in cititor_txt]
                return continut
        except Exception as e:
            print(f'Eroare la citirea fisierul text: {e}')
            return None
            



citestefisier = citesteFisiere()


#functie pentru adaugarea si mutarea fisierelor
    
def verifica_fisiere(folder_intrari):
    print('Aplicatia a pornit')
    if not os.path.exists(folder_intrari):
        print(f'Folderul {folder_intrari} nu exista')
        return 
    while True:
            for file in os.listdir(folder_intrari):
                if determina_tip_fisier(file) =='csv':
                    for line in citestefisier.citeste_csv(file,folder_intrari):
                            query=f"INSERT INTO `cladire`.`acces`VALUES(null,'{line[0]}','{formatare_data(line[1])}','{line[2]}','{extrage_id(file)}');"
                            mysqlcon.adauga_in_baza_de_date(query)

                    move_file(redenumeste_fisier(file,folder_intrari),folder_intrari)
                elif determina_tip_fisier(file) == 'txt':
                    for line in citestefisier.citeste_txt(file,folder_intrari):
                            query=f"INSERT INTO `cladire`.`acces`VALUES(null,'{line[0]}','{formatare_data(line[1])}','{line[2].rstrip(';')}','{extrage_id(file)}');"
                            mysqlcon.adauga_in_baza_de_date(query)
                    move_file(redenumeste_fisier(file,folder_intrari),folder_intrari)
                else:
                    print('Introduceti un document de tipul CSV sau TEXT')

