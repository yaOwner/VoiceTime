prev = []
@client.event
async def on_ready():
	print('Bot connected')
	while True:
		for guild in client.guilds:
			ignored_channels = [761870642794070067]
				
			voices = [channel for channel in guild.voice_channels if channel.id not in ignored_channels]
			members = [channel.members for channel in voices]
				
			ids = []
			for lst in members:
				for member in lst:
					ids.append(member)

			if len(ids) <= 0:
				continue
				
			for member in ids:
				if member in prev:
					if not collection.count_documents({"_id": member.id}):
						collection.insert_one({"_id": message.author.id, "minvoice": 0, "lvl": 1, "xp": 0, "cash": 0})
	
					mins = collection.find_one({"_id": member.id})['minvoice'] + 1
					collection.update_one({"_id": member.id}, {"$set": {"minvoice": mins}})
					if mins % 60 == 0:
						xp = collection.find_one({"_id": member.id})['xp'] + random.randint(6, 12)
						
						collection.update_one({"_id": member.id}, {"$set": {"xp": xp}})
						if xp >= 500 + 900 * collection.find_one({"_id": member.id})['lvl']:
							lvl_up = collection.find_one({"_id": member.id})['lvl'] + 1
								
							collection.update_one({"_id": member.id}, {"$set": {"lvl": lvl_up, "xp": 0}})

							award = 226 * lvl_up
							newbalance = collection.find_one({"_id": member.id})['cash'] + award
								
							collection.update_one({"_id": member.id}, {"$set": {"cash": newbalance}})

				else:
					prev.append(member)
						
		await asyncio.sleep(1)


@client.event
async def on_voice_state_update(member, before, after):
	pass


@client.command()
async def voicetime(ctx):
	seconds = collection.find_one({"_id": ctx.author.id})['minvoice']

	seconds = seconds % (24 * 3600)
	days = seconds // (60 * 60 * 24)
	hours = seconds // 3600
	seconds %= 3600
	minutes = seconds // 60
	seconds %= 60

	user = collection.find_one({"_id": ctx.author.id})
	emb = discord.Embed(title = f'profile | {ctx.author}')
	emb.add_field(name = 'Уровень', value = user['lvl'])
	emb.add_field(name = 'Опыт', value = user['xp'])
	emb.add_field(name = 'баланс', value = user['cash'])
	emb.add_field(name = 'время в войсе', value = f'{days}д. {hours}ч. {minutes}м.')

	await ctx.send(embed = emb)
