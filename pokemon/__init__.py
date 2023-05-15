from .pokemon import Pokemon


async def setup(bot):
    n = Pokemon()
    await bot.add_cog(n)
