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
        user=mysqlcon.selecteaza_din_baza_de_date(query)
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

@app.route('/sterge_utilizator', methods =['GET'])
def stergere_utilizator_page():
    return render_template('stergere_utilizator.html')

        
@app.route('/sterge_utilizator', methods =['POST'])
def sterge_utilizator():
    try:
        id_utilizator = request.form['idUtilizator']
        query = f"DELETE FROM `cladire`.`persoane` WHERE Id = {id_utilizator};"
        mysqlcon.adauga_in_baza_de_date(query)
        return (f'Utilizatorul cu id-ul:{id_utilizator}')
    except TypeError as e:
        print(f'Utilizator nu a fost sters: {e}')


@app.route('/adauga_utilizator', methods = ['GET'])
def adauga_utilizator_page():
    return render_template('utilizator.html')

@app.route('/adauga_utilizator', methods = ['POST'])
def adauga_utilizator():
    nume = request.form['nume']
    prenume = request.form['prenume']
    companie = request.form['companie']
    id_manager = request.form['idManager']
    email = request.form['email']
    query = f"INSERT INTO `cladire`.`persoane` VALUES(null,'{nume}','{prenume }','{companie}',{id_manager},'{email}');"
    mysqlcon.adauga_in_baza_de_date(query)
    return jsonify({'status': 'success', 'message': 'Utilizatorul a fost adăugat cu succes în baza de date.'})

    

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
    data_curenta = datetime.now().strftime('%Y-%m-%d')
    inceput_zi = datetime.strptime(f'{data_curenta} 00:00:00', '%Y-%m-%d %H:%M:%S')
    sfarsit_zi = datetime.strptime(f'{data_curenta} 23:59:59', '%Y-%m-%d %H:%M:%S')
    query1 = f'SELECT * FROM `cladire`.`acces`'
    data=mysqlcon.selecteaza_din_baza_de_date(query1)
    query2 = f'SELECT * FROM `cladire`.`persoane`'
    data1 = mysqlcon.selecteaza_din_baza_de_date(query2)
    query3 =f"SELECT persoane.Nume, SUM(CASE WHEN AC.Sens = 'out' THEN 1 WHEN AC.Sens = 'in' THEN  -1 END * HOUR(AC.Data)) as OreLucrate FROM `cladire`.`acces` AC JOIN persoane ON AC.ID_Persoana = persoane.ID  WHERE AC.Data BETWEEN '{inceput_zi}' AND '{sfarsit_zi}' GROUP BY persoane.Nume;"
    data2 = mysqlcon.selecteaza_din_baza_de_date(query3)
    return render_template('statistici.html', data=data, data1=data1,data2=data2)
    




if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
