import pytest
import asyncio
import warnings
from metaTarget import ppb2_dnn_ecfp4, ppb2_nb_ecfp4, ppb2_nnmqn_nbecfp4,  ppb2_nnxfp_nbecfp4
from metaTarget import ppb2_nnnb_ecfp4, ppb2_nn_mqn, ppb2_nn_xfp, ppb2_nn_ecfp4

warnings.filterwarnings("ignore")
SMILES = "FC1=CC=C(CC2=NNC(=O)C3=CC=CC=C23)C=C1C(=O)N1CCN(CC1)C(=O)C1CC1"


@pytest.fixture(scope='module')
def setup_module(request):
    def teardown_module():
        print("teardown_module called.")

    request.addfinalizer(teardown_module)
    print('setup_module called.')


@pytest.mark.parametrize("smiles", (SMILES,))
def test_sea(setup_module, smiles):
    print('ppb2_dnn_ecfp4 called.')
    assert asyncio.run(ppb2_dnn_ecfp4(smiles)) != "{}"


if __name__ == "__main__":
    pytest.main()
