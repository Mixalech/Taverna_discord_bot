import discord
from discord.ext import commands


TOKEN = "xxxx-xxxx--xxxx-xxxx--x-x-x-x-x--x-xx-xx-x"
bot = commands.Bot(command_prefix='/', intents = discord.Intents.all())
ID_POST = 1137999093982040115
MAX_ROLES = 7
USER_ROLES_LIST = {}


ROLES_LIST = {
    "🍺": 1137679541561729074, #посетитель
    "🚬": 1137959358517477416, #курильщик
    "🚭": 1137609824025198683, #трезвый
}