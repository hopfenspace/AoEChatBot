import os, json
from telegram.ext import Updater, CommandHandler

with open("./config.json", "r") as fd:
	config = json.load(fd)

taunts = {}
tauntNames = {}
commands = []
for filename in os.listdir(config["taunt-dir"]):
	split = filename.split(" ")
	num = int(split[0])
	name = " ".join(split[1 : ]).split(".")[0]
	path = os.path.join(config["taunt-dir"], filename)

	taunts[num] = path
	tauntNames[num] = name
	commands.append(str(num))

commands = sorted(commands)

def handleCmd(bot, update):
	msg = update.message
	text = msg.text.split(" ")[0].split("@")[0][1 : ]
	num = int(text)
	file = taunts[num]

	with open(file, "rb") as fd:
		bot.send_voice(msg.chat.id, fd)

def sendCmdList(bot, update):
	update.message.reply_text("Supported Commands: /" + ", /".join(commands))

def sendCmdDoc(bot, update):
	doc = "commands - Print a list of all available commands\n" + \
		"doc - Print a BotFather friendly command documentation"

	for num in commands:
		num = int(num)
		doc += "\n{} - {}".format(num, tauntNames[num])

	update.message.reply_text(doc)

updater = Updater(config["telegram-token"])

updater.dispatcher.add_handler(CommandHandler("commands", sendCmdList))
updater.dispatcher.add_handler(CommandHandler("doc", sendCmdDoc))

for cmd in commands:
	updater.dispatcher.add_handler(CommandHandler(cmd, handleCmd))

updater.start_polling()
updater.idle()
