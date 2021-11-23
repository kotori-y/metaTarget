import asyncio

import pandas as pd
import requests
from requests.exceptions import RequestException

from utils import retry


@retry(maxAttemptTimes=3)
async def passOnline(smiles: str):
    # http://www.pharmaexpert.ru/passonline/predict.php

    try:
        session: requests.Session = requests.Session()

        loginUrl = 'http://way2drug.com/passonline/predict.php'
        loginData = {
            'user_login': 'cenuswei',
            'user_password': 'f353630039',
        }
        _ = session.post(url=loginUrl, data=loginData, timeout=60)

        predictUrl = "http://way2drug.com/passonline/result_id.php"
        predictData = {'smi': smiles}
        resIndex = session.post(predictUrl, data=predictData, timeout=20).text.strip()

        resUrl = f"http://way2drug.com/passonline/pred1.php?id_task={resIndex}"

        attempt = 1
        result = session.get(resUrl, timeout=60).text
        while 'automatically updated every 10 seconds' in result and attempt <= 3:
            await asyncio.sleep(10)
            attempt += 1
            result = session.get(resUrl, timeout=60).text

        try:
            df = pd.read_html(result, header=0, thousands=None)[0]
        except ValueError:
            return pd.DataFrame()

        df.columns = ['Probability to be active', 'Probability to be inactive', 'Biological Activity']

    except RequestException:
        df = pd.DataFrame()

    return df.to_json()


if __name__ == "__main__":
    _smi = "CCCCCC"
    test = asyncio.run(passOnline(_smi))
    print("DONE")
