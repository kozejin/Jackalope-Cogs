import discord
from redbot.core import commands
import aiohttp

class JackaUtility(commands.Cog):
    """Cog for custom commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def d4calc(self, ctx):
        """Diablo 4 Calculator"""

        embed = discord.Embed()
        embed.title = f"D4 Build Calculator"
        embed.url = f"https://diablo.kozejin.dev/tools/skillcalc/"
        embed.description = f"A build calculator for Diablo 4."
        embed.set_image(url="https://i.imgur.com/9aSJQ9E.png")
        embed.set_footer(text="Diablo Tools")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def d4map(self, ctx):
        """Diablo 4 Map"""

        embed = discord.Embed()
        embed.title = f"Diablo 4 Map"
        embed.url = f"https://diablo.kozejin.dev/tools/map/"
        embed.description = f"An interactive map for Diablo 4."
        embed.set_image(url="https://i.imgur.com/k1yBWut.png")
        embed.set_footer(text="Diablo Tools")
        await ctx.send(embed=embed)