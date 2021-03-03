import discord
from discord.ext import commands
from discord import Embed

import json
from search_that_hash import api
from name_that_hash.runner import api_return_hashes_as_json
import asyncio

class Hashes(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def get_discord_embed(self, desc, color, title):
		embed = discord.Embed(title=title, description=desc, color=color)
		embed.set_footer(text='https://github.com/HashPals/Search-That-Hash')
		return embed

	@commands.command()
	async def crack(self,ctx, hash):

		### CREATING EMBED ###

		desc = f"Searching {hash} :sunglasses:"
		color = 0xFFA500
		title = "Hashy - Cracks hashes via Search-That-Hash API"

		embed = self.get_discord_embed(desc, color, title)

		message = await ctx.send(embed=embed)

		### GETTING RESULTS ###

		result = api.return_as_fast_json([hash])[0]
		desc = hash

		### REACTING ###

		def check(reaction, user):
			return user == ctx.author and str(reaction.emoji) == "✅"

		### PRINTING ###

		if hash in result:
			if result[hash] == 'Could not crack hash':
				color = 0xDC143C
				embed = self.get_discord_embed(desc, color, title)
				embed.add_field(name="Failed : ", value="Hash was not found in any database. React ✅ to see possible hash types.")
				await message.edit(embed=embed)
				while True:
					try:
						reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)						
						types = json.loads(api_return_hashes_as_json([hash]))
						color = 0x0800ff
						embed_types = self.get_discord_embed(desc, color, title)
						to_print = []

						for i in range(len(types[hash])):
							if i > 5:
								break
							to_print.append(types[hash][i]['name'])

						embed.add_field(name="Possible Types : ", value=", ".join(to_print), inline=False)
						await message.edit(embed=embed)
					except asyncio.TimeoutError:
						pass

			elif result[hash] == 'No types found for this hash.':
				color = 0xDC143C
				embed = self.get_discord_embed(desc, color, title)
				embed.add_field(name="Failed : ", value="Hash type could not be found")
				embed.add_field(name="Ciphey : ", value="Maybe this isn't actully a hash and instead, encrypted text. Check out our sister project ciphey for more info - https://github.com/Ciphey/Ciphey", inline=False)

			else:
				color = 0x00ff00
				embed = self.get_discord_embed(desc, color, title)
				embed.add_field(name="Cracked :", value=result[hash])
		else:
			color = 0xDC143C
			desc = "Something went wrong :cry:"
			embed = self.get_discord_embed(desc, color, title)

		await message.edit(embed=embed)
		await ctx.send(ctx.author.mention)

def setup(bot):
	bot.add_cog(Hashes(bot))