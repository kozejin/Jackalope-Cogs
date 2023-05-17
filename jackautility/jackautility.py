from redbot.core import commands

class JackaUtility(commands.Cog):
    """Cog for custom commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def d4calc(self, ctx):
        """Diablo 4 Calculator"""

        embed = discord.Embed()
        embed.title = f"Diablo 4 Calculator"
        embed.url = f"http://diablo.kozejin.dev"
        embed.set_footer(text="Diablo Tools")
        await ctx.send(embed=embed)