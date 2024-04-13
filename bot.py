import requests
import json
import chess
import time
def read_game_state(game_id, bot_token):
    url = f"https://lichess.org/api/bot/game/stream/{game_id}"
    headers = {"Authorization": f"Bearer {bot_token}"}

    try:
        with requests.get(url, headers=headers, stream=True) as response:
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        game_state = json.loads(line.decode('utf-8'))
                        return game_state
            else:
                print("Failed to connect. Check your game ID and bot token.")
                return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def play_move(game_id, move, bot_token):
    url = f"https://lichess.org/api/bot/game/{game_id}/move/{move}"
    headers = {"Authorization": f"Bearer {bot_token}"}

    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print("Move successfully played.")
            return True
        else:
            print("Failed to play move.")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def find_black_info(game_data):
    if 'black' in game_data:
        return game_data['black']
    else:
        return None

def find_white_info(game_data):
    if 'white' in game_data:
        return game_data['white']
    else:
        return None

game_id = "M5oo9qvzM4hV"
bot_token = "lip_aO2neoPU45kTorbEbWX9"

white_info = find_white_info(read_game_state(game_id, bot_token))
black_info = find_black_info(read_game_state(game_id, bot_token))

def whatcolour(game_data, username):
    if 'black' in game_data:
        black = game_data['black']
        white = game_data['white']
        try:
            if black['id'] == username:
                return "black"
        except:    
            if white['id'] == username:
                return "white"
    return "Not in game"

white = False
black = True

def get_value(string):
    try:
        return [value[string] for value in read_game_state(bot_token)['state']]
    except:
        print("Couldn't find any games with specified string: {string}")

#print(get_value("winner"))

print(len(read_game_state(game_id, bot_token)['state']['moves'].split(" ")))

#https://lichess.org/C6be9uAk
#opponents_mpve = (read_game_state(game_id, bot_token)['state']['moves'].split(" ")[-1])
#print(opponents_mpve)