import discord
from discord.ext import commands
from cogs.moduels import hacking_modules


class Crackers(commands.Cog, name="Cracking & Identifying tools"):
    def __init__(self, bot):
        self.bot = bot
        self.bot.cache = {}
        self.hacking_modules_obj = hacking_modules()

    def get_link(self, embed, link):
        embed.add_field(
            name="Links",
            inline=False,
            value=f"Our github: {link}",
        )
        return embed

    @commands.command()
    async def nth(self, ctx, *, hash):
        embed = self.hacking_modules_obj.nth(hash)
        await ctx.send(
            ctx.author.mention,
            embed=self.get_link(embed, "https://github.com/HashPals/Name-That-Hash"),
        )

    @commands.command()
    async def what(self, ctx, *, text):
        embed = self.hacking_modules_obj.what(text)
        await ctx.send(
            ctx.author.mention,
            embed=self.get_link(embed, "https://github.com/bee-san/pyWhat"),
        )

    @commands.command()
    async def ciphey(self, ctx, *, text):
        msg = await ctx.send(
            ctx.author.mention,
            embed=discord.Embed(
                title="Running ciphey 🏃‍♂️",
                description="Attempting to decrypt ⌛",
                color=0xFFA500,
            ),
        )
        embed = self.hacking_modules_obj.ciphey(text)
        await msg.edit(
            embed=self.get_link(embed, "https://github.com/Ciphey/Ciphey"),
        )

    @commands.command()
    async def sth(self, ctx, *, text):
        msg = await ctx.send(
            ctx.author.mention,
            embed=discord.Embed(
                title="Running STH 🏃‍♂️",
                description="Attempting to crack ⌛",
                color=0xFFA500,
            ),
        )
        embed = self.hacking_modules_obj.sth(text)
        await msg.edit(
            embed=self.get_link(embed, "https://github.com/HashPals/Search-That-Hash"),
        )


def setup(bot):
    bot.add_cog(Crackers(bot))
