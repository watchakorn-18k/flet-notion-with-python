import requests
import json
import ctypes


def connectdb() -> str:
    try:
        with open("token.json", "r") as f:
            json_data = json.loads(f.read())
            token = json_data["token"]
    except:
        with open("token.json", "w") as f:
            f.write(
                """{
    "token": ""
}"""
            )
            if (
                ctypes.windll.user32.MessageBoxW(
                    0, "Please add token token.json", "Token Error!", 16
                )
                == 1
            ):
                import sys

                sys.exit()
    with open("token.json", "r") as f:
        json_data = json.loads(f.read())
        if json_data["token"] == "":
            if (
                ctypes.windll.user32.MessageBoxW(
                    0, "Please add token in token.json", "Token Error!", 16
                )
                == 1
            ):
                import sys

                sys.exit()

    databaseId = "abc69f13662d4c3dbda6053da5555b8c"

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
    }
    return databaseId, headers
