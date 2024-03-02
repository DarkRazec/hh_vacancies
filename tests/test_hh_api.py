import pytest
from src.modules.HeadHunterAPI import HeadHunterAPI


@pytest.fixture
def hh_api():
    return HeadHunterAPI()


def test_hh_api(hh_api):
    assert type(hh_api.get_vacancies('', 1)[0]["name"]) == str
