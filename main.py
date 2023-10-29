# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os
from dotenv import load_dotenv
import settings
import re
import json

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='€', description=settings.description, intents=intents)

mid_print = []
low_print = []
high_print = []
current_posting = []
template = r"^.*kv [A-Za-z0-9]{3,10} [0-9]{1,3}.*$"
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
            ticket_price =await get_price(ctx, owner_id)
    if ticket_price > 0:
          current_posting.append([post_info, owner_id, ticket_price])
            
    if ctx.content.startswith("€yoi"):
        market = discord.Embed(title="Market", color=0x00ff00, )
        for current_post in current_posting:
            user = await bot.fetch_user(current_post[1])
            user_mention = discord.utils.escape_markdown(user.mention)
            market.add_field(name="Card Info", value=("price: " + current_post[2] + current_post[0] + " Owned by:  · " +  user_mention), inline=True)

        await ctx.channel.send(embed=market)
        
# Gets price by waiting for 
@bot.command()
async def get_price(ctx, ownder_id):
    def check(message):
        # return true if message id matches owner id and is in same channel
        return str(message.author.id) == str(ownder_id) and str(message.channel.id) == str(ctx.channel.id)
    
    await ctx.channel.send("Please send me a message")
    on_message = await bot.wait_for('message', check=check)

    if re.match(str(r'^[0,9]{1,4}'), str(on_message)):
        await ctx.channel.send(f"price is set at  {on_message.content}")
        return int(on_message.content)
    else:   
        await ctx.channel.send("incorrect input restart whole process")
        return None

async def save_market():
    #uses the current_posting to iterate through all the nested lists and save them under catagories in a .txt file so they can be read on bot initialization later.
    

    async def save_market():
        with open('market.json', 'w') as f:
            json.dump({'current_posting': current_posting}, f)

try:
    load_dotenv()
    bot.run(os.getenv("TOKEN"))
except Exception as e:
    print(f"An error occurred: {e}")
