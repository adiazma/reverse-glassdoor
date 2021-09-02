from requests import Session, Response, Request
from urllib.parse import urlencode, quote
from bs4 import BeautifulSoup
import json, os, requests, mysql.connector, math
import base64

BASE_URL = 'www.glassdoor.ca'

HOST = '192.168.1.105'

DATABASE = 'productos'

USER = 'admin'

PASSWORD = 'admin'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'es-419,es;q=0.9',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'upgrade-insecure-requests': '1',
    'Referer': f'https://{BASE_URL}/',
    'Origin': f'https://{BASE_URL}',
}

# Functions
def set_session_cookies(_session, cookies):
    for cookie in cookies:
        if 'httpOnly' in cookie:
            cookie['rest'] = {'httpOnly': cookie.pop('httpOnly')}
        if 'expiry' in cookie:
            cookie['expires'] = cookie.pop('expiry')
        if 'sameSite' in cookie:
            cookie.pop('sameSite')
        _session.cookies.set(**cookie)

def get_session_cookies(session, filters=[]):
    cookies = []
    if session:
        for cookie in session.cookies:
            if filters and cookie.name not in filters:
                continue
            cookie_dict = {'name': cookie.name, 'value': cookie.value}
            if cookie.domain:
                cookie_dict['domain'] = cookie.domain
            cookies.append(cookie_dict)
    return cookies

# Monster
def EmployeeListing(_session, employee='python'):
    url = f'https://{BASE_URL}/'
    request = Request('GET', url=url, headers=headers)
    req = _session.prepare_request(request)
    response = _session.send(req)

    print(response.headers)
    print(response.cookies.get_dict())

    url = f'https://{BASE_URL}/graph'
    request = Request('POST', url=url, data=str.encode(json.dumps({
        'operationName': 'JobSearchQuery',
        'query': 'query JobSearchQuery($searchParams: SearchParams) {\n  jobListings(contextHolder: {searchParams: $searchParams}) {\n    adOrderJobLinkImpressionTracking\n    totalJobsCount\n    filterOptions\n    companiesLink\n    dataset1\n    indexablePageForSeo\n    searchQueryGuid\n    indeedCtk\n    paginationCursors {\n      pageNumber\n      cursor\n      __typename\n    }\n    companyFilterOptions {\n      id\n      shortName\n      __typename\n    }\n    serpSeoLinksVO {\n      relatedJobTitlesResults\n      topCityIdsToNameResults {\n        key\n        value\n        __typename\n      }\n      topEmployerIdsToNameResults {\n        key\n        value\n        __typename\n      }\n      searchedJobTitle\n      searchedKeyword\n      searchedLocationIdAsString\n      searchedLocationType\n      searchedLocationSeoName\n      topEmployerNameResults\n      __typename\n    }\n    jobsPageSeoData {\n      pageTitle\n      pageHeader\n      pageFooterText\n      pageMetaDescription\n      __typename\n    }\n    pageImpressionGuid\n    pageSlotId\n    relatedCompaniesLRP\n    relatedCompaniesZRP\n    relatedJobTitles\n    resourceLink\n    seoTableEnabled\n    jobListingSeoLinks {\n      linkItems {\n        position\n        url\n        __typename\n      }\n      __typename\n    }\n    jobListings {\n      jobview {\n        job {\n          descriptionFragments\n          eolHashCode\n          jobReqId\n          jobSource\n          jobTitleId\n          jobTitleText\n          listingId\n          __typename\n        }\n        jobListingAdminDetails {\n          adOrderId\n          cpcVal\n          importConfigId\n          jobListingId\n          jobSourceId\n          userEligibleForAdminJobDetails\n          __typename\n        }\n        overview {\n          id\n          name\n          shortName\n          squareLogoUrl\n          __typename\n        }\n        gaTrackerData {\n          trackingUrl\n          jobViewDisplayTimeMillis\n          requiresTracking\n          isIndeedJob\n          searchTypeCode\n          pageRequestGuid\n          isSponsoredFromJobListingHit\n          isSponsoredFromIndeed\n          __typename\n        }\n        header {\n          adOrderId\n          advertiserType\n          ageInDays\n          applyUrl\n          easyApply\n          easyApplyMethod\n          employerNameFromSearch\n          jobLink\n          jobCountryId\n          jobResultTrackingKey\n          locId\n          locationName\n          locationType\n          needsCommission\n          normalizedJobTitle\n          organic\n          payPercentile90\n          payPercentile50\n          payPercentile10\n          hourlyWagePayPercentile {\n            payPercentile90\n            payPercentile50\n            payPercentile10\n            __typename\n          }\n          rating\n          salarySource\n          sponsored\n          payPeriod\n          payCurrency\n          savedJobId\n          sgocId\n          categoryMgocId\n          urgencySignal {\n            labelKey\n            messageKey\n            normalizedCount\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',
        'variables': {
            'searchParams': {
                'keyword': employee,
                'locationId': 3,
                'locationType': 'COUNTRY',
                'numPerPage': 30,
                'pageCursor': None,
                'pageNumber': 1,
                'searchType': 'SR',
                'seoUrl': False,
                'filterParams': [
                    {
                        'filterKey': 'applicationType',
                        'values': '1',
                    }, {
                        'filterKey': 'sc.keyword',
                        'values': employee,
                    }, {
                        'filterKey': 'locT',
                        'values': 'N',
                    }, {
                        'filterKey': 'locId',
                        'values': '3',
                    },
                ]
            }
        }
    })), headers=headers)
    req = _session.prepare_request(request)
    response = _session.send(req)

    print(response.text)

