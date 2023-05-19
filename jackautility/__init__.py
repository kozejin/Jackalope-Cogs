from .jackautility import JackaUtility

async def setup(bot):
    await bot.add_cog(JackaUtility(bot))