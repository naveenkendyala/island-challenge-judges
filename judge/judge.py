import configparser
import requests
import time
import csv
import concurrent.futures
import random
from kubernetes import client, config

PASSWORDS = []

config_parser = configparser.ConfigParser()
config_parser.read('settings.ini')

PLAYER_COUNT = 100
MAX_THREADS = 16

morse_messages = {
    "ROOM SERVICE? ORDERED COCONUTS 3 DAYS AGO.",
    "SEND PIZZA. TIRED OF COCONUTS.",
    "YOUR UBER IS ARRIVING NOW. JUST KIDDING.",
    "SEND SUNSCREEN.",
    "FORGOT CHARGER. ANY SPARES?",
    "404: BEACH NOT FOUND. PLEASE REDIRECT.",
    "HELP! MISSING WIFI CODE!",
    "THE FLAG CODE IS: CONTAINERS"
}

morse_dict = {
    "!":"-.-.--",
    "$":"...-..-",
    "&":".-...",
    "'":".----.",
    "(":"-.--.",
    ")":"-.--.-",
    "+":".-.-.",
    "-":"-....-",
    ".":".-.-.-",
    "/":"-..-.",
    "0":"-----",
    "1":".----",
    "2":"..---",
    "3":"...--",
    "4":"....-",
    "5":".....",
    "6":"-....",
    "7":"--...",
    "8":"---..",
    "9":"----.",
    ":":"---...",
    ";":"-.-.-.",
    "=":"-...-",
    "?":"..--..",
    "@":".--.-.",
    "A":".-",
    "B":"-...",
    "C":"-.-.",
    "D":"-..",
    "E":".",
    "F":"..-.",
    "G":"--.",
    "H":"....",
    "I":"..",
    "J":".---",
    "K":"-.-",
    "L":".-..",
    "M":"--",
    "N":"-.",
    "O":"---",
    "P":".--.",
    "Q":"--.-",
    "R":".-.",
    "S":"...",
    "T":"-",
    "U":"..-",
    "V":"...-",
    "W":".--",
    "X":"-..-",
    "Y":"-.--",
    "Z":"--..",
    "_":"..--.-",
    " ":"/"
}

