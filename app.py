from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

# Database connectie functie
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lutsendb"
        )
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        raise

@app.route("/testkort")
def oefeningen():
    return "halter benchpress"

@app.route("/test-db")
def test_db():
    """Test endpoint om te zien wat de database teruggeeft"""
    try:
        mydb = get_db_connection()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM bench_oefeningen LIMIT 1")
        myresult = mycursor.fetchall()
        
        if not myresult:
            mycursor.close()
            mydb.close()
            return jsonify({'message': 'Geen data gevonden', 'columns': 'N/A'})
        
        # Get column names
        keys = [i[0] for i in mycursor.description]
        mycursor.close()
        mydb.close()
        
        return jsonify({
            'message': 'Database connectie succesvol',
            'columns': keys,
            'sample_data': dict(zip(keys, myresult[0])) if myresult else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/bench_oefeningen1")
def alleoefeningen():
    try:
        mydb = get_db_connection()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM bench_oefeningen")
        myresult = mycursor.fetchall()
        
        if not myresult:
            mycursor.close()
            mydb.close()
            return jsonify([]), 200  # Return empty array if no results
        
        keys = [i[0] for i in mycursor.description]
        data = []
        
        # Create data with both original and normalized column names for frontend compatibility
        for row in myresult:
            row_dict = dict(zip(keys, row))
            normalized = row_dict.copy()
            
            # Add normalized versions for frontend compatibility
            for key, value in row_dict.items():
                key_lower = key.lower()
                # Map to frontend expected names (case-sensitive)
                if key_lower == 'oefeningen':
                    normalized['Oefeningen'] = value
                if key_lower == 'sets':
                    normalized['Sets'] = value
                if key_lower == 'id' or key == 'bench_oefeningen':
                    normalized['bench_oefeningen'] = value
                if key_lower == 'omschrijving':
                    normalized['Omschrijving'] = value
            
            data.append(normalized)
        
        mycursor.close()
        mydb.close()
        print(f"Returning {len(data)} records")  # Debug output
        return jsonify(data)  # gebruik jsonify voor JSON response
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/bench_oefeningen3/<int:oef_id>', methods=['DELETE'])
def verwijderen(oef_id):
    mydb = get_db_connection()
    mycursor = mydb.cursor()
    sql = "DELETE FROM bench_oefeningen WHERE id = %s"
    mycursor.execute(sql, (oef_id,))
    mydb.commit()
    mycursor.close()
    mydb.close()
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
    mydb = get_db_connection()
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()
    mydb.close()
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



@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)