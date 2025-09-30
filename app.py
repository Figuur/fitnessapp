from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

# Lokale database connectie
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="lutsendb"
)

@app.route("/testkort")
def oefeningen():
    return "halter benchpress"

@app.route("/bench_oefeningen1")
def alleoefeningen():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM bench_oefeningen")
    myresult = mycursor.fetchall()
    keys = [i[0] for i in mycursor.description]
    data = [dict(zip(keys, row)) for row in myresult]
    return jsonify(data)  # gebruik jsonify voor JSON response

@app.route('/bench_oefeningen3/<int:oef_id>', methods=['DELETE'])
def verwijderen(oef_id):
    mycursor = mydb.cursor()
    sql = "DELETE FROM bench_oefeningen WHERE id = %s"
    mycursor.execute(sql, (oef_id,))
    mydb.commit()
    return jsonify({'message': f'Oefening {oef_id} verwijderd'})

@app.route('/bench_oefeningen', methods=['POST'])
def toevoegen():
    oefening = request.json
    sql = """
        INSERT INTO bench_oefeningen (duur, sets, Aantal_keer, oefeningen, Omschrijving) 
        VALUES (%s, %s, %s, %s, %s)
    """
    val = (
        oefening["duur"], oefening["sets"], oefening["Aantal_keer"], 
        oefening["oefeningen"], oefening["Omschrijving"]
    )
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    return jsonify({'message': 'Oefening toegevoegd!'})

@app.route("/upload", methods=["POST"])
def uploaden():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    UPLOAD_FOLDER = './uploads'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path})
