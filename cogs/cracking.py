import discord
from discord.ext import commands
from discord import Embed

import json
from search_that_hash import api

class Hashes(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def get_discord_embed(self, desc, color, title):
		return discord.Embed(title=title, description=desc, color=color)

	@commands.command()
	async def crack(self,ctx, hash):

		### CREATING EMBED ###

		desc = "Searching.....:sunglasses:"
		color = 0xFFA500
		title = "Hashy - Cracks hashes via Search-That-Hash API"

		embed = self.get_discord_embed(desc, color, title)

		loading = await ctx.send(embed=embed)

		### GETTING RESULTS ###

		result = api.return_as_fast_json([hash])[0]

		### PRINTING ###

		if hash in result:
			color = 0x00FF00
			desc = hash
			embed = self.get_discord_embed(desc, color, title)
			embed.add_field(name="Cracked :", value=result[hash])
		else:
			color = 0xDC143C
			desc = "Failed to find :cry:"
			embed = self.get_discord_embed(desc, color, title)

		await loading.edit(embed=embed)

def setup(bot):
	bot.add_cog(Hashes(bot))