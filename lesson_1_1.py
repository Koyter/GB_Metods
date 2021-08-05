import json
from pprint import pprint
import requests


def get_response(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        return response
    return None


def save_user_info(get_response):
    with open("data.json", "w") as f:
        json.dump(get_response.json(), f)


def repos(Get_response):
    UserList = []
    for i in Get_response.json():
        UserList.append(i["name"])
    return UserList


def pipeline():
    username = "Koyter"
    response = get_response(username)
    save_user_info(response)
    repos_list = repos(response)
    pprint(repos_list)


if __name__ == "__main__":
    pipeline()
