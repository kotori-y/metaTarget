import asyncio
import warnings

import pytest

from metaTarget import swiss

warnings.filterwarnings("ignore")
SMILES = "FC1=CC=C(CC2=NNC(=O)C3=CC=CC=C23)C=C1C(=O)N1CCN(CC1)C(=O)C1CC1"


@pytest.fixture(scope='module')
def setup_module(request):
    def teardown_module():
        print("teardown_module called.")

    request.addfinalizer(teardown_module)
    print('setup_module called.')


@pytest.mark.parametrize("smiles", (SMILES,))
def test_swiss(setup_module, smiles):
    print('swiss called.')
    assert asyncio.run(swiss(smiles)) != "{}"


if __name__ == "__main__":
    pytest.main()
