# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os
from dotenv import load_dotenv
import settings
import re

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='€', description=settings.description, intents=intents)

template_pattern = r'.*Owned by <@\d+>\n\n\*\*`[a-z0-9]+`(?: · [★☆]{1,5}){2} · #[0-9]+ · ◈[0-9]+ · [\w: ]+ · \*\*[\w ]+\*\*b.*'

settings = settings.Settings()




@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return
    if ctx.channel.id == settings.expected_channel_id:
        if ctx.embeds and (ctx.author.id == settings.karuta_bot_id and ctx.author.name == settings.karuta_bot_name or ctx.author.name == "Karuta#1280"):
            print("found embeds")
            card_info = ctx.embeds[0].to_dict()['description']

            card_print = re.search(r'#(\d+)', card_info).group(1)
            editon = re.search(r'◈(\d+)', card_info).group(1)
            owner_id = re.search(r'Owned by <@(\d+)>', card_info).group(1)
            

load_dotenv()
bot.run(os.getenv("TOKEN"))
