from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from hashlib import sha256

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

#db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'query1'
mysql = MySQL(app)
#db


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        hexpass = sha256(password.encode()).hexdigest()
        print(hexpass)
        # ADD uvijete koji actually provjeravaju db
        query = f"SELECT titula FROM korisnik WHERE email = '{email}' AND password = HEX(password) = '{password}'"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        korisnik = cursor.fetchall()
        print(korisnik)
        
        if korisnik:
            session['titula'] = korisnik[0][0]
            print(korisnik[0][0])
            if (korisnik[0][0] == "admin"):
                print("U admin if")
                return redirect(url_for('pocetna_admin')), 303
            elif (korisnik[0][0] == "user"):
                print("U user if")
                return redirect(url_for('pocetna')), 303
        else:
            return render_template('login.html', error='Uneseni su krivi korisnički podaci')

@app.route('/', methods=['GET'])
def pocetna():
    #print(session)

    if 'titula' in session:

        #db
        headings = ("Proizvođač","Boja", "Materijal","Promjer[mm]","Masa","Datum unosa")

        query = f"SELECT * FROM filament"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        filament = cursor.fetchall()
        print(filament)
        #return f'Filamenti: {filament}', 200
        #db
        return render_template('index.html', headings=headings, filament=filament)
        #return render_template('index.html')
    return redirect(url_for('login')), 303

@app.route('/admin', methods=['GET'])
def pocetna_admin():
    print(session)

    if 'titula' in session:
        return render_template('pocetna_admin.html')

    return redirect(url_for('login')), 303

@app.route('/new-user', methods=['GET','POST'])
def new_user():
    print(session)

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
    print(session)

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
        
    # Provjera da li mail postoji, ako ne, dozvoli stvaranje
    # novog korisnika
    # if email not in db.... uzmi ove podatke i storeaj ih u db
        return redirect(url_for('pocetna_admin')), 303

    return redirect(url_for('new_filament.html')), 303

if __name__ == '__main__':
    app.run()

