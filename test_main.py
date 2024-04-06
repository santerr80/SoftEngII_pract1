from fastapi.testclient import TestClient
from main import app
import pandas as pd

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "TapexTokenizer"}


def test_create_upload_file():
    with open('countries.csv', 'rb') as f:
        response = client.post("/uploadfile/", files={"file": f})

    assert response.status_code == 200
    assert response.json()["filename"] == "countries.csv"
    df = pd.read_csv('countries.csv', encoding='utf-8', sep=';')
    assert response.json()["dataframe"] == df.to_json()


def test_create_request():
    response = client.post("/request_create/", json={"my_request":
                           "test_request"})

    assert response.status_code == 200
    assert response.json() == {"Request": "my_request"}


# def test_tokenize():
#     df = pd.read_csv('countries.csv', encoding='utf-8', sep=';')
#     my_request = "Get me most small country"
#     response = client.post("/tokenize/", json={"df": df.to_json(),
#                            "my_request": my_request})
#     assert response.status_code == 200
#     assert response.json()["response"] == " belarus"
