import json
import requests

# test for Apple Inc.
cik = '0000320193'
url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

res = requests.get(url, headers=headers)
f = json.loads(res.text)
with open('financial_statement.json', 'w') as fs:
    fs.write(f)