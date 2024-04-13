import requests
import json

def play_game(username, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Create a game challenge
    data = {
        'rated': 'true',
        'variant': 'standard'
    }
    response = requests.post(f'https://lichess.org/api/challenge/{username}', headers=headers, json=data)
    
    if response.status_code != 200:
        print(f"Failed to create a game challenge. Status code: {response.status_code}")
        return
    
    game_info = response.json().get('challenge')
    if not game_info:
        print("Failed to retrieve game information.")
        return
    
    game_id = game_info.get('id')
    if not game_id:
        print("Failed to retrieve game ID.")
        return
    
    print(f"Game created successfully! Game ID: {game_id}")
    
    # Wait for an opponent to accept the challenge
    print("Waiting for an opponent to accept the challenge...")
    while True:
        response = requests.get(f'https://lichess.org/api/stream/event', headers=headers, stream=True)
        for line in response.iter_lines():
            if line:
                event = json.loads(line)
                if event['type'] == 'challenge':
                    if event['challenge']['id'] == game_id and event['challenge']['status'] == 'accepted':
                        print("Opponent accepted the challenge! Starting the game...")
                        return event['challenge']['url']
                    
username = 'DillonBot'
token = 'lip_eouqmvubVApOnZV8GnFP'

game_url = play_game(username, token)
if game_url:
    print("Game URL:", game_url)
else:
    print("Failed to start the game.")


