from flask import Flask
from flask import request
import mysql.connector
import sys
import json
import hashlib

with open('config.json') as config_data_file:
    config = json.load(config_data_file)

mysqlconfig = config['mysql']
appconfig = config['app']

mydb = mysql.connector.connect(
    host=mysqlconfig['host'],
    port=mysqlconfig['port'],
    auth_plugin=mysqlconfig['auth_plugin'],
    user=mysqlconfig['user'],
    passwd=mysqlconfig['passwd'],
    database=mysqlconfig['db']
)
mycursor = mydb.cursor()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/electricityusage', methods=['POST'])
def postusage():
    reqdata = request.get_json()

    print('request: ', reqdata, file=sys.stderr)

    #check if all values are set
    if (not 'start' in reqdata) or reqdata['start']=='':
        return 'start field is required'
    if (not 'end' in reqdata) or reqdata['end']=='':
        return 'end field is required'
    if not 'watthour' in reqdata:
        return 'watthour field is required'
    if not 'key' in reqdata:
        return 'API key is required'

    #authentication check
    keyhash = (hashlib.sha256(reqdata['key'].encode('utf-8'))).hexdigest()
    if keyhash != appconfig['API_KEY']:
        return 'Authentication failed'

    sql = "INSERT INTO consumption (start, end, watthour) VALUES (%s, %s, %s)"
    entry = (reqdata['start'], reqdata['end'], reqdata['watthour'])
    mycursor.execute(sql, entry)
    mydb.commit()
    return 'ok'

if __name__ == '__main__':
    app.run(host=appconfig['ip'], port=appconfig['port'], debug=appconfig['debug'])