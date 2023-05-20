import discord
from redbot.core import commands
import requests
from .d2commands import D4Utility

class DiabloAPI(D4Utility, commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def fetch_unique_items(self):
        url = "https://hellforge.vercel.app/api/v2/items/uniques"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data

    def fetch_characters(self):
        url = "https://hellforge.vercel.app/api/v2/characters"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data

    @commands.command()
    async def itemdb(self, ctx, *, item_name: str):
        unique_items = self.fetch_unique_items()

        if unique_items is not None:
            for item in unique_items:
                if item_name.lower() == item["name"].lower():
                    embed = discord.Embed(title=item["name"])
                    embed.add_field(name="Availability", value=item["availability"], inline=False)
                    embed.add_field(name="Ladder Only", value=item["ladderOnly"], inline=False)
                    embed.add_field(name="Drop Once", value=item["dropOnce"], inline=False)
                    embed.add_field(name="Item Level", value=item["itemLvl"], inline=False)
                    embed.add_field(name="Required Level", value=item["requiredLevel"], inline=False)
                    embed.add_field(name="Type", value=item["type"], inline=False)
                    embed.add_field(name="Price", value=item["price"], inline=False)
                    embed.set_footer(text="Data Provided by HellForge")
                    await ctx.send(embed=embed)
                    return

        await ctx.send(f"No data found for item: {item_name}")

    @commands.command()
    async def chardb(self, ctx, *, character_name: str):
        url = f"https://hellforge.vercel.app/api/v2/characters?name={character_name}"
        response = requests.get(url)
        if response.status_code == 200:
            character_data = response.json()
            if character_data:
                character = next((c for c in character_data if c["name"].lower() == character_name.lower()), None)
                if character:
                    embed = discord.Embed(title=character["name"])
                    embed.add_field(name="Strength", value=character.get("str", "N/A"), inline=True)
                    embed.add_field(name="Dexterity", value=character.get("dex", "N/A"), inline=True)
                    embed.add_field(name="Intelligence", value=character.get("int", "N/A"), inline=True)
                    embed.add_field(name="Vitality", value=character.get("vit", "N/A"), inline=True)
                    embed.add_field(name="Stamina", value=character.get("stamina", "N/A"), inline=False)
                    embed.set_footer(text="Data Provided by HellForge")
                    await ctx.send(embed=embed)
                    return
                else:
                    await ctx.send(f"No data found for character: {character_name}")

        await ctx.send("Failed to fetch character data.")