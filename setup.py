from requests import Session
import glassdoor, json, time, os
from datetime import datetime

global session

def AuthSession():
    session = Session()
    session.headers = glassdoor.headers
    creds = json.loads(open(f'{os.getcwd()}/creds.json', 'rb').read())
    #session = glassdoor.Auth(session)
    return session

def LoopSession(session):
    files = glassdoor.EmployeeListing(session)['data']['jobListings']['jobListings']
    for item in files:
        print(item['jobview'].keys())
    
session = AuthSession()
LoopSession(session)
    
