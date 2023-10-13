import telebot
import save_load
from state import State


def manual_load(message, admin_list: list[str]):
  if message.from_user.username not in admin_list:
    return
  save_load.load()


def end_game(message: telebot.types.Message, bot: telebot.TeleBot,
             current: State, admin_list: list[str]) -> None:
  if message.from_user.username not in admin_list:
    return
  current.set_game_running(False)
  # Reset the players
  for player in current.players:
    bot.send_message(chat_id=player.id, text="======GAME HAS ENDED======")
  current.clear_players_list()
  current.clear_all_agencies()
  #delete previously saved files
  save_load.clear_saves()
  # Send a message to the group
  bot.send_message(chat_id=message.chat.id,
                   text="The game has ended. All roles have been reset.")
