import asyncio
import re
import warnings

import pandas as pd
import requests
from requests.exceptions import RequestException

warnings.filterwarnings("ignore")


async def targetHunter(smile):
    # https://www.cbligand.org/TargetHunter/search_target.php

    login_url = 'https://www.cbligand.org/TargetHunter/login.php'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
              'Connection': 'close',
              }
    data = {
        'usrname': 'catkin7',
        'usrpasswd': 'y7B5@t!g',
        'btnLogin2': 'Login',
    }
    session = requests.Session()

    try:
        _ = session.post(url=login_url, data=data, headers=header, timeout=60, verify=False)
    except RequestException:
        return "{}"

    search_url = 'https://www.cbligand.org/TargetHunter/search_target.php'

    data = {
        "File1": (None, '', 'application/octet-stream'),
        "hiddensmi": (None, smile),
        "Smiles": (None, smile),
        "Fingerprint": (None, 'FP2'),
        "searchtype": (None, 'sim2d'),
        "similarity": (None, '60'),
        "ChEMBL": (None, 'on'),
        "PubChem": (None, 'on'),
        "Submit": (None, 'Submit'),
    }

    try:
        page = session.post(search_url, files=data, headers=header, timeout=60).text
    except RequestException:
        return "{}"

    patterns = re.compile('(wrk\d*)')
    try:
        wrkid = re.findall(patterns, page)[0]
    except IndexError:
        return "{}"

    result_url = 'https://www.cbligand.org/TargetHunter/retrieve_target.php?similarity=60&dir=' + wrkid + '&FP=FP2'

    try:
        result_page = session.get(result_url, headers=header, timeout=60).text
    except RequestException:
        return "{}"

    try:
        df = pd.read_html(result_page, header=0)[1]
    except ValueError:
        return "{}"

    clean_target = [x.replace('Find Assays Nearby', '') for x in df['Target']]
    df['Target'] = clean_target

    return df.T.to_json()


if __name__ == "__main__":
    _smi = "CCCCCC"
    res = asyncio.run(targetHunter(_smi))
    print(res)