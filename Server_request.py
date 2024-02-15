from flask import Flask , request, jsonify, render_template
import mysql.connector
from const import *
from dateutil import parser
from datetime  import datetime

app= Flask(__name__)

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


def formatare_data(data_originala):
    data_obj = parser.parse(data_originala)
    data_formatata = data_obj.strftime('%Y-%m-%d %H:%M:%S')
    return data_formatata

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/acces', methods=['POST'])
def save_data():
    try:
        request_data = request.json
        data = request_data['data']
        sens = request_data['sens']
        id_persoana = request_data['idPersoana']
        id_poarta = request_data['idPoarta']
        query = f"INSERT INTO `cladire`.`acces` VALUES (null,{id_persoana},'{formatare_data(data)}','{sens}',{id_poarta});"
        mysqlcon.adauga_in_baza_de_date(query)
        return('Datele au fost adaugate cu succes')
    except TypeError as e: 
        print(f'Datele nu au fost adaugate din cauza erori: {e}')

if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)