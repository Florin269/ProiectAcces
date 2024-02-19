from flask import Flask , request, jsonify, render_template,url_for,flash,redirect
import mysql.connector
from const import *
from dateutil import parser
from datetime  import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


app= Flask(__name__)
app.config['SECRET_KEY'] = 'parola123'

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

class LoginForm(FlaskForm):
    username = StringField('Utilizator', validators=[DataRequired()])
    password = PasswordField('Parola', validators=[DataRequired()])
    submit = SubmitField('Conectare')
    

def verifica_credentiale(username, password):
    try:
        query = f"SELECT * from `cladire`.`administrator` where NumeAdministrator = '{username}';"
        print(query)
        user=mysqlcon.selecteaza_din_baza_de_date(query)
        print(user)
        if user:
            if user[0][2]== password:
                return True
            else:
                return False
    except Exception as e:
        print(f'Eroare la verificarea credentialelor: str{(e)}')
            

@app.route('/', methods =['GET','POST'])
def index():
    form=LoginForm()
    if form.validate_on_submit():
        if verifica_credentiale(form.username.data,form.password.data):
            flash('Autentificare reusita!','success')
            return redirect(url_for('logged_in'))
        else:
            flash('Autentificare esuata.Verificare user si parola')
    return render_template('index.html',form=form)

@app.route('/logged-in')
def logged_in():
    return render_template('logged_in.html')

@app.route('/utilizator', methods = ['POST'])
def utilizator():
    try:
        request_data = request.json
        Id = request_data['Id']
        nume = request_data['Nume']
        prenume = request_data['Prenume']
        companie = request_data['Companie']
        IdManager = request_data['IdManager']
        Email = request_data['Email']
        query = f"INSERT INTO `cladire`.`persoane` VALUES ({Id},'{nume}','{prenume}','{companie}','{IdManager}','{Email}');"
        mysqlcon.adauga_in_baza_de_date(query)
        return('Datele au fost adaugate cu succes')
    except TypeError as e:
        print(f'Datele nu au fost adaugate din cauza erori: {e}')


@app.route('/acces', methods=['POST'])
def acces():
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

@app.route('/statistici', methods = ['GET'])
def statistici():
    query = f'SELECT * FROM `cladire`.`acces`'
    data=mysqlcon.selecteaza_din_baza_de_date(query)
    return render_template('statistici.html', data=data)



if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
