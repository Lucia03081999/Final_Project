from functools import wraps
import requests
import os
from flask import Flask, request, Response
from config import *
import json
import time
import datetime
import os 
from pymongo import MongoClient
from bson import json_util
import collections
from logica_planilla import *
import csv

app = Flask(__name__)

@app.route('/')
def hola():
    return('<h1>Holi, soy la página principal (´･ω･`)')
# Esta parte del codigo funciona, pero da un error (Sospecho que es mi libreria) que no permite ver las páginas.
@app.after_request
def after(response):
    log ={
        'service':str(request.url_rule),
        'date':str(datetime.datetime.now()),
        'status':{
            'code': str(response.status_code),
            'text': str(response.status)
            },
        'responses':
        {
            'long':str(response.content_length),
            'type':str(response.content_type),
            'mimetype': str(response.mimetype)},
        'user':{
            'ip_user': str(request.environ['REMOTE_ADDR']),
            'user_port': str(request.environ['REMOTE_PORT'])
            }
        }
    
    client = MongoClient(mongo_uri)
    db = client.test_database
    collection = db.test_collection
    try:
        insertar_log = collection.insert_one(log)
        if insertar_log.acknowledged == True:
            
            print('Now Saving: ', log)
            print ('Success: saved log. ')
    except:
        print('Error: nos vamos. ', sys.exc_info())
#Si quitamos el código que va hasta aquí, no sale ningún error


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    for user in USERS:
        if (user['user'] == username and user['pass'] == password):            
            return True
        else:
            print('Error: sus credenciales no coinciden.')

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/resultados')
def resultados():
    return main_sheets()

@app.route('/microdatos')
def microdatos():
    return sent_sentimiento()       
@app.route('/pagina_que_funciona')
def mostrar():
    return('esta pagina funcionaa')
app.run()