# SQL
def DiccionarioSQL(Select):
    cnxn = mysql.connector.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, charset='latin1', auth_plugin='mysql_native_password')
    cursor = cnxn.cursor(buffered=True)
    cursor.execute(Select)
    cnxn.commit()
    Header, Respuesta = [column[0] for column in cursor.description], []
    for idx, Rows in enumerate(list(cursor.fetchall())) or []:
        Resultado = [x for x in Rows]
        Lista = {y: Resultado[idy] for idy, y in enumerate(Header)}
        Respuesta.append(Lista)
    cnxn.close()
    return Respuesta

def DiccionarioStore(store, values):
    cnxn = mysql.connector.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, charset='latin1', auth_plugin='mysql_native_password')
    cursor = cnxn.cursor(buffered=True)
    cursor.callproc(str(store), values)
    for result in cursor.stored_results():
        description = result.description
        fetch = result.fetchall()
    Header, Respuesta = [column[0] for column in description], []
    for idx, Rows in enumerate(list(fetch)) or []:
        Resultado = [x for x in Rows]
        Lista = {y: Resultado[idy] for idy, y in enumerate(Header)}
        Respuesta.append(Lista)
    cnxn.close()
    return Respuesta

def Execute(Update, Multi=False):
    cnxn = mysql.connector.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, auth_plugin='mysql_native_password')
    cursor = cnxn.cursor()
    cursor.execute(Update)
    cnxn.commit()
    cursor.close()
    cnxn.close()

import re
def InsertarTabla(Todo, Tabla = ''):
    if len(Todo)>0:
        Corte = 500
        SubA = DiccionarioSQL(f"SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH FROM information_schema.COLUMNS WHERE TABLE_NAME = '{Tabla}'")
        SubA = [a for a in SubA if a['COLUMN_NAME'] in Todo[0].keys()]
        def NonLatin(text): 
            return deEmojify(text.replace("'", '').replace("’", '').replace("’", '').replace("“", '').replace("”", ''))
        Residuo, Paso, Pasos = len(Todo)%Corte, 0, math.floor(len(Todo)/Corte)
        while True:
            Siguiente = Paso*Corte + (Corte if Paso!=Pasos else Residuo)
            Grupo = Todo[Paso*Corte:Siguiente]; Paso+=1;
            if Grupo == []: break;
            def Formato(a, b):
                SubB = [c for c in SubA if c['COLUMN_NAME'] == b['COLUMN_NAME']]
                b = a[b['COLUMN_NAME']] 
                if b == None or b == 'None': return 'NULL'
                if len(SubB)==0: return "'" + str(b).replace("'", "") + "'" if str(b)!='' else 'NULL'
                if SubB[0]['DATA_TYPE'] not in ('varchar','char','datetime'): return "'" + str(b).replace("'", "").replace("\\", "") + "'" if str(b)!='' else 'NULL'
                if SubB[0]['DATA_TYPE'] in ('datetime'): return "'" + str(b).replace("'", "").replace("\\", "") + "'" if str(b)!='' and str(b)!='0000-00-00 00:00:00' else 'NULL'
                return "'" + NonLatin(str(str(b)[:int(SubB[0]['CHARACTER_MAXIMUM_LENGTH'])]).replace('"', "").replace("'", "").replace("\\", "")) + "'" if str(b)!='' else 'NULL'
            Execute("INSERT INTO {0}({1}) VALUES {2};".format(Tabla, ",".join([str(a['COLUMN_NAME']) for a in SubA]), ", ".join(["({0})".format(" ,".join([Formato(a, b) for b in SubA])) for a in Grupo])))
            if Paso == Pasos+1: break
    else: pass
