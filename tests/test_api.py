import json
import time

import requests

API = 'http://127.0.0.1:8080'


def test_create_user():
    user_data = {'name': f'test_create_user{time.time()}', 'password': 'pass_ex'}
    response = requests.post(f'{API}/user/create/', json=user_data)
    assert response.status_code == 200


def test_get_ads(create_ads):

    response = requests.get(f'{API}/ads/{create_ads["id"]}')
    assert response.status_code == 200
    assert response.json()['heading'] == create_ads['heading']


def test_get_ads_not_found(create_ads):
    response = requests.get(f'{API}/ads/99999')
    assert response.status_code == 404
    assert response.json() == {'status': 'error', 'descriptions': 'user not found'}


def test_create_ads():
    ads_data = {'heading': f'test_create{time.time()}', 'description': 'desc_ex', 'user_id': 1}
    response = requests.post(f'{API}/ads/', json=ads_data)
    assert response.status_code == 200


def test_patch_ads(create_ads):
    patch_data = {'heading': 'patch_heading'}
    response = requests.patch(f'{API}/ads/{create_ads["id"]}', json=patch_data)
    assert response.status_code == 200
    assert response.json()['heading'] == patch_data['heading']

    response = requests.get(f'{API}/ads/{create_ads["id"]}')
    assert response.status_code == 200
    assert response.json()['heading'] == patch_data['heading']


def test_delete_ads(create_ads):
    response = requests.delete(f'{API}/ads/{create_ads["id"]}')
    assert response.status_code == 200
    assert response.json() == {'status': 'delete'}

    response = requests.get(f'{API}/ads/{create_ads["id"]}')
    assert response.status_code == 404


