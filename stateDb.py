import requests
import json
from connect import connectdb


databaseId, headers = connectdb()


def readDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    # print(res.status_code)
    # print(res.text)

    with open("./db.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)


def writeDatabase(income_number: int, client_name: str):
    createUrl = "https://api.notion.com/v1/pages"

    newPageData = {
        "parent": {"database_id": databaseId},
        "properties": {
            "income": {"id": "lOMn", "type": "number", "number": int(income_number)},
            "client-name": {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {"content": str(client_name), "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": str(client_name),
                        "href": None,
                    }
                ],
            },
        },
    }

    data = json.dumps(newPageData)
    # print(str(uploadData))

    res = requests.request("POST", createUrl, headers=headers, data=data)
