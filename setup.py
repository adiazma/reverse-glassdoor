from requests import Session
import glassdoor, json, time, os
from datetime import datetime

global session

def AuthSession():
    session = Session()
    session.headers = glassdoor.headers
    creds = json.loads(open(f'{os.getcwd()}/creds.json', 'rb').read())
    session = glassdoor.EmployeeListing(session)
    return session

AuthSession()
    
