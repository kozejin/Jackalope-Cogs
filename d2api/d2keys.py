import discord
import re
from redbot.core import commands
from bs4 import BeautifulSoup
import aiohttp

class D2Keys:
    BASE_URL = "https://classic.battle.net"
    ITEM_URLS = [
        f"{BASE_URL}/diablo2exp/items/elite/uhelms.shtml",
        f"{BASE_URL}/diablo2exp/items/elite/uarmor.shtml",
        f"{BASE_URL}/diablo2exp/items/elite/ushields.shtml"
    ]