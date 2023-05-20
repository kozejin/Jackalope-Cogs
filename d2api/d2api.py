import discord
from redbot.core import commands
import requests
from bs4 import BeautifulSoup

class D2Scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def item(self, ctx, *item_name):
        item_name = " ".join(item_name)  # Join the words in the item name

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
            # Find the item name
            item_name_element = row.find("b")
            if item_name_element:
                current_item_name = item_name_element.text.strip()
                if item_name.lower() in current_item_name.lower():
                    item_stats_elements = row.find_next_siblings("tr")
                    item_stats = []
                    for stats_element in item_stats_elements:
                        if stats_element.find("td"):
                            item_stats.append(stats_element.find("td").text.strip())

                    # Find the item image
                    img_element = row.find("img")
                    if img_element:
                        item_image_url = "https://classic.battle.net" + img_element["src"]
                    else:
                        item_image_url = None

                    # Send the item details as a message
                    embed = discord.Embed(title=current_item_name, color=discord.Color.green())
                    if item_image_url:
                        embed.set_thumbnail(url=item_image_url)
                    if item_stats:
                        item_stats_str = "\n".join([f"\u00A0{stat}" for stat in item_stats])
                        embed.description = item_stats_str
                    await ctx.send(embed=embed)
                    return

        # If the item was not found, send an error message
        await ctx.send(f"Item '{item_name}' not found in the database.")