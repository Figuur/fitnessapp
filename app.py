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

@app.route('/add_exercise', methods=['POST'])
def add_exercise():
    data = request.json
    
    # Voeg nieuwe oefening toe aan de database
    new_exercise = {
        'Oefeningen': data['Oefeningen'],
        'Sets': data['Sets'],
        'Aantal_keer': data['Aantal_keer'],
        'Omschrijving': data['Omschrijving']
    }
    
    # Voeg hier je database logica toe
    # Bijvoorbeeld: db.bench_oefeningen.insert_one(new_exercise)
    
    return jsonify({'message': 'Exercise added successfully'})