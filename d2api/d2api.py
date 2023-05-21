import discord
import re
from redbot.core import commands
from bs4 import BeautifulSoup
import aiohttp
from .d2keys import BASE_URL, ITEM_URLS
from .d2const import properties, color_code

class D2Scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()  # HTTP session for making requests

    async def fetch_html(self, url):
        async with self.session.get(url) as response:
            return await response.text()

    @commands.command()
    async def item(self, ctx, *item_name):
        item_name = " ".join(item_name).lower()  # Join the words in the item name

        for item_url in ITEM_URLS:
            try:
                # Send a GET request to the URL and retrieve the page HTML
                html = await self.fetch_html(item_url)
            except Exception as e:
                await ctx.send(f"Error fetching data: {e}")
                return

            # Create a BeautifulSoup object to parse the HTML
            soup = BeautifulSoup(html, "html.parser")

            # Find all the item rows in the table
            rows = soup.find_all("tr")

            # Iterate over each row and extract the item details
            for row in rows:
                # Find the item name
                item_name_element = row.find("b")
                if item_name_element:
                    current_item_name = item_name_element.text.strip().lower()
                    if item_name in current_item_name:
                        raw_info = row.get_text(separator='\n')
                        item_info = [line for line in raw_info.split('\n') 
                                    if any(prop in line.lower() for prop in properties) or "-" in line]

                        # Find color coded information
                        colored_elements = row.find_all("font", {"color": re.compile(color_code, re.I)})
                        colored_info = [element.get_text() for element in colored_elements]
                        item_info.extend(colored_info)

                        # Find the item image
                        img_element = row.find("img")
                        if img_element:
                            item_image_url = BASE_URL + img_element["src"]
                        else:
                            item_image_url = None

                        # Send the item details as a message
                        title = current_item_name.split(" ")
                        title = " ".join(word.capitalize() for word in title)
                        embed = discord.Embed(title=title, color=discord.Color.green())
                        if item_image_url:
                            embed.set_thumbnail(url=item_image_url)
                        if item_info:
                            item_info_str = "\n".join(item_info)
                            embed.description = item_info_str
                        await ctx.send(embed=embed)
                        return

        # If the item was not found, send an error message
        await ctx.send(f"Item '{item_name}' not found in the database.")
