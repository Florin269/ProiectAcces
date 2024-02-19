import os
import mysql.connector
import shutil
import time
import csv
import re
from const import *
from dateutil import parser
from datetime  import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule



class MySqlConnection:
    def __init__(self):
        self.mydb = mysql.connector.connect(host ='localhost', user='root', password = password, database = bazadate)
        self.cursor =self.mydb.cursor()

    def selecteaza_din_baza_de_date(self,query):
        self.cursor.execute(query)
        rezultat = self.cursor.fetchall()
        return rezultat

mysqlcon=MySqlConnection()



class Monitorizare():
    def __init__(self):
        pass
        
    def salveaza_in_fisier_csv(self,date):
        data_curenta = datetime.now()
        nume_fisier = f'{data_curenta.strftime("%Y-%m-%d")}_chiulangii.csv'
        with open(folder_backup_intrari + '/' + nume_fisier, 'w', newline='') as file_csv:
            writer = csv.writer(file_csv)
            writer.writerow(['Nume', 'OreLucrate'])

            for data in date:
                writer.writerow(data)

    def salveaza_in_fisier_txt(self,date):
        data_curenta = datetime.now()
        nume_fisier = f'{data_curenta.strftime("%Y-%m-%d")}_chiulangii.txt'
        with open(folder_backup_intrari + '/' + nume_fisier, 'w', newline='') as file_txt:
            writer = csv.writer(file_txt)
            for data in date:
                writer.writerow(data)

    def trimitere_email(self,listaangajatii):
            EmailManager = ManagerEmail
            for angajat in listaangajatii:
                msg = MIMEMultipart()
                msg['From'] = EmailTrimite
                msg['To'] = EmailManager
                msg['Subject'] = f'Atenție: {angajat[0]} a chiulit astăzi!'
                body = f'Bună ziua,\n\n{angajat[0]} a chiulit astăzi și a lucrat doar {angajat[1]} ore.'
                msg.attach(MIMEText(body, 'plain'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(EmailTrimite, parolaemail)
                text = msg.as_string()
                server.sendmail(EmailTrimite, EmailManager, text)
                server.quit()
         

    def extragere_date(self):
        data_curenta = datetime.now().strftime('%Y-%m-%d')
        inceput_zi = datetime.strptime(f'{data_curenta} 00:00:00', '%Y-%m-%d %H:%M:%S')
        sfarsit_zi = datetime.strptime(f'{data_curenta} 23:59:59', '%Y-%m-%d %H:%M:%S')
        query = f"SELECT persoane.Nume, SUM(CASE WHEN AC.Sens = 'out' THEN 1 WHEN AC.Sens = 'in' THEN  -1 END * HOUR(AC.Data)) as OreLucrate FROM `cladire`.`acces` AC JOIN persoane ON AC.ID_Persoana = persoane.ID  WHERE AC.Data BETWEEN '{inceput_zi}' AND '{sfarsit_zi}' GROUP BY persoane.Nume HAVING OreLucrate < 8;"
        rezultate = mysqlcon.selecteaza_din_baza_de_date(query)
        monitor.salveaza_in_fisier_csv(rezultate)
        monitor.salveaza_in_fisier_txt(rezultate)
        monitor.trimitere_email(rezultate)
        return rezultate


monitor = Monitorizare()
monitor.extragere_date()

