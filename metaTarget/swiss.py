import requests

import time
import re
import pandas as pd

try:
    from .utils import retry
except ImportError:
    from utils import retry

import asyncio
from requests.exceptions import RequestException


@retry(maxAttemptTimes=3)
async def swiss(smile):
    # http://www.swisstargetprediction.ch/

    start_url = 'http://www.swisstargetprediction.ch/predict.php'
    s = requests.session()
    body = {"organism": 'Homo_sapiens', "smiles": smile, "Example": ""}

    try:
        response = s.post(start_url, data=body, timeout=60)
    except RequestException:
        return "{}"

    patterns = re.compile('location.replace\("(.*?)"\);')
    try:
        x = re.findall(patterns,response.text)[0]
    except IndexError:
        return "{}"

    result_url = 'http://www.swisstargetprediction.ch/'+x
    await asyncio.sleep(15)

    try:
        page = s.get(result_url,timeout=60).text
    except RequestException:
        return "{}"

    try:
        df = pd.read_html(page,header=0)[0]
    except ValueError:
        return "{}"

    clean_actives = [x.replace(' &nbsp','') for x in df['Known actives (3D/2D)']]
    df['Known actives (3D/2D)'] = clean_actives

    return df.T.to_json()


if __name__ == "__main__":
    _smi = "CCCCCC"
    res = asyncio.run(swiss(_smi))
    print(res)
