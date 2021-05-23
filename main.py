import discord
from discord.ext import commands

if __name__ == "__main__":

    bot = commands.Bot(command_prefix="$")

    exts = ["cogs.tools"]

    for ext in exts:
        bot.load_extension(ext)

with open(".env", "r") as file:
    token = file.read()

bot.run(
    token,
    bot=True,
    reconnect=True,
)
