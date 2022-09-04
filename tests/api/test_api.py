import requests


def test_api_main_endpoint():
    response = requests.get('http://127.0.0.1:8000/api/v1/')
    assert response.status_code == 200


def test_get_entry():
    portfolio_id = '00dc9d7c-fcef-4653-a3e8-2931ba5665b4'
    try:
        response = requests.get(f"http://127.0.0.1:8000/api/v1/daily-return/{portfolio_id}")
        assert response.status_code == 200
    except KeyError as e:
        return False
    except ConnectionError as e:
        return False
