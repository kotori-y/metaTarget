import asyncio

import pandas as pd
import requests
from requests.exceptions import RequestException

try:
    from .utils import retry
except ImportError:
    from utils import retry

__all__ = [
    "ppb2_nn_ecfp4", "ppb2_dnn_ecfp4", "ppb2_nnnb_ecfp4",
    "ppb2_nnmqn_nbecfp4", "ppb2_nnxfp_nbecfp4", "ppb2_nn_xfp",
    "ppb2_nn_mqn", "ppb2_nb_ecfp4"
]

class PPBTwo:
    def __init__(self, smiles: str, method: str):
        assert method in [
            "NN(ECfp4)", "NN(Xfp)", "NN(MQN)",
            "NN(ECfp4) + NB(ECfp4)", "NN(Xfp) + NB(ECfp4)",
            "NN(MQN) + NB(ECfp4)", "NB(ECfp4)", "DNN(ECfp4)"
        ]

        self.smiles = smiles
        self.method = method

        self.hashTable = {
            "NN(ECfp4)": {
                "smi": self.smiles, "fp": "ECfp4",
                "method": "Sim", "scoringmethod": "TANIMOTO"
            },

            "NN(Xfp)": {
                "smi": self.smiles, "fp": "Xfp",
                "method": "Sim", "scoringmethod": "CBD"
            },

            "NN(MQN)": {
                "smi": self.smiles, "fp": "MQN",
                "method": "Sim", "scoringmethod": "CBD"
            },

            "NN(ECfp4) + NB(ECfp4)": {
                "smi": self.smiles, "fp": "ECfp4",
                "method": "SimPlusNaiveBayes", "scoringmethod": "TANIMOTO"
            },

            "NN(Xfp) + NB(ECfp4)": {
                "smi": self.smiles, "fp": "Xfp",
                "method": "SimPlusNaiveBayes", "scoringmethod": "CBD"
            },

            "NN(MQN) + NB(ECfp4)": {
                "smi": self.smiles, "fp": "MQN",
                "method": "SimPlusNaiveBayes", "scoringmethod": "CBD"
            },

            "NB(ECfp4)": {
                "smi": self.smiles, "fp": "ECfp4",
                "method": "NaiveBayes", "scoringmethod": "CBD"
            },

            "DNN(ECfp4)": {
                "smi": self.smiles, "fp": "ECfp4",
                "method": "DNN", "scoringmethod": "TANIMOTO"
            }

        }

    async def predict(self):
        session: requests.Session = requests.Session()
        requestUrl = "https://ppb2.gdb.tools/predict"
        headers = {
            "User-Agent": "Mozilla / 5.0(Macintosh; Intel Mac OS X 10.15; rv: 90.0) Gecko / 20100101 Firefox / 90.0"
        }

        params = self.hashTable[self.method]

        try:
            response = session.get(requestUrl, params=params, timeout=300, headers=headers)
        except RequestException:
            return "{}"

        try:
            df = pd.read_html(response.text, header=0)[1]
        except ValueError:
            return "{}"

        df.columns = ['Rank', 'ChEMBL ID', 'Common name', 'Method_ID']
        df['Method_ID'] = self.method

        return df.T.to_json()


# @retry(maxAttemptTimes=1)
async def ppb2_dnn_ecfp4(smiles: str):
    spider: PPBTwo = PPBTwo(smiles, "DNN(ECfp4)")
    return await spider.predict()


# @retry(maxAttemptTimes=1)
async def ppb2_nb_ecfp4(smiles: str):
    spider: PPBTwo = PPBTwo(smiles, "NB(ECfp4)")
    return await spider.predict()


# @retry(maxAttemptTimes=1)
async def ppb2_nnmqn_nbecfp4(smiles: str):
    spider: PPBTwo = PPBTwo(smiles, "NN(MQN) + NB(ECfp4)")
    return await spider.predict()


# @retry(maxAttemptTimes=1)
async def ppb2_nnxfp_nbecfp4(smiles: str):
    spider: PPBTwo = PPBTwo(smiles, "NN(Xfp) + NB(ECfp4)")
    return await spider.predict()


# @retry(maxAttemptTimes=1)
async def ppb2_nnnb_ecfp4(smiles: str):
    spider: PPBTwo = PPBTwo(smiles, "NN(ECfp4) + NB(ECfp4)")
    return await spider.predict()


# @retry(maxAttemptTimes=1)
async def ppb2_nn_mqn(smiles: str):
    spider: PPBTwo = PPBTwo(smiles, "NN(MQN)")
    return await spider.predict()


# @retry(maxAttemptTimes=1)
async def ppb2_nn_xfp(smiles: str):
    spider: PPBTwo = PPBTwo(smiles, "NN(Xfp)")
    return await spider.predict()


# @retry(maxAttemptTimes=1)
async def ppb2_nn_ecfp4(smiles: str):
    spider: PPBTwo = PPBTwo(smiles, "NN(ECfp4)")
    return await spider.predict()


if __name__ == "__main__":
    _smi = "Cc4cccc(C3CCC(N2CCN(c1cccnc1)CC2)CC3)c4"


    async def foobar():
        return await asyncio.gather(
            ppb2_dnn_ecfp4(_smi), ppb2_nb_ecfp4(_smi), ppb2_nnmqn_nbecfp4(_smi),
            ppb2_nnxfp_nbecfp4(_smi), ppb2_nnnb_ecfp4(_smi), ppb2_nn_mqn(_smi),
            ppb2_nn_xfp(_smi), ppb2_nn_ecfp4(_smi)
        )


    res = asyncio.run(foobar())
    print(res)