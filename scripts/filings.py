import requests
import json
import pandas as pd

# test for Netflix
cik = '0001065280'
url = f'http://data.sec.gov/submissions/CIK{cik}.json'
headers = {'User-Agent' : 'Mozilla'}

s = requests.get(url, headers)
submission = json.loads(s.text)

acc = submission['filings']['recent']['accessionNumber']
acc = [s.replace('-', '') for s in acc]
form = submission['filings']['recent']['form']
filings = pd.DataFrame(zip(form, acc), columns=['AccessionNumber', 'Form'])
latest_filing = filings[filings['AccessionNumber']=='10-K'].iloc[0].at['Form']