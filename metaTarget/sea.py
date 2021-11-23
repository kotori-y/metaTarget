import asyncio
import json

import requests
import pandas as pd

from utils import retry

from lxml import etree


@retry(maxAttemptTimes=3)
async def sea(smiles: str) -> json:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.99 Safari/537.36'
    }

    session = requests.Session()

    url = "https://sea.bkslab.org/"
    resp = session.get(url)
    tree = etree.HTML(resp.text)
    token = tree.xpath('//*[@id="csrf_token"]/@value')[0]

    start_url = 'https://sea.bkslab.org/search'

    data = {
        'csrf_token': token,
        'ref_type': 'library',
        'ref_library_id': 'default',
        'query_type': 'custom',
        'query_custom_targets_paste': smiles,  # Mol
    }

    response = session.post(url=start_url, headers=headers, data=data)
    page = session.get(response.url).text

    attempt = 0
    while 'pending' in page:
        await asyncio.sleep(15)
        page = session.get(response.url).text
        attempt += 1
        if attempt == 5:
            return json.dumps({})
    try:
        df: pd.DataFrame = pd.read_html(page)[0].dropna(axis=0)
    except ValueError:
        df: pd.DataFrame = pd.DataFrame()

    return df.T.to_json()


if __name__ == "__main__":
    _smiles: str = "CCCCCC"
    res = asyncio.run(sea(_smiles))
    print("DONE")
