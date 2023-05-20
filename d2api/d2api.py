import discord
from redbot.core import commands
import requests
from bs4 import BeautifulSoup

class D2Scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def item(self, ctx, item_name):
        url = "https://classic.battle.net/diablo2exp/items/elite/uhelms.shtml"

        # Send a GET request to the URL and retrieve the page HTML
        response = requests.get(url)
        html = response.text

        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(html, "html.parser")

        # Find all the item rows in the table
        rows = soup.find_all("tr")

        # Iterate over each row and extract the item details
        for row in rows:
            # Find the item name and stats
            item_name_element = row.find("b")
            if item_name_element:
                current_item_name = item_name_element.text.strip()
                if current_item_name.lower() == item_name.lower():
                    item_stats = row.find("font").text.strip()

                    # Send the item details as a message
                    embed = discord.Embed(title=current_item_name, description=item_stats, color=discord.Color.green())
                    await ctx.send(embed=embed)
                    return

        # If the item was not found, send an error message
        await ctx.send(f"Item '{item_name}' not found in the database.")