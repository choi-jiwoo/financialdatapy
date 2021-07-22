import financials
import pandas as pd

# test for Netflix
def get_filings_list(cik): 
    cik = '0001065280'
    url = f'http://data.sec.gov/submissions/CIK{cik}.json'
    data = financials.request_data(url)

    acc = data['filings']['recent']['accessionNumber']
    acc = [s.replace('-', '') for s in acc]
    form = data['filings']['recent']['form']
    filings = pd.DataFrame(zip(form, acc), columns=['AccessionNumber', 'Form'])
    latest_filing = filings[filings['AccessionNumber']=='10-K'].iloc[0].at['Form']

    return latest_filing