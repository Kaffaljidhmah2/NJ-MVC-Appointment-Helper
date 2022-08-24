from linecache import checkcache
from posixpath import relpath
from const import MVC_URL, SERVICE_ID
import datetime
from utils import parse_response_all, gen_avail_places, parse_response_one
import requests
import time

def service_time_check(text):
    
    service_time_url = MVC_URL + SERVICE_ID[text]
    try:
        response = requests.get(service_time_url)
    except Exception:
        reply = 'Fail to connect to NJ MVC website.'
    else:
        sorted_time_list = parse_response_all(response, '331231', 3)
        reply = gen_avail_places(sorted_time_list, service_time_url, is_from_parse_one=False)
    return reply


def appt_check(text, location_id):
    service_time_url = MVC_URL + SERVICE_ID[text] + '/' + location_id
    ftime = None
    try:
        response = requests.get(service_time_url)
    except:
        reply = ('Fail to connect to NJ MVC website.')
    else:
        if location_id == '0':
            result = parse_response_all(response, '331231', 1)
            is_from_parse_one = False
        else:
            result = parse_response_one(response, '331231', location_id)
            is_from_parse_one = True
        if len(result) == 1:
            reply, ftime = gen_avail_places(result, service_time_url, is_from_parse_one)
        else:
            reply = ('No available place found.')
    return reply, ftime


def main():
    #service_time_check(init_permit)
    reply = ""
    init_permit = 'INITIAL PERMIT (NOT FOR KNOWLEDGE TEST)'
    init_permit_url = 'https://telegov.njportal.com/njmvc/AppointmentWizard/15/'
    
    ftimes = []
    for i in ['186', '194', '193', '206', '264', '200', '187']:
        reply0, ftime = appt_check(init_permit, i) 
        reply += reply0
        if ftime is not None:
            ftimes.append([ftime, i])
    
    checked=False
    for ftime, i in ftimes:
        if ftime < datetime.datetime(2022,9,30):
            print()
            print(str(ftime))
            print("\033[31m", ' Url: ', init_permit_url + i)
            print()
            checked=True 
    
    return reply, checked
    # bakers basin
    # edison # NO! 02172022
    # south plainfield # sounds good !
    # rahway
    # elizabeth
    # newark
    # bayonne

def sound():
    for t in range(5):
        print('\a')
        time.sleep(1)

if __name__ == "__main__":
    sound()
    while True:
        reply, checked = main()
        if checked:
            sound()
            print("\033[31m", 'Found! ')
        else:
            print("\033[92m", 'Nothing: ', '|'.join([x[10:15] for x in reply.split('\n')]))
        time.sleep(10)