bottle_message = [ "                                                                                                                                                                                                                                                                                                                                                                                                                      ",
                   "                                                                                                                                                                                            dddddddd                                                                                                                                                                                                                  ",
                   "TTTTTTTTTTTTTTTTTTTTTTThhhhhhh                                         ffffffffffffffff  lllllll                                                                                            d::::::d                           iiii                                GGGGGGGGGGGGG                  lllllll                                                                                                             ",
                   "T:::::::::::::::::::::Th:::::h                                        f::::::::::::::::f l:::::l                                                                                            d::::::d                          i::::i                            GGG::::::::::::G                  l:::::l                                                                                                             ",
                   "T:::::::::::::::::::::Th:::::h                                       f::::::::::::::::::fl:::::l                                                                                            d::::::d                           iiii                           GG:::::::::::::::G                  l:::::l                                                                                                             ",
                   "T:::::TT:::::::TT:::::Th:::::h                                       f::::::fffffff:::::fl:::::l                                                                                            d:::::d                                                          G:::::GGGGGGGG::::G                  l:::::l                                                                                                             ",
                   "TTTTTT  T:::::T  TTTTTT h::::h hhhhh           eeeeeeeeeeee          f:::::f       ffffff l::::l   aaaaaaaaaaaaa     ggggggggg   ggggg         cccccccccccccccc   ooooooooooo       ddddddddd:::::d     eeeeeeeeeeee         iiiiiii     ssssssssss         G:::::G       GGGGGG  aaaaaaaaaaaaa    l::::l   aaaaaaaaaaaaa  ppppp   ppppppppp     aaaaaaaaaaaaa     ggggggggg   ggggg   ooooooooooo       ssssssssss   ",
                   "        T:::::T         h::::hh:::::hhh      ee::::::::::::ee        f:::::f              l::::l   a::::::::::::a   g:::::::::ggg::::g       cc:::::::::::::::c oo:::::::::::oo   dd::::::::::::::d   ee::::::::::::ee       i:::::i   ss::::::::::s       G:::::G                a::::::::::::a   l::::l   a::::::::::::a p::::ppp:::::::::p    a::::::::::::a   g:::::::::ggg::::g oo:::::::::::oo   ss::::::::::s  ",
                   "        T:::::T         h::::::::::::::hh   e::::::eeeee:::::ee     f:::::::ffffff        l::::l   aaaaaaaaa:::::a g:::::::::::::::::g      c:::::::::::::::::co:::::::::::::::o d::::::::::::::::d  e::::::eeeee:::::ee      i::::i ss:::::::::::::s      G:::::G                aaaaaaaaa:::::a  l::::l   aaaaaaaaa:::::ap:::::::::::::::::p   aaaaaaaaa:::::a g:::::::::::::::::go:::::::::::::::oss:::::::::::::s ",
                   "        T:::::T         h:::::::hhh::::::h e::::::e     e:::::e     f::::::::::::f        l::::l            a::::ag::::::ggggg::::::gg     c:::::::cccccc:::::co:::::ooooo:::::od:::::::ddddd:::::d e::::::e     e:::::e      i::::i s::::::ssss:::::s     G:::::G    GGGGGGGGGG           a::::a  l::::l            a::::app::::::ppppp::::::p           a::::ag::::::ggggg::::::ggo:::::ooooo:::::os::::::ssss:::::s",
                   "        T:::::T         h::::::h   h::::::he:::::::eeeee::::::e     f::::::::::::f        l::::l     aaaaaaa:::::ag:::::g     g:::::g      c::::::c     ccccccco::::o     o::::od::::::d    d:::::d e:::::::eeeee::::::e      i::::i  s:::::s  ssssss      G:::::G    G::::::::G    aaaaaaa:::::a  l::::l     aaaaaaa:::::a p:::::p     p:::::p    aaaaaaa:::::ag:::::g     g:::::g o::::o     o::::o s:::::s  ssssss ",
                   "        T:::::T         h:::::h     h:::::he:::::::::::::::::e      f:::::::ffffff        l::::l   aa::::::::::::ag:::::g     g:::::g      c:::::c             o::::o     o::::od:::::d     d:::::d e:::::::::::::::::e       i::::i    s::::::s           G:::::G    GGGGG::::G  aa::::::::::::a  l::::l   aa::::::::::::a p:::::p     p:::::p  aa::::::::::::ag:::::g     g:::::g o::::o     o::::o   s::::::s      ",
                   "        T:::::T         h:::::h     h:::::he::::::eeeeeeeeeee        f:::::f              l::::l  a::::aaaa::::::ag:::::g     g:::::g      c:::::c             o::::o     o::::od:::::d     d:::::d e::::::eeeeeeeeeee        i::::i       s::::::s        G:::::G        G::::G a::::aaaa::::::a  l::::l  a::::aaaa::::::a p:::::p     p:::::p a::::aaaa::::::ag:::::g     g:::::g o::::o     o::::o      s::::::s   ",
                   "        T:::::T         h:::::h     h:::::he:::::::e                 f:::::f              l::::l a::::a    a:::::ag::::::g    g:::::g      c::::::c     ccccccco::::o     o::::od:::::d     d:::::d e:::::::e                 i::::i ssssss   s:::::s       G:::::G       G::::Ga::::a    a:::::a  l::::l a::::a    a:::::a p:::::p    p::::::pa::::a    a:::::ag::::::g    g:::::g o::::o     o::::ossssss   s:::::s ",
                   "      TT:::::::TT       h:::::h     h:::::he::::::::e               f:::::::f            l::::::la::::a    a:::::ag:::::::ggggg:::::g      c:::::::cccccc:::::co:::::ooooo:::::od::::::ddddd::::::dde::::::::e               i::::::is:::::ssss::::::s       G:::::GGGGGGGG::::Ga::::a    a:::::a l::::::la::::a    a:::::a p:::::ppppp:::::::pa::::a    a:::::ag:::::::ggggg:::::g o:::::ooooo:::::os:::::ssss::::::s",
                   "      T:::::::::T       h:::::h     h:::::h e::::::::eeeeeeee       f:::::::f            l::::::la:::::aaaa::::::a g::::::::::::::::g       c:::::::::::::::::co:::::::::::::::o d:::::::::::::::::d e::::::::eeeeeeee       i::::::is::::::::::::::s         GG:::::::::::::::Ga:::::aaaa::::::a l::::::la:::::aaaa::::::a p::::::::::::::::p a:::::aaaa::::::a g::::::::::::::::g o:::::::::::::::os::::::::::::::s ",
                   "      T:::::::::T       h:::::h     h:::::h  ee:::::::::::::e       f:::::::f            l::::::l a::::::::::aa:::a gg::::::::::::::g        cc:::::::::::::::c oo:::::::::::oo   d:::::::::ddd::::d  ee:::::::::::::e       i::::::i s:::::::::::ss            GGG::::::GGG:::G a::::::::::aa:::al::::::l a::::::::::aa:::ap::::::::::::::pp   a::::::::::aa:::a gg::::::::::::::g  oo:::::::::::oo  s:::::::::::ss  ",
                   "      TTTTTTTTTTT       hhhhhhh     hhhhhhh    eeeeeeeeeeeeee       fffffffff            llllllll  aaaaaaaaaa  aaaa   gggggggg::::::g          cccccccccccccccc   ooooooooooo      ddddddddd   ddddd    eeeeeeeeeeeeee       iiiiiiii  sssssssssss                 GGGGGG   GGGG  aaaaaaaaaa  aaaallllllll  aaaaaaaaaa  aaaap::::::pppppppp      aaaaaaaaaa  aaaa   gggggggg::::::g    ooooooooooo     sssssssssss    ",
                   "                                                                                                                              g:::::g                                                                                                                                                                                       p:::::p                                         g:::::g                                   ",
                   "                                                                                                                  gggggg      g:::::g                                                                                                                                                                                       p:::::p                             gggggg      g:::::g                                   ",
                   "                                                                                                                  g:::::gg   gg:::::g                                                                                                                                                                                      p:::::::p                            g:::::gg   gg:::::g                                   ",
                   "                                                                                                                   g::::::ggg:::::::g                                                                                                                                                                                      p:::::::p                             g::::::ggg:::::::g                                   ",
                   "                                                                                                                    gg:::::::::::::g                                                                                                                                                                                       p:::::::p                              gg:::::::::::::g                                    ",
                   "                                                                                                                      ggg::::::ggg                                                                                                                                                                                         ppppppppp                                ggg::::::ggg                                      ",
                   "                                                                                                                         gggggg                                                                                                                                                                                                                                        gggggg                                         " ]

