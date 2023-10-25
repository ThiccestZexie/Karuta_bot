# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
import os
import requests
import json
from dotenv import load_dotenv

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='€', description=description, intents=intents)

user_ids = []


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return
    if ctx.embeds:
        print("found embeds")
        print(ctx.embeds)
        print(ctx.embeds[0].to_dict()['description'])




load_dotenv()
bot.run(os.getenv("TOKEN"))
