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

        found_item = False  # Flag to check if the item is found
        item_info = []  # List to store item details

        # Iterate over each row and extract the item details
        for row in rows:
            # Find the item name
            item_name_element = row.find("b")
            if item_name_element:
                current_item_name = item_name_element.text.strip()
                if item_name.lower() in current_item_name.lower():
                    found_item = True  # Set the flag to indicate item found
                else:
                    found_item = False  # Set the flag to indicate item not found
                    continue  # Skip to the next row if item not found

            # Find the item information
            if found_item:
                item_info_elements = row.find_all("font", face="arial,helvetica", size="-1")
                for element in item_info_elements:
                    item_info.append(element.text.strip())

        # If the item was found, send the item details as a message
        if found_item:
            # Find the item image
            img_element = soup.find("img", alt=current_item_name)
            if img_element:
                item_image_url = "https://classic.battle.net" + img_element["src"]
            else:
                item_image_url = None

            # Send the item details as a message
            embed = discord.Embed(title=current_item_name, color=discord.Color.green())
            if item_image_url:
                embed.set_thumbnail(url=item_image_url)
            if item_info:
                item_info_str = "\n".join(item_info)
                embed.description = item_info_str
            await ctx.send(embed=embed)
        else:
            # If the item was not found, send an error message
            await ctx.send(f"Item '{item_name}' not found in the database.")