from flask import Flask, request, session, redirect, url_for, render_template, flash
import requests
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash

headers = {
 "X-RapidAPI-Key": "VwcLhnprCsWnvoLjuNQ6eXAoEdiNa0DCnyWbCrpo5wBx3CgnDY0sFInBar7Tedti",
 "X-RapidAPI-Host": "spec-it.p.rapidapi.com"
}

app = Flask(__name__)
app.secret_key = "bkvdsfkbvsfudbhsdfbhuo"

conn = psycopg2.connect(database="PyProject_db", user="postgres", password="7410", host="127.0.0.1", port="5432")


@app.route('/', methods=["POST", "GET"])
def index():

    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cur.fetchone()

        if account:
            password_rs = account['password']
            if check_password_hash(password_rs, password):
                session['loggedin'] = True
                session['username'] = account['username']
                return redirect(url_for('nft'))
            else:
                flash('Incorrect username/password')
        else:
            flash('Incorrect username/password')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        repass = request.form['repass']

        if password == repass:

            _hashed_password = generate_password_hash(password)

            cur.execute('SELECT * FROM users WHERE username = %s', (username,))
            account = cur.fetchone()

            if account:
                flash('Account already exists!')
            else:

                cur.execute("INSERT INTO users (fullname, username, password) VALUES (%s,%s,%s) RETURNING *", (fullname, username, _hashed_password))
                account = cur.fetchone()
                conn.commit()
                session['loggedin'] = True
                session['username'] = account['username']
                return redirect(url_for('nft'))

        else:
            flash('Passwords do not match')
    elif request.method == 'POST':

      flash('Please fill out the form!')

    return render_template('register.html')


@app.route('/Error')
def error():
    return render_template('Error.html')

@app.route('/nft', methods=['GET', 'POST'])
def nft():
    if 'loggedin' in session:
        if request.method == 'POST':
            returnValue=""
            address = request.form.get('address')
            if(db(address)):
                cur = conn.cursor()
                cur.execute("SELECT nft_metadata FROM nfts where nft_address='"+address+"'")
                records = cur.fetchall()
                returnValue=records[0][0]
            else:            
                url = "https://solana-gateway.moralis.io/nft/mainnet/{}/metadata".format(address)
                headers = {
                    "X-API-Key": "VwcLhnprCsWnvoLjuNQ6eXAoEdiNa0DCnyWbCrpo5wBx3CgnDY0sFInBar7Tedti"
                }
                returnValue = requests.get(url, headers=headers).text
                cur = conn.cursor()
                cur.execute("insert into nfts(nft_address,nft_metadata) values('{}','{}')".format(address, returnValue))
                conn.commit()
            return '''
                    <h1>{}</h1>
                    '''.format(returnValue)
        return render_template('index.html')
    else:
        return redirect(url_for('login'))
 


    


def db(address):
    conn = psycopg2.connect("dbname=PyProject_db user=postgres password='7410'")
    cur = conn.cursor()
    cur.execute("SELECT * FROM nfts where nft_address='"+address+"'")
    if(cur.rowcount==0):
        return False
    return True


@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('username', None)

   return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
