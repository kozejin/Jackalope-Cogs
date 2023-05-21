import discord
from redbot.core import commands
from bs4 import BeautifulSoup
import aiohttp
from bs4.element import NavigableString

BASE_URL = "https://classic.battle.net"
ITEM_URL = f"{BASE_URL}/diablo2exp/items/elite/uhelms.shtml"

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

        try:
            # Send a GET request to the URL and retrieve the page HTML
            html = await self.fetch_html(ITEM_URL)
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
                    # Find the item properties
                    property_element = row.find("td", attrs={"width": "100%"})
                    item_info = []  # Define item_info outside the condition
                    if property_element:
                        for child in property_element.children:
                            if isinstance(child, NavigableString):
                                item_info.append(child.strip())

                    # Find the item image
                    img_element = row.find("img")
                    if img_element:
                        item_image_url = BASE_URL + img_element["src"]
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
                    return

        # If the item was not found, send an error message
        await ctx.send(f"Item '{item_name}' not found in the database.")

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())
