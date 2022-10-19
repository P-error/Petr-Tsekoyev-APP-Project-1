from flask import Flask, request
import requests
import psycopg2
app = Flask(__name__)

@app.route('/')
def index():
    return 'Get NFT'

@app.route('/nft', methods=['GET', 'POST'])
def get_nft():
    if request.method == 'POST':
        returnValue=""
        address = request.form.get('address')
        if(db(address)):
            conn = psycopg2.connect("dbname=nft_db user=postgres password='7410'")
            cur = conn.cursor()
            cur.execute("SELECT nft_metadata FROM nft where nft_address='"+address+"'")
            records = cur.fetchall()
            returnValue=records[0][0]
        else:            
            url = "https://solana-gateway.moralis.io/nft/mainnet/{}/metadata".format(address)
            headers = {
                "X-API-Key": "VwcLhnprCsWnvoLjuNQ6eXAoEdiNa0DCnyWbCrpo5wBx3CgnDY0sFInBar7Tedti"
            }
            returnValue = requests.get(url, headers=headers).text
            conn = psycopg2.connect("dbname=nft_db user=postgres password='7410'")
            cur = conn.cursor()
            cur.execute("insert into nft(nft_address,nft_metadata) values('{}','{}')".format(address, returnValue))
            conn.commit()
        return '''
                <h1>{}</h1>
                  '''.format(returnValue)
    return '''
           <form method="POST"style="margin: left; width: 220px; text-align: left;">
               <div><label>Enter an Address: <input type="text" name="address"></label></div>
               <input type="submit" value="Submit">
           </form>'''


def db(address):
    conn = psycopg2.connect("dbname=nft_db user=postgres password='7410'")
    cur = conn.cursor()
    cur.execute("SELECT * FROM nft where nft_address='"+address+"'")
    if(cur.rowcount==0):
        return False
    return True

if __name__ == '__main__':

    app.run(debug=True, port=5001)