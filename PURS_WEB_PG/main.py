from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

#db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'markopurs'
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

        # ADD uvijete koji actually provjeravaju db
        #query = f"SELECT email, password FROM korisnik"
        #cursor = mysql.connection.cursor()
        #cursor.execute(query)
        #korisnik = cursor.fetchall()
        #print(korisnik)
        #result = [i[0] for i in korisnik]
        #print (result)
        #print (result [0])
        #print (result [1])
        #print (result [2])

        #for i in result:
        if email == 'test@gmail.com' and password == 'test':
            session['username'] = 'test'
            return redirect(url_for('pocetna')), 303
        elif email == 'admin@gmail.com' and password == 'admin':
            session['username'] = 'admin'
            return redirect(url_for('pocetna_admin')), 303
        else:
            return render_template('login.html', error='Uneseni su krivi korisnički podaci')


@app.route('/', methods=['GET'])
def pocetna():
    print(session)

    if 'username' in session:

        #db
        #query = f"SELECT * FROM filament"
        #cursor = mysql.connection.cursor()
        #cursor.execute(query)
        #filament = cursor.fetchall()
        #print(filament)
        #return f'Filamenti: {filament}', 200
        #db
        #return render_template('index.html', filament=filament)
        return render_template('index.html')
    return redirect(url_for('login')), 303

@app.route('/admin', methods=['GET'])
def pocetna_admin():
    print(session)

    if 'username' in session:
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
        #db
        stringfirst = "INSERT INTO korisnik(email, password, titula) VALUES('"
        stringmidd = "', UNHEX(SHA2('"
        stringlast = "', 256)), 'user')"
        query = f'{stringfirst} {email} {stringmidd} {password} {stringlast}'
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        mysql.connection.commit()
        mysql.connection.close()
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
        masa = request.form.get('masa')
        datum = request.form.get('datum')
        
    # Provjera da li mail postoji, ako ne, dozvoli stvaranje
    # novog korisnika
    # if email not in db.... uzmi ove podatke i storeaj ih u db
        return redirect(url_for('pocetna_admin')), 303

    return redirect(url_for('new_filament.html')), 303

if __name__ == '__main__':
    app.run()

