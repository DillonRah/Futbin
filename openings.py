import requests
import json
import chess
import time

def get_masters(bot_token):
    url = f"https://explorer.lichess.ovh/masters"
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
    
game_id = "2MR8HConZCg"
bot_token = "lip_aO2neoPU45kTorbEbWX9"

#white_info = find_white_info(get_masters(game_id, bot_token))
#black_info = find_black_info(get_masters(game_id, bot_token))

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

#print(amIblack(get_masters(game_id, bot_token)))
#https://lichess.org/C6be9uAk
#opponents_mpve = (get_masters(game_id, bot_token)['state']['moves'].split(" ")[-1])
whitenumbers = []
blacknumbers = []
drawnumbers = []

def get_value(string):
    try:
        return [value[string] for value in get_masters(bot_token)['moves']]
    except:
        print("Couldn't find any games with specified string: {string}")
        return None

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    # Divide the array into two halves
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    # Recursively sort each half
    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)
    
    # Merge the sorted halves
    return merge(left_half, right_half)

def merge(left, right):
    result = []
    left_idx, right_idx = 0, 0
    
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] < right[right_idx]:
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1
    
    # Add remaining elements from left and right subarrays
    result.extend(left[left_idx:])
    result.extend(right[right_idx:])
    
    return result


def openingmove(colour):
    white_values = get_value("white")
    black_values = get_value("black")
    moves = get_value("uci")
    ratios = [white / black for white, black in zip(white_values, black_values)]
    sortedratios = merge_sort(ratios)
    map = {}
    for move, ratio in zip(moves, ratios):
        map[ratio] = move

    if colour == "white":
        return map[sortedratios[-1]]
    if colour == "black":
        return map[sortedratios[0]]
    print("Invalid colour")
    return None

#print(openingmove("white"))
#print(whatcolour(read_game_state(game_id, bot_token), "dillonnea"))

print(len(read_game_state(game_id, bot_token)['state']['moves'].split(" ")))