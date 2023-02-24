import json

from datetime import datetime, timezone, timedelta

with open("db.json", "r", encoding="utf8") as f:
    json_data = json.loads(f.read())


def get_money() -> list:
    list_tmp = []
    for i in json_data["results"]:
        if len(i["properties"].keys()) != 1:
            list_tmp.append(i["properties"]["income"]["number"])
    return list_tmp


def get_list_name() -> list:
    list_temp = []
    for i in json_data["results"]:
        if len(i["properties"]["client-name"]["title"]) != 0:
            list_temp.append(
                i["properties"]["client-name"]["title"][0]["text"]["content"]
            )
    return list_temp


def get_list_all() -> list:
    list_temp = []
    for i in json_data["results"]:
        utc_dt = datetime.fromisoformat(i["created_time"].replace("Z", "+00:00"))
        local_tz = timezone(timedelta(hours=7))  # adjust hours as needed
        local_dt = utc_dt.astimezone(local_tz)
        if (
            len(i["properties"]["client-name"]["title"]) != 0
            and len(i["properties"].keys()) != 1
        ):
            list_temp.append(
                [
                    i["properties"]["client-name"]["title"][0]["text"]["content"],
                    i["properties"]["income"]["number"],
                    local_dt,
                ]
            )

    return list_temp


# print(get_money())
