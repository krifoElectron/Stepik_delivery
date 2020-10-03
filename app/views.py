from flask import render_template

from app import app

@app.route('/')
def render_main():
    return render_template('index.html')