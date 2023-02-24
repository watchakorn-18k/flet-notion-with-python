import requests
import json
import os


def connectdb() -> str:
    with open("token.json", "r") as f:
        json_data = json.loads(f.read())

    token = json_data["token"]

    databaseId = "abc69f13662d4c3dbda6053da5555b8c"

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
    }
    return databaseId, headers
