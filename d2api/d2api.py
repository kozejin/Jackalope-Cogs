import discord
from redbot.core import commands
import requests
from bs4 import BeautifulSoup

def scrape_item_details(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')

    item_details = []

    for row in rows:
        columns = row.find_all('td')

        if len(columns) == 2:
            item_name = columns[0].find('b').text.strip()
            item_type = columns[0].find_all('center')[1].text.strip()
            item_stats = columns[1].text.strip()

            item_details.append({
                'Item Name': item_name,
                'Item Type': item_type,
                'Item Stats': item_stats
            })

    return item_details

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

        # Scrape item details
        item_data = scrape_item_details(html)

        found_item = False  # Flag to check if the item is found

        for item in item_data:
            if item_name.lower() in item['Item Name'].lower():
                found_item = True  # Set the flag to indicate item found

                # Send the item details as a message
                embed = discord.Embed(title=item['Item Name'], description=item['Item Type'], color=discord.Color.green())
                embed.add_field(name='Item Stats', value=item['Item Stats'])
                await ctx.send(embed=embed)
                break

        if not found_item:
            # If the item was not found, send an error message
            await ctx.send(f"Item '{item_name}' not found in the database.")