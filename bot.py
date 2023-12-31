import os
import re

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
discordInviteFilter = re.compile("(...)?(?:https?://)?discord(?:(?:app)?\.com/invite|\.gg)/?[a-zA-Z0-9]+/?")

def extract_card_print(post : list):
    card_print = re.search(r'#(\d+)', post[0]).group(1)
    return int(card_print)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

    
@bot.event
async def on_message(ctx : discord.context):
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
            ticket_price = await get_price(ctx, owner_id)

            if ticket_price > 0 and ticket_price != None:
                if str(editon) == "1":
                    settings.ed_one_post.append([post_info, owner_id, ticket_price])
                elif str(editon) == "2":
                    settings.ed_two_post.append([post_info, owner_id, ticket_price])
                elif str(editon) == "3":
                    settings.ed_three_post.append([post_info, owner_id, ticket_price])
                elif str(editon) == "4":
                    settings.ed_four_post.append([post_info, owner_id, ticket_price])
                elif str(editon) == "5":
                    settings.ed_five_post.append([post_info, owner_id, ticket_price])
                else:
                    settings.ed_six_post.append([post_info, owner_id, ticket_price])
                settings.save_posting()


    if discordInviteFilter.match(ctx.content) and ctx.content != settings.this_server_link  and ctx.channel.id == settings.expected_channel_id:
        await ctx.delete()
        await ctx.channel.send('no invites NOPPERS')
    
    if ctx.content.startswith("€yoi"):
        market = await create_market(ctx)
        await ctx.channel.send(embed=market)
        
# Gets price by waiting for user input
async def get_price(ctx : discord.context, ownder_id) -> int:
    def check(message):
        # return true if message id matches owner id and is in same channel
        return str(message.author.id) == str(ownder_id) and str(message.channel.id) == str(ctx.channel.id)
    
    #TODO: add timeout and make it so you have to react to message. 
    await ctx.channel.send("Respond with a price: ")
    on_message = await bot.wait_for('message', check=check)

    if on_message.content.isdigit():
        await ctx.channel.send(f"price is set at  {on_message.content}")
        return int(on_message.content)
    else:   
        await ctx.channel.send("incorrect input restart whole process")
        raise Exception("incorrect input")
    

@bot.slash_command(guild_ids=[1145481891357675582])
async def post_market(ctx):
    channel_id = settings.get_market_channel_id()  # replace with your channel id
    channel = bot.get_channel(int(channel_id))
    ed_lists = ['ed_one_post', 'ed_two_post', 'ed_three_post', 'ed_four_post', 'ed_five_post', 'ed_six_post']
    for ed_posts in ed_lists:
        market = await create_post(ctx, ed_posts, getattr(settings, ed_posts))
        await channel.send(market)




# Crates a string with post info
async def create_post(ctx: discord.context, title: str, list_of_cards: list) -> str:
    message = "### " + title + "\n"
    for card in list_of_cards:
        user = await bot.fetch_user(card[1])
        message += (f"{card[2]} :tickets: {card[0]} · Owned by: <@{user.id}>\n")
    return message


#Creates a embed with post info
async def create_market(ctx : discord.context) -> discord.Embed: 
    market = discord.Embed(title="Market", color=0x00ff00, )
    for current_post in settings.current_posting:
        user = await bot.fetch_user(current_post[1])
        market.add_field(name="Card Info", value=((f"{current_post[2]} :tickets: · {current_post[0]} Owned by: · <@{user.id}>\n")), inline=False)
    return market


@bot.slash_command(guild_ids=[1145481891357675582], name= "set-market-channel",description="Sets the channel where the market will be posted")
async def set_market_channel(ctx):
    settings.market_channel_id = ctx.channel.id
    await ctx.channel.send(f"market channel set to {settings.market_channel_id}")


@bot.slash_command(guild_ids=[1145481891357675582],
                   name= "remove-card",
                   description="Removes a listed card from the market"
                   )
async def remove_card(ctx, card_code : str):
    def extract_code(s):
        parts = s.split('·')
        code = parts[0].strip()
        code = code.replace('**', '')
        code = code.replace('`', '')
        return code
    
    # Removes a card from all lists
    ed_lists = ['ed_one_post', 'ed_two_post', 'ed_three_post', 'ed_four_post', 'ed_five_post', 'ed_six_post']
    card_removed = False
    for ed_list in ed_lists:
        for card in getattr(settings, ed_list):
            if str(extract_code(card[0])) == str(card_code):
                getattr(settings, ed_list).remove(card)    
                await ctx.channel.send(f"removed {card_code} ")
                settings.save_posting()
                card_removed = True
    if not card_removed:
        await ctx.channel.send(f"card {card_code} not found")



if __name__ == "__main__":                
    try:
        load_dotenv()
        bot.run(os.getenv("TOKEN"))
    except Exception as e:
        print(f"An error occurred: {e}")

