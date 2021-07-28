import requests
import re
import json
from bs4 import BeautifulSoup

# Request data from sec.gov
def request_data(url, ret):
    headers = {'User-Agent' : 'Mozilla'}
    res = requests.get(url, headers=headers)
    res_type = int(re.search('\d+', str(res)).group())
    
    if res_type == 200: 
        if ret == 'json':
            json_file = json.loads(res.text)
            return json_file
        elif ret == 'html':
            soup = BeautifulSoup(res.text, 'html.parser')
            return soup

    else:
        raise Exception(f'Request failure. Response [{res_type}]')
        quit()