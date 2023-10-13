import telebot
from agency import agency
from Oplayer import Oplayer


class State:

  __game_running: bool
  __players: list[Oplayer]
  __fbi: agency
  __cia: agency
  __icpo: agency
  __main_chat: int

  def __init__(self) -> None:
    self.set_game_running(False)
    self.players = []
    self.fbi = agency()
    self.cia = agency()
    self.icpo = agency()
    #TODO now it's hardcoded, in future I want it to be loaded from save.json or from another file
    self.main_chat = -1001718028928

  def is_game_running(self) -> bool:
    return self.game_running

  def set_game_running(self, state: bool) -> None:
    self.game_running = state
    return

  def get_players_list(self) -> list[Oplayer]:
    return self.players

  def append_player(self, message: telebot.types.Message) -> str:
    if self.is_game_running():
      return "Can't join a running game!"
    for player in self.players:
      if player.id == message.from_user.id:
        return f"{player.username} is already part of the game."

    # If player is new
    player = Oplayer()
    player.id = message.from_user.id
    player.username = message.from_user.username
    player.alive = True
    self.players.append(player)
    # Send a message to the user
    return f"{player.username} is now part of the game."

  def remove_player(self, message: telebot.types.Message) -> str:
    if self.is_game_running():
      return "Can't leave a running game!"
    for player in self.players:
      if player.id == message.from_user.id:
        self.players.remove(player)
        return f"{player.username} has left the game."

    # Send a message to the user
    return f"{message.from_user.username} is not part of the game."

  def clear_players_list(self) -> None:
    self.players.clear()

  def append_fbi(self, member: str) -> None:
    self.fbi.append_member(member)

  def append_cia(self, member: str) -> None:
    self.cia.append_member(member)

  def append_icpo(self, member: str) -> None:
    self.icpo.append_member(member)

  def get_fbi(self) -> agency:
    return self.fbi

  def get_cia(self) -> agency:
    return self.cia

  def get_icpo(self) -> agency:
    return self.icpo

  def clear_all_agencies(self) -> None:
    self.fbi.clear()
    self.cia.clear()
    self.icpo.clear()

  def set_main_chat(self, chat_id: int) -> None:
    self.main_chat = chat_id