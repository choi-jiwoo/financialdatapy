import requests
import json
from bs4 import BeautifulSoup

# Request data from sec.gov
def request_data(url, ret):
    headers = {'User-Agent' : 'Mozilla'}
    res = requests.get(url, headers=headers)
    
    if res.ok: 
        if ret == 'json':
            json_file = json.loads(res.text)
            return json_file
        elif ret == 'html':
            soup = BeautifulSoup(res.text, 'html.parser')
            return soup
    else:
        raise Exception(f'Bad response')