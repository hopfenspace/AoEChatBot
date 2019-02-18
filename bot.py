import os, json
from telegram.ext import Updater, CommandHandler

with open("./config.json", "r") as fd:
	config = json.load(fd)

taunts = {}
commands = []
for file in os.listdir(config["taunt-dir"]):
	num = int(file.split(" ")[0])
	path = os.path.join(config["taunt-dir"], file)
	taunts[num] = path
	commands.append(str(num))

def handleCmd(bot, update):
	msg = update.message
	text = msg.text.split(" ")[0][1 : ]
	num = int(text)
	file = taunts[num]

	with open(file, "rb") as fd:
		bot.send_voice(msg.chat.id, fd)

updater = Updater(config["telegram-token"])

for cmd in commands:
	updater.dispatcher.add_handler(CommandHandler(cmd, handleCmd))

updater.start_polling()
updater.idle()
