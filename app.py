from flask import Flask, render_template, jsonify, request, Response
import requests
import os
import pandas as pd
import json
from datetime import datetime
from data_maker import get_data

app = Flask(__name__)

@app.route('/data',methods=['POST'])
def data():
    gameid = request.form['text']
    return Response(json.dumps(get_data(gameid)))

@app.route('/')
def timeline():
    gameid = '0041500116'
    return render_template('index.html',data=get_data(gameid))

@app.route('/', methods=['POST'])
def timeline_post():
    gameid = request.form['text']
    return render_template('index.html',data=get_data(gameid))

if __name__ == '__main__':
    app.run(debug=True)