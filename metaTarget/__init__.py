import time

import asyncio

try:
    from .swiss import swiss
    from .targetHunter import targetHunter
    from .passOnline import passOnline
    from .sea import sea
    from .targetNet import targetNet
    from .ppb2 import *
except ImportError:
    from swiss import swiss
    from targetHunter import targetHunter
    from passOnline import passOnline
    from sea import sea
    from targetNet import targetNet
    from ppb2 import *

from pkg_resources import get_distribution

__version__ = get_distribution('meta_target').version


class MetaTarget:
    def __init__(self, smiles: str):
        self.smiles = smiles
        self.tasks = {
            "swiss": False,
            "targetHunter": False,
            "passOnline": False,
            "sea": False,
            "ppb2_dnn_ecfp4": False,
            "ppb2_nb_ecfp4": False,
            "ppb2_nnmqn_nbecfp4": False,
            "ppb2_nnxfp_nbecfp4": False,
            "ppb2_nnnb_ecfp4": False,
            "ppb2_nn_mqn": False,
            "ppb2_nn_xfp": False,
            "ppb2_nn_ecfp4": False
        }

    async def _runSwiss(self):
        res = await swiss(self.smiles)
        self.tasks["swiss"] = True
        print(self.tasks)
        return res

    async def _runTargetHunter(self):
        res = await targetHunter(self.smiles)
        self.tasks["targetHunter"] = True
        print(self.tasks)
        return res

    async def _runPassOnline(self):
        res = await passOnline(self.smiles)
        self.tasks["passOnline"] = True
        print(self.tasks)
        return res

    async def _runSea(self):
        res = await sea(self.smiles)
        self.tasks["sea"] = True
        print(self.tasks)
        return res

    # Followings are ppb2 series

    async def _run_ppb2_dnn_ecfp4(self):
        res = await ppb2_dnn_ecfp4(self.smiles)
        self.tasks["ppb2_dnn_ecfp4"] = True
        print(self.tasks)
        return res

    async def _run_ppb2_nb_ecfp4(self):
        res = await ppb2_nb_ecfp4(self.smiles)
        self.tasks["ppb2_nb_ecfp4"] = True
        print(self.tasks)
        return res

    async def _run_ppb2_nnmqn_nbecfp4(self):
        res = await ppb2_nnmqn_nbecfp4(self.smiles)
        self.tasks["ppb2_nnmqn_nbecfp4"] = True
        print(self.tasks)
        return res

    async def _run_ppb2_nnxfp_nbecfp4(self):
        res = await ppb2_nnxfp_nbecfp4(self.smiles)
        self.tasks["ppb2_nnxfp_nbecfp4"] = True
        print(self.tasks)
        return res

    async def _run_ppb2_nnnb_ecfp4(self):
        res = await ppb2_nnnb_ecfp4(self.smiles)
        self.tasks["ppb2_nnnb_ecfp4"] = True
        print(self.tasks)
        return res

    async def _run_ppb2_nn_mqn(self):
        res = await ppb2_nn_mqn(self.smiles)
        self.tasks["ppb2_nn_mqn"] = True
        print(self.tasks)
        return res

    async def _run_ppb2_nn_xfp(self):
        res = await ppb2_nn_xfp(self.smiles)
        self.tasks["ppb2_nn_xfp"] = True
        print(self.tasks)
        return res

    async def _run_ppb2_nn_ecfp4(self):
        res = await ppb2_nn_ecfp4(self.smiles)
        self.tasks["ppb2_nn_ecfp4"] = True
        print(self.tasks)
        return res

    async def run(self):
        res = await asyncio.gather(
            self._runSwiss(), self._runTargetHunter(), self._runPassOnline(),
            self._runSea(), self._run_ppb2_dnn_ecfp4(),
            # self._run_ppb2_nb_ecfp4(), self._run_ppb2_nnmqn_nbecfp4(),
            # self._run_ppb2_nnxfp_nbecfp4(), self._run_ppb2_nnnb_ecfp4(),
            # self._run_ppb2_nn_mqn(), self._run_ppb2_nn_xfp(),
            # self._run_ppb2_nn_ecfp4()
        )
        return res


if __name__ == "__main__":
    _smi = "CCCCCC"

    metaTarget = MetaTarget(_smi)
    _res = asyncio.run(metaTarget.run())
    print(_res)
