import discord
from redbot.core import commands
import aiohttp

class JackaUtility(commands.Cog):
    """Cog for custom commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.bot_has_permissions(embed_links=True)
    async def d4skills(self, ctx):
        """Diablo IV Build Calculator"""

        embed = discord.Embed()
        embed.title = f"D4 Build Calculator"
        embed.url = f"https://diablo.kozejin.dev/tools/skillcalc/"
        embed.color = 3447003
        embed.description = f"A build calculator for Diablo 4."
        embed.set_image(url="https://i.imgur.com/9aSJQ9E.png")
        embed.set_footer(text="Diablo Tools")
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    @commands.bot_has_permissions(embed_links=True)
    async def d4map(self, ctx):
        """Diablo IV Map"""

        embed = discord.Embed()
        embed.title = f"Diablo 4 Map"
        embed.url = f"https://diablo.kozejin.dev/tools/map/"
        embed.color = 15105570
        embed.description = f"An interactive map for Diablo 4."
        embed.set_image(url="https://i.imgur.com/k1yBWut.png")
        embed.set_footer(text="Diablo Tools")
        await ctx.send(embed=embed)