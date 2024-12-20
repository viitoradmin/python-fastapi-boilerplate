import os
import requests


class ScheduerJob:
    def delete_past_events(self):
        try:
            url = f"{os.environ.get('BACKEND_URL')}v1/cap/delete/past/event"

            payload = {}
            headers = {
                "Accept": "application/json",
                "Cookie": "csrftoken=tFHOXldbBtoChLw6sKtladcULiJNz1fQUW2vu7byl9Cwrnr1H61NwydEAtQQENlw",
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)
        except Exception as e:
            print(e)