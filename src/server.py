from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
db_name = 'narchives.db'

# Each band gets it's own page, e.g. /band?id=2
@app.route('/band')
def get_band():
    artist_id = request.args.get('id')
    if artist_id is None:
        return "Fuck u want me to do? U didnt provide a band ID!", 400
    
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute(f'SELECT * FROM artist WHERE ID={artist_id}')

    data = cursor.fetchall()
    return render_template('band.html', artist=data[0])


@app.route('/make_band', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        bandname = request.form['bandname']
        formed   = request.form['formed']
        split_up = request.form['splitup']
        genre    = request.form['genre']

        with sqlite3.connect(db_name) as band:
            cursor = band.cursor()
            cursor.execute("INSERT INTO artist \
                    (NAME,FORMED,SPLITUP,GENRE) VALUES (?,?,?,?)",
                        (bandname, formed, split_up, genre))
            band.commit()
        return render_template("added-band.html")
    else:
        return render_template("create-artist.html")

@app.route('/showbands')
def showbands():
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM artist')

    data = cursor.fetchall()
    return render_template('bands.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

