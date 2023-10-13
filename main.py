# Importing Required Libraries, Imported os Module For Security
import os, telebot
from flask import Flask
import random
from agency import agency
from Oplayer import Oplayer
from state import State
import save_load, admin, special_interactions

admin_list : list[str] = ["admin1", "admin2"] #telegram admins usernames
# Getting Bot Token From Secrets
BOT_TOKEN = os.environ.get('BOT_TOKEN')
# Define the roles
SPECIALS : list[str] = ["Assassin", "Detective", "AssassinSub", "DetectiveSub1", "DetectiveSub2", "WifeAssassin"]
# Creating Telebot Object
bot = telebot.TeleBot(BOT_TOKEN)
# global game state
current : State = None

@bot.message_handler(commands=['startgame'])
def start_game(message) -> None:
  if message.from_user.username not in admin_list:
    return
  global SPECIALS
  global current
  if current.is_game_running():
    bot.send_message(chat_id=message.chat.id, text="Game is already running")
    return
  if current.players == []:
    bot.send_message(chat_id=message.chat.id,
                     text="No players have joined the game yet.")
    return

  # Slice role list
  if len(SPECIALS) > len(current.players):
    SPECIALS = SPECIALS[0:len(current.players)]
  # Fill with empty role list
  elif len(SPECIALS) <= len(current.players):
    for i in range(len(SPECIALS), len(current.players)):
      SPECIALS.append("None")
  # Shuffle the roles
  random.shuffle(SPECIALS)
  current.set_game_running(True)
  # Assign roles to each member
  random_pos : int = []
  for i in range(0, len(current.players)):
    random_pos.append(i % 3)
  random.shuffle(random_pos)
  for i, player in enumerate(current.players):
    bot.send_message(chat_id=player.id, text="======NEW GAME HAS STARTED======")
    player.special = SPECIALS[i]
    if player.special != "None":
      bot.send_message(chat_id=player.id, text=f"Your special role is {player.special}")
    print("index of role assignation loop:" + str(i))#DEBUG
    agency_id = random_pos[i]
    agency_name = "none"
    match agency_id:
      case 0:
        agency_name = "FBI"
        current.append_fbi(player.username)
      case 1:
        agency_name = "CIA"
        current.append_cia(player.username)
      case 2:
        agency_name = "ICPO"
        current.append_icpo(player.username)
    bot.send_message(chat_id=player.id, text=f"Your agency is {agency_name}")
    
    
  # Other agency members
  fbi_members : list[str] = current.get_fbi().get_members_list()
  cia_members : list[str] = current.get_cia().get_members_list()
  icpo_members : list[str] = current.get_icpo().get_members_list()
  for player in current.players:
    for member in fbi_members:
      if player.username == member:
        bot.send_message(chat_id=player.id, text="Other FBI members are: " + ",".join(
          element for element in fbi_members
        ))
    for member in cia_members:
      if player.username == member:
        bot.send_message(chat_id=player.id, text="Other CIA members are: " + ",".join(
          element for element in cia_members
        ))
    for member in icpo_members:
      if player.username == member:
        bot.send_message(chat_id=player.id, text="Other ICPO members are: " + ",".join(
          element for element in icpo_members
        ))
  
  bot.send_message(chat_id=message.chat.id,text="Roles have been chosen. Check your private chat.")
  save_load.save(current)

# Join game lobby
@bot.message_handler(commands=['join'])
def join_game(message : telebot.types.Message):
  global current
  result_message = current.append_player(message)
  bot.send_message(
    chat_id=message.chat.id,
    text=result_message)
  save_load.save(current)

# Leave game lobby
@bot.message_handler(commands=['leave'])
def leave_game(message : telebot.types.Message):
  global current
  result_message = current.remove_player(message)
  bot.send_message(
    chat_id=message.chat.id,
    text=result_message)
  save_load.save(current)

# admin commands
@bot.message_handler(commands=['load'])
def manual_load(message) -> None:
  admin.manual_load(message, admin_list)

@bot.message_handler(commands=['endgame'])
def end_game(message: telebot.types.Message) -> None:
  admin.end_game(message, bot, current, admin_list)

@bot.message_handler(commands=['assassin','Assassin'])
def assassin_message(message: telebot.types.Message) -> None:
  special_interactions.assassin_message(message, bot, current)

@bot.message_handler(commands=['detective', 'Detective'])
def detective_message(message: telebot.types.Message) -> None:
  special_interactions.detective_message(message, bot, current)

@bot.message_handler(commands=['dbook', 'Dbook'])
def dbook_message(message: telebot.types.Message) -> None:
  special_interactions.dbook_message(message, bot, current)

app = Flask(__name__)


@app.route('/')
def home():
  return "Il bot è in esecuzione"


def run_flask():
  app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
  random.seed()
  #global current
  current = save_load.load()
  from threading import Thread
  t = Thread(target=run_flask)
  t.start()
  bot.infinity_polling()