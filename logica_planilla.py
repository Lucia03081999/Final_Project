from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import csv
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions
from config import *
import watson_developer_cloud

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Horarios'


def funcion_sentimiento(x):
    natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2017-02-27',
            username=sentiment_user,
            password=sentiment_pass)
    try:
        response = natural_language_understanding.analyze(
            text=str(x),
            features=Features(sentiment=SentimentOptions()))
        sent= json.dumps(response['sentiment']['document']['label'])
        if sent == '"positive"':
            sentimiento = 'positivo'
        elif sent == '"negative"':
            sentimiento = 'negativo'
        else:
            sentimiento = 'neutral'
            return sentimiento
    except watson_developer_cloud.watson_service.WatsonApiException:
        sentimiento = '(Sentimiento no detectado) '
        return sentimiento

    
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        print('Llegue2')
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main_sheets():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1WjlpwJmKGWVwM24tWm5jQGM-_Rk4MwA51uvGTnsB_aw'
    rangeName = 'Form Responses 1'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    if not values:
        return('No data found.')
    else:
        planilla = ''
        with open ('sheet.csv', 'w') as archive:
            writer = csv.writer(archive)
            writer.writerows(values)
            with open ('sheet.csv','r') as archive:
                reader = csv.reader(archive)
                with open('values.txt','w') as v:
                    v.write(str(values))
        
                for row in reader:
                    line = '{}{}'.format(str(row)[1:-1],'</br>')
                    planilla = planilla + line
                return planilla




def sent_sentimiento():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1WjlpwJmKGWVwM24tWm5jQGM-_Rk4MwA51uvGTnsB_aw'
    rangeName = 'Form Responses 1'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    if not values:
        return('No data found.')
    else:
        answers = values[1: -1]
        DictSent = { }
        number = 0
        number3 = 0
        try:
            for i in range(0 , 100):
                ans = answers[number]
                ans = str(ans).split("', '")
                number2 = 0
                number = number + 1
                try:
                    for i in range(0 , 20):
                        DictSent [str(number3)] = ans[number2]
                        number2 = number2 +1
                        number3 = number3 +1
                        
                except IndexError:
                    pass


        except IndexError:
            pass
        
        numero4 = 0
        sentimientos = { }
        

        with open('sentimientos.csv','w+') as archivo_sentimientos:
            try:
                for i in range (0, 1500):
                
                    respuesta = DictSent[str(numero4)]
                    sentimiento = funcion_sentimiento(respuesta)
                    sentimientos [str(respuesta)] = sentimiento
                    numero4 = numero4 + 1
                        
            except IndexError:
                pass
            return str(sentimientos)
