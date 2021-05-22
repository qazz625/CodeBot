import discord
import os
import codefapi

TOKEN = ''

client = discord.Client()	

@client.event
async def on_ready():
	print("{0.user} has started running".format(client))
	

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith(';link'):
		s = message.content.split()
		if len(s) != 2:
			await message.channel.send("Incorrect format")
		else:
			okmessage = codefapi.request_link_user(s[1])
			await message.channel.send(okmessage[1])
			if okmessage[0] == 1:
				done = codefapi.link_user(message.author, s[1], okmessage[2])
				if done == 1:
					codefapi.insert_user(message.author, s[1])
					await message.channel.send("Linking Successful!!!!")
				else:
					await message.channel.send("Linking Failed")

	elif message.content.startswith(';problem'):
		s = message.content.split()
		s = s[1:]
		if len(s) != 1 and len(s) != 2:
			await message.channel.send("Incorrect format")
		else:
			await message.channel.send("GETTING PROBLEM")
			link = codefapi.get_problem(str(message.author), s)
			await message.channel.send(link)


	elif message.content.startswith(';virtual'):
		links = codefapi.get_virtual(str(message.author))
		if links == -1:
			await message.channel.send("User must be linked to give virtual contest.")
		else:
			for x in links:
				await message.channel.send(x)

client.run(TOKEN)