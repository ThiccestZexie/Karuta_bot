import os
import re
import json

import discord
from dotenv import load_dotenv

import settings
intents = discord.Intents.all()

intents.message_content = True
intents.presences = True
intents.members = True
intents.guilds = True
intents.emojis = True
intents.bans = True
intents.invites = True
intents.voice_states = True
intents.integrations = True
intents.webhooks = True
bot = discord.Bot(intents=intents)

settings = settings.Settings()


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    settings.load_posting()
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

            if ticket_price > 0 and ticket_price != None:
                settings.add_to_current_posting(post_info, owner_id, ticket_price)

        

    if ctx.content.startswith("€yoi"):
        market = discord.Embed(title="Market", color=0x00ff00, )
        for current_post in settings.current_posting:
            user = await bot.fetch_user(current_post[1])
            user_mention = discord.utils.escape_markdown(user.mention)
            market.add_field(name="Card Info", value=(current_post[0] + " Owned by:  · " +  user_mention), inline=True)

        await ctx.channel.send(embed=market)
        
# Gets price by waiting for user input
async def get_price(ctx, ownder_id):
    def check(message):
        # return true if message id matches owner id and is in same channel
        return str(message.author.id) == str(ownder_id) and str(message.channel.id) == str(ctx.channel.id)
    
    await ctx.channel.send("Please send me a message")
    on_message = await bot.wait_for('message', check=check)

    if on_message.content.isdigit():
        await ctx.channel.send(f"price is set at  {on_message.content}")
        return int(on_message.content)
    else:   
        await ctx.channel.send("incorrect input restart whole process")
        raise Exception("incorrect input")



@bot.slash_command(guild_ids=[1145481891357675582])
async def hello(ctx):
    await ctx.respond("Hello!")



try:
    load_dotenv()
    bot.run(os.getenv("TOKEN"))
except Exception as e:
    print(f"An error occurred: {e}")