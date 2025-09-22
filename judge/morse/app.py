import random
import requests
import os
import time

PLAYER_COUNT = 100

cluster_domain = os.environ.get('CLUSTERDOMAIN', '')

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
    "!": "-.-.--",
    "$": "...-..-",
    "&": ".-...",
    "'": ".----.",
    "(": "-.--.",
    ")": "-.--.-",
    "+": ".-.-.",
    "-": "-....-",
    ".": ".-.-.-",
    "/": "-..-.",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ":": "---...",
    ";": "-.-.-.",
    "=": "-...-",
    "?": "..--..",
    "@": ".--.-.",
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "_": "..--.-",
    " ": "/"
}


def ascii_to_morse(input_string):
    return ' '.join([morse_dict.get(char.upper(), '') for char in input_string])



def post_json_and_forget(url, data):

    try:
        print(f"HTTP POST: {url}")
        response = requests.post(url, json=data)
        print(response)
        
        if response.status_code == 200:
            print(f"{response.status_code} - morse code succesfully received")
            print(data)
        elif response.status_code == 503:
            print(f"{response.status_code} - player API endpoint not responsing yet")
        else:
            print(f"An unexpected error occurred: {response.status_code}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")




def challenge_morse():

    for i in range(1, PLAYER_COUNT + 1):
        url = f"https://morse-player{i}.apps.{cluster_domain}/decode-morse"
        morse_message = random.choice(list(morse_messages))
        data = {
            'message': ascii_to_morse(morse_message)
        }
        post_json_and_forget(url, data)
        time.sleep(0.1)


def main():
    while True:
        challenge_morse()
        time.sleep(0.1)


if __name__ == "__main__":
    main()
