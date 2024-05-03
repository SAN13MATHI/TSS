# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('JWT_SECRET')  # Set a secret key for flash messages

# Connect to MongoDB
client = MongoClient(os.getenv('MONGO_URI'))
db_name = 'test'  # Assuming your database name is 'test'
db = client[db_name]

users_collection = db['users']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Insert user data into MongoDB
        users_collection.insert_one({'username': username, 'password': password})
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if user exists in MongoDB
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('about', username=username))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/about/<username>')
def about(username):
    return render_template('about.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
