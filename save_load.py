import json
import os
from state import State
from Oplayer import Oplayer

file_path = "./save_files/save.json"


def save(current: State):
  global file_path
  to_save: json = {
    "game_running": False,
    "players": [],
    "fbi": {
      "members": []
    },
    "cia": {
      "members": []
    },
    "icpo": {
      "members": []
    }
  }

  to_save["game_running"] = current.game_running
  to_save["fbi"]["members"] = current.fbi.members
  to_save["cia"]["members"] = current.cia.members
  to_save["icpo"]["members"] = current.icpo.members

  players_list: list[Oplayer] = current.get_players_list()
  for player in players_list:
    player_data: json = {
      "id": 0,
      "special": "None",
      "username": "",
      "alive": True
    }
    player_data["id"] = player.id
    player_data["special"] = player.special
    player_data["username"] = player.username
    player_data["alive"] = player.alive
    to_save["players"].append(player_data)

  with open(file_path, "w") as file:
    json.dump(to_save, file)


def load(file_path: str = file_path) -> State:
  if not os.path.exists(file_path):
    return State()

  json_data: json
  with open(file_path, "r") as json_file:
    loaded = json.load(json_file)

  current: State = State()
  current.game_running = loaded["game_running"]
  current.fbi.members = loaded["fbi"]["members"]
  current.cia.members = loaded["cia"]["members"]
  current.icpo.members = loaded["icpo"]["members"]

  for player in loaded["players"]:
    player_obj: Oplayer = Oplayer()
    player_obj.id = player["id"]
    player_obj.special = player["special"]
    player_obj.username = player["username"]
    player_obj.alive = player["alive"]
    current.players.append(player_obj)

  return current


def clear_saves() -> None:
  if os.path.exists(file_path):
    #maybe use try except block?
    os.remove(file_path)
