from .d2items import DiabloAPI

async def setup(bot):
    await bot.add_cog(DiabloAPI(bot))