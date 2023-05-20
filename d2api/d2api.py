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

        # Find the table containing the item data
        table = soup.find("table", class_="wikitable")

        # Iterate over each row in the table
        for row in table.find_all("tr")[1:]:
            columns = row.find_all("td")
            current_item_name = columns[0].text.strip()

            # Check if the current item matches the search item
            if current_item_name.lower() == item_name.lower():
                item_stats = columns[1].text.strip()

                # Send the item details as a message
                embed = discord.Embed(title=current_item_name, description=item_stats, color=discord.Color.green())
                await ctx.send(embed=embed)
                return

        # If the item was not found, send an error message
        await ctx.send(f"Item '{item_name}' not found in the database.")