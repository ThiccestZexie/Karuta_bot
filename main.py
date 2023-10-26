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

mid_print = []
low_print = []
high_print = []
current_posting = []

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
            card_info_lines = card_info.split('\n')
            card_info_lines.pop(0)  # Remove the first line (Owned by)
            post_info = ''.join(card_info_lines)  # Join the remaining lines back into a string
            current_posting.append([post_info, owner_id])
    if ctx.content.startswith("€yoi"):

        market = discord.Embed(title="Market", color=0x00ff00, )
        for current_post in current_posting:
            user = await bot.fetch_user(current_post[1])
            user_mention = discord.utils.escape_markdown(user.mention)
            market.add_field(name="Card Info", value=(current_post[0] + " Owned by: " +  user_mention), inline=True)

        await ctx.channel.send(embed=market)

load_dotenv()
bot.run(os.getenv("TOKEN"))
