import telebot
from state import State


def assassin_message(message: telebot.types.Message, bot: telebot.TeleBot,
                 current: State) -> None:
  if message.chat.id == current.main_chat:
    return
  for player in current.players:
    if player.special != "Assassin" and player.username == message.from_user.username:
      return
  bot.send_message(chat_id=current.main_chat, text="Assassin: " + message.text[5:])


def detective_message(message: telebot.types.Message, bot: telebot.TeleBot,
                    current: State) -> None:
  if message.chat.id == current.main_chat:
    return
  for player in current.players:
    if player.special != "Detective" and player.username == message.from_user.username:
      return
  bot.send_message(chat_id=current.main_chat,
                   text="Detective: " + message.text[8:])


def dbook_message(message: telebot.types.Message, bot: telebot.TeleBot,
                  current: State) -> None:
  if message.chat.id == current.main_chat:
    return
  for player in current.players:
    if player.special != "Assassin" and player.username == message.from_user.username:
      return
  bot.send_message(chat_id=current.main_chat,
                   message_thread_id=407,
                   text=message.text[7:])
