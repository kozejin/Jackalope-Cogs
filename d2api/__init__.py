from .d2api import D2Scraper

async def setup(bot):
    await bot.add_cog(D2Scraper(bot))