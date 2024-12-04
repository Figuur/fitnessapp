from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
import mysql.connector

mydb = mysql.connector.connect(
  host="raimondappdb.mysql.database.azure.com",  #port erbij indien mac
  user="raimondadmin",
  password="uiop7890UIOP&*()",
  database="lutsendb"
)

@app.route("/testkort")
def oefeningen():
    return "halter benchpress"

@app.route("/bench_oefeningen")
def alleoefeningen():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM bench_oefeningen")
    myresult = mycursor.fetchall()
    keys = [i[0] for i in mycursor.description]
    data = [
        dict(zip(keys, row)) for row in myresult
    ]
    return data

# verwijder kaart probeersel 
@app.route('/bench_oefeningen/<int:bench_oefeningen>')

def delete(bench_oefeningen):
    delete_card = delete.bench_oefeningen.get_or_404(bench_oefeningen)

    try:
        bench_oefeningen.session.delete(delete_card)
        bench_oefeningen.session.commit()
        

    except:
        return "er was een probleem met het verijderen van de kaart"

    
        
    

@app.route('/bench_oefeningen', methods=['POST'])

def bench_oefeningen():

    oefening = request.json
    print("hallo")
    # Voeg nieuwe oefening toe aan de database
    print(oefening["duur"])
    

    sql = "INSERT INTO bench_oefeningen (duur, sets, Aantal_keer, oefeningen, Omschrijving) VALUES (%s, %s, %s, %s, %s)"
    val = (oefening["duur"], oefening["sets"], oefening["Aantal_keer"], oefening["oefeningen"], oefening["Omschrijving"])

    mycursor = mydb.cursor()
    mycursor.execute(sql, val)

    mydb.commit()
    
    return "<p>Hello, World!!! ??? </p>"

@app.route("/upload", methods=["POST"])
def uploaden():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200