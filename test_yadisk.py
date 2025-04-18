import os
import requests
import pytest
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("YANDEX_TOKEN")
BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources'
HEADERS = {'Authorization': f'OAuth {TOKEN}'}


def create_folder(folder_name):
    return requests.put(BASE_URL, headers=HEADERS, params={'path': folder_name})


def get_folder(folder_name):
    return requests.get(BASE_URL, headers=HEADERS, params={'path': folder_name})


def delete_folder(folder_name):
    return requests.delete(BASE_URL, headers=HEADERS, params={'path': folder_name, 'permanently': 'true'})


@pytest.mark.parametrize("folder_name", ["test_folder_api"])
def test_create_folder_success(folder_name):
    delete_folder(folder_name)  # Очистка
    response = create_folder(folder_name)
    assert response.status_code == 201

    check = get_folder(folder_name)
    assert check.status_code == 200
    assert check.json().get('type') == 'dir'


@pytest.mark.parametrize("folder_name", ["test_folder_api"])
def test_create_existing_folder(folder_name):
    create_folder(folder_name)
    response = create_folder(folder_name)
    assert response.status_code == 409