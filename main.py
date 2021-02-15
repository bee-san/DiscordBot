import discord
from discord.ext import commands
from name_that_hash import runner
import json
from search_that_hash import api
import random

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command()
async def hash(ctx, hash):
    result = json.loads(api.return_as_fast_json([hash]))
    embed = discord.Embed(title="Hashy - Cracks hashes via Search-That-Hash API", description=hash, color=random.randint(0,16777215)) #,color=Hex code
    try:
        if result[0][hash][0] == {}:
            embed.add_field(name="Plaintext", value="Could not crack hash", inline=False)
        else:
            embed.add_field(name="Plaintext", value=result[0][hash], inline=False)
    except:
        embed.add_field(name="Plaintext", value="Could not crack hash", inline=False)
    embed.set_footer(text="https://github.com/HashPals/Search-That-Hash") #if you like to
    await ctx.send(embed=embed)

bot.run("")
