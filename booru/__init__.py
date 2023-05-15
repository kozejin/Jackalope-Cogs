from .booru import Booru


async def setup(bot):
    n = Booru()
    await bot.add_cog(n)