bottle_coords = [(x, y) for x,
                 chosen_str in enumerate(bottle_message) for y,
                 char in enumerate(chosen_str) if char.strip()]


def list_all_running_pods():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    pods = v1.list_pod_for_all_namespaces(watch=False)

    running_pods = {}

    for pod in pods.items:
        if pod.status.phase == "Running":
            namespace = pod.metadata.namespace
            if namespace not in running_pods:
                running_pods[namespace] = []
            running_pods[namespace].append({
                'pod_name': pod.metadata.name,
                'replicas': len(pod.status.container_statuses) if pod.status.container_statuses else 0
            })

    return running_pods

# Function to pick a random character from the bottle message
def pick_bottle_char():
    y, x = random.choice(bottle_coords)
    char = bottle_message[y][x]
    return char, x, y

# Function to convert ASCII to Morse code
def ascii_to_morse(input_string):
    return ' '.join([morse_dict.get(char.upper(), '') for char in input_string])

def check_url_response(url, message):
    print(url)
    try:
        response = requests.get(url)
        if response.text.strip() == message:
            return True
        else:
            return False
    except requests.RequestException:
        return False

def post_json_and_forget(url, data):
    try:
        print(url)
        print(data)
        requests.post(url, json=data)
    except:
        pass  # Ignore exceptions

