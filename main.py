import discord
from discord.ext import commands

if __name__ == "__main__":

    bot = commands.Bot(command_prefix="$")

    exts = ["cogs.cracking"]

    for ext in exts:
        bot.load_extension(ext)

bot.run(
    "",
    bot=True,
    reconnect=True,
)
