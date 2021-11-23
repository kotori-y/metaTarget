import asyncio
import json

import pandas as pd
import requests
from requests.exceptions import RequestException


async def targetNet(smile: str) -> json:
    url = "http://targetnet.scbdd.com/calcnet/calc_ensemble_text/"
    data = {
        "smile": (None, smile),
        "finger_type": (None, "BaseInfo_daylight", "BaseInfo_ecfp4")
    }

    try:
        resp = requests.post(url, data=data)
    except RequestException:
        return "{}"

    try:
        out = pd.read_html(resp.text)[0]
    except ValueError:
        return "{}"

    return out.T.to_json()


if __name__ == "__main__":
    _smi = "C(C=CC1)=C(C=1C(=O)O)O"
    res = asyncio.run(targetNet(_smi))