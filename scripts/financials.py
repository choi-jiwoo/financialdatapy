import pandas as pd
import yaml
from scripts import request


def get_std_financials(ticker: str, financial_statement: str) -> pd.DataFrame:
    """Get standardized financials of a company.

    Args:
        ticker (str): company ticker
        financial_statement (str): which financial statement to receive

    Returns:
        pd.DataFrame: [description]
    """
    with open('config/config.yml', 'r') as f:
        config = yaml.safe_load(f)

    api_key = config['user']['financialmodelingprep_api_key']
    base_url = 'https://financialmodelingprep.com/api/v3/'
    param = f'{financial_statement}/{ticker}?limit=120&apikey={api_key}'
    url = base_url + param

    data = request.request_data(url, 'json')
    df = pd.DataFrame(data)
    new_name = [
        ''.join(map(lambda y: y if y.islower() else ' '+y, x)).capitalize()
        for x
        in df.index
    ]
    df.index = new_name
    df = df.rename(
        index={
            'Epsdiluted': 'Eps diluted',
            'Ebitdaratio': 'Ebitda ratio'
        }
    )
    # columns 0~5 : filing info
    # last two columns : filing url
    start_pos = 6
    end_pos = -2
    financial_data = df.iloc[:, start_pos:end_pos].T
    financial_data.columns = df['date'].values

    return financial_data
