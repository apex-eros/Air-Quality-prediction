from flask import Flask, jsonify, render_template, request, redirect, session
import sqlite3
from joblib import load
import numpy as np
import json


app = Flask(__name__)
app.secret_key = 'your_secret_key'

lr_model = load('model.pkl')

def predict_aqi_lr(lr, input_data):
    return lr.predict([input_data])[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        conn.commit()
        conn.close()
        
        return redirect('/login.html')
    return render_template('signup.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['username'] = user[0]
            return redirect('/')
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from request
    data = request.get_json()

    # Extract location and time from request data
    location = int(data["location"])
    time = int(data["time"])

    # Generate random gas values
    pm25, pm10, co, co2, no2, so2, o3 = np.random.uniform(0, 100, size=7)

    # Predict AQI using the loaded model
    input_data = [location, time, pm25, pm10, co, co2, no2, so2, o3]
    predicted_aqi = predict_aqi_lr(lr_model, input_data)
    print(predicted_aqi)

    op={"predicted_aqi": predicted_aqi}
  

    print(op)


    # Return predicted AQI as JSON response
    return json.dumps(op)

if __name__ == '__main__':
    app.run(debug=True)
