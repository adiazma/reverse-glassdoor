from requests import Session
import glassdoor, json, time, os
from datetime import datetime

global session

def AuthSession():
    session = Session()
    session.headers = glassdoor.headers
    creds = json.loads(open(f'{os.getcwd()}/creds.json', 'rb').read())
    return glassdoor.Auth(session, creds)

def LoopSession(session, page={}):
    files = glassdoor.EmployeeListing(session, page=page)['data']['jobListings']['jobListings']
    for item in files:
        key = item['jobview']['header']['jobResultTrackingKey'].split('-')[-1]
        glassdoor.EmployeeQuestions(session, key)
    
session, page = AuthSession()
LoopSession(session, page)
    
