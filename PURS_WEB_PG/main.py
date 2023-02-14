from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from hashlib import sha256


import MQTT
MQTT.main()


app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

#db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'markopurs'
app.config['MYSQL_DB'] = 'query1'
mysql = MySQL(app)
#db

manufacturer = ('Plastika Trček', 'ESUN', 'PolyMaker', 'Creality', 'Prusa', 'ColorFabb')
colour = ('Crna', 'Bijela', 'Siva', 'Plava', 'Crvena', 'Zelena', 'Žuta')
material = ('PLA', 'PETG', 'ABS', 'ASA', 'TPU', 'TPE', 'PA-12', 'PC', 'PC-CF', 'HIPS')
promjer = ('1.75', '2.85')

def parsingFun(substring):
    print("User: " + substring[0])
    print("New ili edit filament: " + substring[1])
    print("Filament data: " + substring[2])
    print("Masa filamenta: " + substring[3])
    sub = substring[2]
    print("len of substring2: " + str(len(sub)))
    data = []

    data = [sub[i:i+2] for i in range(0, len(sub), 2)]
    print([sub[i:i+2] for i in range(0, len(sub), 2)])

    print("Proizvodjac: " + manufacturer[int(data[0])])
    print("Boja: " + colour[int(data[1])])
    print("Materijal: " + material[int(data[2])])
    print("Promjer: " + promjer[int(data[3])])
    print("Masa: " + substring[3])

    if substring[1] == '#n': 
        with app.app_context():
            query = f"REPLACE INTO filament(proizvođač, boja, materijal, promjer, masa, datum_vrijeme_upisa) VALUES ('{manufacturer[int(data[0])]}', '{colour[int(data[1])]}', '{material[int(data[2])]}', '{promjer[int(data[3])]}', '{substring[3]}', NOW())"
            cursor = mysql.connection.cursor()
            cursor.execute(query)
            mysql.connection.commit()
    elif substring[1] == '#e':
            query = f"UPDATE filament SET masa = '{substring[3]}' WHERE proizvođač = '{manufacturer[int(data[0])]}', boja = '{colour[int(data[1])]}', materijal = '{material[int(data[2])]}', promjer = '{promjer[int(data[3])]}'"
            cursor = mysql.connection.cursor()
            cursor.execute(query)
            mysql.connection.commit()




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Izbacivanje iz sessiona nakon gašenja stranice/logout-a
        for key in list(session.keys()):
            session.pop(key)
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = sha256(request.form.get('password').encode()).hexdigest()
        print(password)
        # ADD uvijete koji actually provjeravaju db
        query = f"SELECT titula FROM korisnik WHERE email = '{email}' AND HEX(password) = '{password}'"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        korisnik = cursor.fetchall()
        
        if korisnik:
            session['titula'] = korisnik[0][0]

            if (korisnik[0][0] == "admin"):
                return redirect(url_for('pocetna_admin')), 303
            
            elif (korisnik[0][0] == "user"):
                return redirect(url_for('pocetna')), 303
       
        else:
            return render_template('login.html', error='Uneseni su krivi korisnički podaci')

@app.route('/', methods=['GET'])
def pocetna():

    if 'titula' in session:
        
        headings = ("ID","Proizvođač","Boja", "Materijal","Promjer[mm]","Masa","Datum unosa")
        query = f"SELECT * FROM filament"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        filament = cursor.fetchall()
        
        return render_template('index.html', headings=headings, filament=filament)
        
    return redirect(url_for('login')), 303

@app.route('/admin', methods=['GET'])
def pocetna_admin():

    if 'titula' in session:
        
        headings = ("ID","Proizvođač","Boja", "Materijal","Promjer[mm]","Masa","Datum unosa")
        query = f"SELECT * FROM filament"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        filament = cursor.fetchall()
        
        return render_template('pocetna_admin.html', headings=headings, filament=filament)
        
    return redirect(url_for('login')), 303

