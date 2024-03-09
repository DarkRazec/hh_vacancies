import pytest
from src.modules.hh_api import HeadHunterAPI


@pytest.fixture
def hh_api():
    return HeadHunterAPI()


def test_hh_api(hh_api):
    assert type(hh_api.get_vacancies('', 1, 1)[0]["name"]) == str
