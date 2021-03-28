import discord
from discord.ext import commands
from functools import cache

import json
from search_that_hash import api
from name_that_hash.runner import api_return_hashes_as_json


class Hashes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_discord_embed(self, color):
        embed = discord.Embed(title=self.title, description=self.desc, color=color)
        embed.set_footer(text="Search that hash is licensed under GPLv3")
        return embed

    def get_types(self, embed):
        if self.result[self.hash] != "Could not crack hash":
            value = "Type(s): " + ", ".join(self.result[self.hash]["types"])
            if not self.result[self.hash]["verified"]:
                value += "\nThis hash is NOT verified, we cannot prove the plaintext / type is equal to this hash."
        else:
            to_print = []
            types = json.loads(api_return_hashes_as_json([self.hash]))
            for i in range(len(types[self.hash])):
                if i > 5:
                    break
                to_print.append(types[self.hash][i]["name"])

            value = "Type(s): " + ", ".join(to_print)

        value += f"\n\n{self.ctx.author.mention}\nhttps://github.com/HashPals/Search-That-Hash"

        embed.add_field(
            name="Additonal Info : ",
            value=value,
            inline=False,
        )
        return embed

    def defult_search(self):

        self.desc = f"Searching {self.hash} :sunglasses:"
        color = 0xFFA500
        self.title = "Hashy - Cracks hashes via Search-That-Hash API"
        embed = self.get_discord_embed(color)
        return embed

    @cache
    def get_json_result(self):
        return api.return_as_fast_json([self.hash])[0]

    def get_results(self):

        self.result = self.get_json_result()
        desc = self.hash

        if self.hash in self.result:

            if self.result[self.hash] == "Could not crack hash":
                self.desc = f"Failed to crack {self.hash} :cry:"
                color = 0xDC143C
                embed = self.get_discord_embed(color)
                embed.add_field(
                    name="Failed : ",
                    value="Hash was not found in any database.",
                )

                return self.get_types(embed)

            elif self.result[self.hash] == "No types found for this hash.":
                self.desc = f"Failed to crack {self.hash} :cry:"
                color = 0xDC143C
                embed = self.get_discord_embed(color)
                embed.add_field(name="Failed : ", value="Hash type not found")
                embed.add_field(
                    name="Ciphey : ",
                    value=f"Maybe this isn't actually a hash and instead, encrypted text. Check out our sister project ciphey for more info - https://github.com/Ciphey/Ciphey \n\n{self.ctx.author.mention}\nhttps://github.com/HashPals/Search-That-Hash",
                    inline=False,
                )

                return embed

            else:
                self.desc = f"Cracked {self.hash} :smile:"
                color = 0x00FF00
                embed = self.get_discord_embed(color)
                embed.add_field(
                    name="Cracked :",
                    value=self.result[self.hash]["plaintext"],
                )

                return self.get_types(embed)

        else:
            color = 0xDC143C
            embed = self.get_discord_embed(color)
            embed.add_field(
                name="Error :", value="Something went wrong with the program"
            )
            print(self.results)
            return embed

    @commands.command()
    async def crack(self, ctx, hash):
        self.ctx = ctx
        self.hash = hash.lower()
        message = await ctx.send(embed=self.defult_search())
        await message.edit(embed=self.get_results())
    

def setup(bot):
    bot.add_cog(Hashes(bot))
