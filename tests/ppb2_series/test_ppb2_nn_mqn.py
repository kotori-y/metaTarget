import asyncio
import warnings

import pytest

from metaTarget import ppb2_nn_mqn

warnings.filterwarnings("ignore")
SMILES = "FC1=CC=C(CC2=NNC(=O)C3=CC=CC=C23)C=C1C(=O)N1CCN(CC1)C(=O)C1CC1"


@pytest.fixture(scope='module')
def setup_module(request):
    def teardown_module():
        print("teardown_module called.")

    request.addfinalizer(teardown_module)
    print('setup_module called.')


@pytest.mark.parametrize("smiles", (SMILES,))
def test_ppb2_nn_mqn(setup_module, smiles):
    print('ppb2_nn_mqn called.')
    assert asyncio.run(ppb2_nn_mqn(smiles)) != "{}"


if __name__ == "__main__":
    pytest.main()