@app.route('/new-user', methods=['GET','POST'])
def new_user():

    if request.method == 'GET':
        return render_template('new_user.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        query = f"INSERT INTO korisnik(email, password, titula) VALUES ('{email}',UNHEX(SHA2('{password}', 256)) , 'user')"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        mysql.connection.commit()

        #db
        # Provjera da li mail postoji, ako ne, dozvoli stvaranje
        # novog korisnika
        # if email not in db.... uzmi ove podatke i storeaj ih u db
        return redirect(url_for('pocetna_admin')), 303

    return redirect(url_for('new_user.html')), 303


@app.route('/new-filament', methods=['GET','POST'])
def new_filament():

    if request.method == 'GET':
        return render_template('new_filament.html')
    elif request.method == 'POST':
        proizvodjac = request.form.get('proizvodjac')
        boja = request.form.get('boja')
        materijal = request.form.get('materijal')
        promjer = request.form.get('promjer')

        query = f"INSERT INTO filament(proizvođač, boja, materijal, promjer, datum_vrijeme_upisa) VALUES ('{proizvodjac}','{boja}','{materijal}','{promjer}', NOW())"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        mysql.connection.commit()
        
        return redirect(url_for('pocetna_admin')), 303

    return redirect(url_for('new_filament.html')), 303

# Dodavanje ruta za sortiranje tablice:
@app.route('/sortby-ID', methods=['GET'])
def sortby_id():

    headings = ("ID","Proizvođač","Boja", "Materijal","Promjer[mm]","Masa","Datum unosa")
    query = f"SELECT * FROM filament ORDER BY id"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    filament = cursor.fetchall()

    if (session['titula'] == "admin"):
        return render_template('pocetna_admin.html', headings=headings, filament=filament)
    
    return render_template('index.html', headings=headings, filament=filament)
    

@app.route('/sortby-proizvodac', methods=['GET'])
def sortby_proizvodac():

    headings = ("ID","Proizvođač","Boja", "Materijal","Promjer[mm]","Masa","Datum unosa")
    query = f"SELECT * FROM filament ORDER BY proizvođač"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    filament = cursor.fetchall()
  
    if (session['titula'] == "admin"):
        return render_template('pocetna_admin.html', headings=headings, filament=filament)
    
    return render_template('index.html', headings=headings, filament=filament)
    
@app.route('/sortby-boja', methods=['GET'])
def sortby_boja():

    headings = ("ID","Proizvođač","Boja", "Materijal","Promjer[mm]","Masa","Datum unosa")
    query = f"SELECT * FROM filament ORDER BY boja"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    filament = cursor.fetchall()

    if (session['titula'] == "admin"):
        return render_template('pocetna_admin.html', headings=headings, filament=filament)

    return render_template('index.html', headings=headings, filament=filament)
    

@app.route('/sortby-materijal', methods=['GET'])
def sortby_materijal():

    headings = ("ID","Proizvođač","Boja", "Materijal","Promjer[mm]","Masa","Datum unosa")
    query = f"SELECT * FROM filament ORDER BY materijal"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    filament = cursor.fetchall()

    if (session['titula'] == "admin"):
        return render_template('pocetna_admin.html', headings=headings, filament=filament)

    return render_template('index.html', headings=headings, filament=filament)
    
@app.route('/sortby-promjer', methods=['GET'])
def sortby_promjer():

    headings = ("ID","Proizvođač","Boja", "Materijal","Promjer[mm]","Masa","Datum unosa")
    query = f"SELECT * FROM filament ORDER BY promjer"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    filament = cursor.fetchall()

    if (session['titula'] == "admin"):
        return render_template('pocetna_admin.html', headings=headings, filament=filament)

    return render_template('index.html', headings=headings, filament=filament)
    
@app.route('/sortby-masa', methods=['GET'])
def sortby_masa():

    headings = ("ID","Proizvođač","Boja", "Materijal","Promjer[mm]","Masa","Datum unosa")
    query = f"SELECT * FROM filament ORDER BY masa"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    filament = cursor.fetchall()

    if (session['titula'] == "admin"):
        return render_template('pocetna_admin.html', headings=headings, filament=filament)

    return render_template('index.html', headings=headings, filament=filament)
    
@app.route('/sortby-datum', methods=['GET'])
def sortby_datum():

    headings = ("ID","Proizvođač","Boja", "Materijal","Promjer[mm]","Masa","Datum unosa")
    query = f"SELECT * FROM filament ORDER BY datum_vrijeme_upisa"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    filament = cursor.fetchall()

    if (session['titula'] == "admin"):
        return render_template('pocetna_admin.html', headings=headings, filament=filament)

    return render_template('index.html', headings=headings, filament=filament)

if __name__ == '__main__':
    app.run()

