import requests
import random
import configparser

config_parser = configparser.ConfigParser()
config_parser.read('settings.ini')

def fetch_user_data(user_id):
    """Fetch user data by user_id."""
    url = f"https://island-ctfd.apps.{config_parser['DEFAULT']['cluster_domain']}/api/v1/users/{user_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for user {user_id}")
        return None

def get_lottery_winner():
    """Run the lottery and return the winner."""
    # Fetch data for all users
    users_data = [fetch_user_data(uid) for uid in range(2, 102)]

    # Filter out any None values (failed fetches)
    users_data = [data for data in users_data if data]

    # Create a lottery pool
    lottery_pool = []
    for user_data in users_data:
        user_tickets = user_data['data']['score']
        for _ in range(user_tickets):
            lottery_pool.append(user_data['data']['id'])  # Use user id to represent each ticket

    # Draw a winner from the lottery pool
    winner_id = random.choice(lottery_pool)
    return next((data for data in users_data if data['data']['id'] == winner_id), None)

if __name__ == "__main__":
    winner = get_lottery_winner()
    if winner:
        print(f"The winner is: {winner['data']['name']} with user ID: {winner['data']['id']}")
    else:
        print("No winner selected!")
