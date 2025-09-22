import os
import requests
import csv
import time


cluster_domain = os.environ.get('CLUSTERDOMAIN', '')

PLAYER_COUNT = 100
PASSWORDS = []
successful_flags = []
successful_flags_2 = []


def get_username(player):
    URL = f"https://island-ctfd.apps.{cluster_domain}"
    username = "admin"
    password = "redhat123"

    s = requests.session()
    s.headers.update({"User-Agent": "curl/7.67.0"})

    # Grab a nonce
    r = s.get(f"{URL}/login")
    print(r)
    if r.status_code != 200:
        raise Exception(
            f"Received status code {r.status_code} from login get"
        )

    # Parse the nonce
    nonce = r.text.split('name="nonce" type="hidden" value="')[1].split('"')[0]

    # Attempt authentication
    r = s.post(
        f"{URL}/login",
        data={"name": username, "password": password, "nonce": nonce},
    )
    if r.status_code != 200:
        raise Exception(
            f"received status code {r.status_code} from login post"
        )

    r = s.get(f"{URL}/api/v1/users/{player+1}")
    return (r.json()['data']['name'])


def submit_flag(player, challenge, flag):
    time.sleep(1)
    URL = f"https://island-ctfd.apps.{cluster_domain}"
    username = get_username(player)
    password = PASSWORDS[player]

    s = requests.session()
    s.headers.update({"User-Agent": "curl/7.67.0"})

    # Grab a nonce
    r = s.get(f"{URL}/login")
    if r.status_code != 200:
        raise Exception(
            f"Received status code {r.status_code} from login get"
        )

    # Parse the nonce
    nonce = r.text.split('name="nonce" type="hidden" value="')[1].split('"')[0]

    # Attempt authentication
    r = s.post(
        f"{URL}/login",
        data={"name": username, "password": password, "nonce": nonce},
    )
    if r.status_code != 200:
        raise Exception(
            f"received status code {r.status_code} from login post"
        )

    # Grab the CSRF token
    csrf_token = r.text.split("csrfNonce': \"")[1].split('"')[0]

    # Save requests session
    session = s

    # Get user profile
    r = session.get(f"{URL}/api/v1/users/me")
    if r.status_code != 200:
        raise RuntimeError(f"failed to retrieve profile")

    data = r.json()["data"]

    r = session.post(
        f"{URL}/api/v1/challenges/attempt",
        json={"challenge_id": challenge, "submission": flag},
        headers={"CSRF-Token": csrf_token},
    )
    if r.status_code != 200:
        raise RuntimeError("failed to submit flag")

    # Check if it was right
    print(r.json()["data"])


def hello_world():

    for i in range(1, PLAYER_COUNT + 1):
        if i not in successful_flags:
            time.sleep(0.1)
            url = f"https://hello-player{i}.apps.{cluster_domain}/"
            print(url)
            try:
                response = requests.get(url).text.strip()
                if response == "Hello World":
                    submit_flag(i, 4, "FLAG_HELLO_99")
                    successful_flags.append(i)

            except requests.RequestException as err:
                print("error:", err)
        else:
            print(f"Flag for player{i} already submitted." )


def bonjour_monde():

    for i in range(1, PLAYER_COUNT + 1):
        if i not in successful_flags_2:
            time.sleep(0.1)
            url = f"https://hello-player{i}.apps.{cluster_domain}/"
            print(url)
            try:
                response = requests.get(url).text.strip()
                if response == "Bonjour Monde":
                    submit_flag(i, 5, "FLAG_BONJOUR_99")
                    successful_flags_2.append(i)
                    
            except requests.RequestException as err:
                print("error:", err)
        else:
            print(f"Flag for player{i} already submitted." )

def main():

    global PASSWORDS
    with open("credentials.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            PASSWORDS.append(row[1])

    while True:
        print("Hello World check...")
        hello_world()
        print("Bonjour Monde check...")
        bonjour_monde()

if __name__ == "__main__":
    main()