def get_username(player):
    URL = "https://island-ctfd.apps.{}".format(config_parser['DEFAULT']['cluster_domain'])
    username = "admin"
    password = "redhat123"

    s = requests.session()
    s.headers.update({"User-Agent": "curl/7.67.0"})

    # Grab a nonce
    r = s.get(f"{URL}/login")
    print(r)
    if r.status_code != 200:
        raise AuthenticationError(
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
        raise AuthenticationError(
            f"received status code {r.status_code} from login post"
        )

    r = s.get(f"{URL}/api/v1/users/{player+1}")
    return (r.json()['data']['name'])

def submit_flag(player, challenge, flag):
    URL = "https://island-ctfd.apps.{}".format(config_parser['DEFAULT']['cluster_domain'])
    username = get_username(player)
    password = PASSWORDS[player]

    s = requests.session()
    s.headers.update({"User-Agent": "curl/7.67.0"})

    # Grab a nonce
    r = s.get(f"{URL}/login")
    if r.status_code != 200:
        raise AuthenticationError(
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
        raise AuthenticationError(
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

def challenges_4_and_5():
    for i in range(1, PLAYER_COUNT + 1):
        url = "https://hello-player{}.apps.{}/".format(i, config_parser['DEFAULT']['cluster_domain'])
        print(url)
        try:
            response = requests.get(url).text.strip()
            if response == "Hello World":
                submit_flag(i, 4, "FLAG_HELLO_99")
            if response == "Bonjour Monde":
                submit_flag(i, 5, "FLAG_BONJOUR_99")
        except requests.RequestException:
            return False

def challenge_11():
    for i in range(1, PLAYER_COUNT + 1):
        url = "https://aloha-player{}.apps.{}/".format(i, config_parser['DEFAULT']['cluster_domain'])
        print(url)
        try:
            response = requests.get(url).text.strip()
            if (response == "Hello World") or (response == "Bonjour Monde"):
                submit_flag(i, 11, "FLAG_ALOHA_99")
        except requests.RequestException:
            return False

executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS)

def challenge_morse():
    global executor

    futures = []

    for i in range(1, PLAYER_COUNT + 1):
        url = "https://morse-player{}.apps.{}/decode-morse".format(i, config_parser['DEFAULT']['cluster_domain'])
        print(url)
        morse_message = random.choice(list(morse_messages))
        data = {
            'message': ascii_to_morse(morse_message)
        }
        futures.append(executor.submit(post_json_and_forget, url, data))

    # Wait for all futures to complete
    concurrent.futures.wait(futures)

def challenge_bottle():
    global executor

    num_bottles = random.randint(10, 200)  # Randomly choose between 10 to 100 bottles
    bottles = []
    futures = []

    for _ in range(num_bottles):
        char, x, y = pick_bottle_char()
        bottle_data = {
            'character': char,
            'coordinates': {'x': x, 'y': y}
        }
        bottles.append(bottle_data)

    for i in range(1, PLAYER_COUNT + 1):
        url = "https://bottles-player{}.apps.{}/collect-bottles".format(i, config_parser['DEFAULT']['cluster_domain'])
        futures.append(executor.submit(post_json_and_forget, url, bottles))

    # Wait for all futures to complete
    concurrent.futures.wait(futures)

def challenge_13_postgres():
    all_pods = list_all_running_pods()
    for i in range(1, 101):
        namespace_name = f"player{i}"
        if namespace_name in all_pods:
            for pod in all_pods[namespace_name]:
                if pod['pod_name'].startswith("postgresql-"):
                    submit_flag(i, 13, "FLAG_POSTGRES_99")

def main():

    global PASSWORDS
    with open("../credentials.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            PASSWORDS.append(row[1])

    while True:
        challenge_bottle()
        challenge_morse()
       #challenges_4_and_5()
       #challenge_11()
       #challenge_13_postgres()

if __name__ == "__main__":
    main()
