from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
db_name = 'narchives.db'


supported_genres = [
    "noisecore",
    "gorenoise",
    "noise",
    "harsh noise"
]

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

    # get albums
    try:
        return render_template('band.html', artist=data[0])
    except:
        return "WTF??? Index error or some shit I don't know why it fucked up", 400


@app.route('/make_band', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        bandname = request.form['bandname']
        formed   = request.form['formed']
        split_up = request.form['splitup']
        genre    = request.form['genre']

        counter = 0
        for i in range(len(supported_genres)):
            if genre.lower() == supported_genres[i]:
                counter += 1

        if counter == 0: # Unknown / Unsupported
            return f"Unsupported genre {genre}!", 400

        with sqlite3.connect(db_name) as band:
            cursor = band.cursor()
            cursor.execute("INSERT INTO artist \
                    (NAME,FORMED,SPLITUP,GENRE) VALUES (?,?,?,?)",
                        (bandname, formed, split_up, genre))
            band.commit()

        return render_template("added-band.html")
    else:
        return render_template("create-artist.html", genres=supported_genres)

@app.route('/showbands')
def showbands():
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM artist')

    data = cursor.fetchall()
    return render_template('bands.html', data=data)


data = ""
@app.route('/addalbum', methods=['POST', 'GET'])
def albumadd():
    bandid = 0
    if request.method == 'GET':
        bandid = request.args.get('id')
        print(f"Band id is {bandid}")

        # Retrieve data so we can form our POST request
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            cur.execute(f"SELECT NAME FROM artist WHERE ID={bandid}")
            global data
            data = cur.fetchone()[0]
            db.commit()

        return render_template('create-album.html')
    elif request.method == 'POST':
        print(data)
        album_name   = request.form['albumname']
        release_year = request.form['released']

        print(f"Album '{album_name}' was released in '{release_year}' by {data}")
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            cur.execute("INSERT INTO album (ARTIST_NAME, ALBUM_NAME, YEAR) VALUES (?,?,?)",
                        (data, album_name, release_year))
            db.commit()
        print("DB added")
        return redirect(url_for('get_band', id=bandid+1))
# Index route
@app.route('/')
def index_route():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

