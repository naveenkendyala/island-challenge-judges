import os
import requests
import csv
import time


cluster_domain = os.environ.get('CLUSTERDOMAIN', '')
token = os.environ.get('JUDGE_SA_TOKEN', '')

PLAYER_COUNT = 100
PASSWORDS = []
successful_flags = []

def checkReplicas(player):
    # Define your OpenShift API server URL, namespace, resource type, and resource name
    api_server_url = f'https://api.{cluster_domain}:6443'
    namespace = f'player{player}'
    resource_type = 'deployments'  # Change to 'replicasets' for ReplicaSets
    resource_name = 'hello'

    # Construct the API endpoint URL
    url = f'{api_server_url}/apis/apps/v1/namespaces/{namespace}/{resource_type}/{resource_name}'
    print(f'url: {url}')

    # Set up the headers with the authentication token
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Send a GET request to the API server
    response = requests.get(url, headers=headers, verify=False)  # Use verify=False for self-signed certificates

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        replicas = data['spec']['replicas']
        print(f'Number of Replicas for {resource_type.capitalize()}: {replicas}')
    else:
        replicas = 0
        print(f'No replicas found for hello deployment. Status code: {response.status_code}')

    return replicas


def submit_flag(player, challenge, flag):
    time.sleep(10)
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

def monkeyBusinessChecker():

    for i in range(1, PLAYER_COUNT + 1):
        try:
            if i not in successful_flags:
                replicas = checkReplicas(i)
                if replicas >= 2:
                    submit_flag(i, 10, "FLAG_MONKEY_BUSINESS_99")
                    successful_flags.append(i) 

                else:
                    print("Hello deployment not found. Skipping Flag submission")
            else:
                print(f"Flag for player{i} already submitted." )
        except requests.RequestException as err:
            print("error:", err)


def main():

    global PASSWORDS
    with open("credentials.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            PASSWORDS.append(row[1])

    while True:
        monkeyBusinessChecker()
        time.sleep(30)

if __name__ == "__main__":
    main()
