import requests
import json
import pandas as pd

def get_cik(url):
    res = requests.get(url)
    data = json.loads(res.text)

    cik_list = pd.DataFrame(data['data'], columns=data['fields'])
    # uniform company names
    cik_list['name'] = cik_list['name'].str.lower().str.title()

    return cik_list