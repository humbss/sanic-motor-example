import pytest
import requests
import json

@pytest.fixture
def server_url():
    return "http://localhost:8000"

def get_header():
    return {
        'Content-Type': "application/json",
        'User-Agent': "PostmanRuntime/7.15.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

def test_post_user(server_url):
    url = server_url + "/user/"
    payload = {"first":"Sanic","last":"Master"}
    resp = requests.post(url, data=json.dumps(payload,indent=4), headers=get_header())
    assert resp.status_code == 200
    assert resp.status_code == 200,resp.text
    return json.loads(resp.text)['id']['body']
    
def test_get_user(server_url):
    testObjectId = test_post_user(server_url)
    url = server_url + "/user/" + str(testObjectId)
    resp = requests.get(url, headers=get_header())
    assert resp.status_code == 200
    assert resp,resp.text