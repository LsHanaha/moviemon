import requests
import json


def main():
    API_KEY = "4279563e"
    URL = f"http://www.omdbapi.com/?apikey={API_KEY}"
    FILMS = ["tt8362852", "tt0065163", "tt0120616", "tt0034398", "tt3120314",
             "tt0367677", "tt1594913", "tt5884052", "tt1572315", "tt0329101"]
    data = {}
    for film in FILMS:
        params = {
            "i": film
        }
        try:
            res = requests.get(URL, params=params)
            res.raise_for_status()
        except requests.HTTPError as e:
            return print(e)
        try:
            data[film] = json.loads(res.text)
        except json.decoder.JSONDecodeError as e:
            raise print(e)
    return data


if __name__ == "__main__":
    main()