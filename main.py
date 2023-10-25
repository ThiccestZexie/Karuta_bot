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
karuta_bot_id = 646937666251915264 
karuta_bot_name = "Karuta"
expected_channel_id  = 1154079321913307167 
user_ids = []


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return
    if ctx.channel.id == expected_channel_id:
        if ctx.embeds and (ctx.author.id == karuta_bot_id and ctx.author.name == karuta_bot_name or ctx.author.name == "Karuta#1280"):
            print("found embeds")
            print(ctx.embeds)
            print(ctx.embeds[0].to_dict()['description'])
        




load_dotenv()
bot.run(os.getenv("TOKEN"))
