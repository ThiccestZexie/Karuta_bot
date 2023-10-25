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
path = "ids.txt"
bot = commands.Bot(command_prefix='€', description=description, intents=intents)

user_ids = []


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

    with open(path, 'r') as f:
         for line in f:
            user_ids.append(int(line))
    for user_id in user_ids:
        user = await bot.fetch_user(user_id)
        print(f" {user} has the id: {user_id}")

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.event
async def on_message(ctx):
    if "I'm dropping 3 cards since" in ctx.content:
        print("Sending DM...")
        channel = ctx.channel
        await send_dm(ctx, message=f"A server drop is happening! In https://discord.com/channels/1145481891357675582/1146524168800698470")
    if "€add" in ctx.content.lower():
        print("Adding ID...")
        if ctx.author.id in user_ids:
            print("ID already in list!")
            return
        if ctx.author.id not in user_ids:
            with open('ids.txt', 'a') as file:
                file.write(str(ctx.author.id) + "\n")
        user_ids.append(ctx.author.id)

        user = await bot.fetch_user(ctx.author.id)
        print(f" {user} has the id: {ctx.author.id}")
        await ctx.channel.send("You have been added to the list!")
    if "€remove" == ctx.content.lower():
        print("Removing ID...")
        user_ids.remove(ctx.author.id)
        with open('ids.txt', 'r') as file:
            lines = file.readlines()
        new_file = []

        for line in lines:
            if line.strip("\n") != str(ctx.author.id):
                new_file.append(line)

        with open('ids.txt', 'w') as file:
            file.writelines(new_file)

        for user_id in user_ids:
            user = await bot.fetch_user(user_id)
            print(f" {user} has the id: {user_id}")

    if "€funny"  in ctx.content.lower():
        f = r"https://official-joke-api.appspot.com/random_joke"
        a = jokes(f)
        print("Sending joke...")

        await ctx.channel.send(a["setup"])
        await ctx.channel.send(a["punchline"])


    if "€check" in ctx.content.lower():
        if ctx.author.id in user_ids:
            await ctx.channel.send("You are in the list!")
        else:
            await ctx.channel.send("You are not in the list!")
    if "€list" in ctx.content.lower():
        for user_id in user_ids:
            user = await bot.fetch_user(user_id)
            print(f" {user} has the id: {user_id}")
    if "x)" in ctx.content.lower():
        user = await bot.fetch_user(ctx.author.id)
        await ctx.channel.send("xD* " + user.mention)
    if "€help" in ctx.content.lower():
        embed = discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/",
                              description="This is an embed that will show how to build an embed and the different components",
                              color=0xFF5733)
        await ctx.channel.send(embed=embed)
    else:
        return

@bot.command("add", help="Adds your ID to the list of people to DM when a server drop happens")
async def add(ctx): 
    if "€add" in ctx.content.lower():
        print("Adding ID...")
        if ctx.author.id in user_ids:
            print("ID already in list!")
            return
        if ctx.author.id not in user_ids:
            with open('ids.txt', 'a') as file:
                file.write(str(ctx.author.id) + "\n")
        user_ids.append(ctx.author.id)

        user = await bot.fetch_user(ctx.author.id)
        print(f" {user} has the id: {ctx.author.id}")
        await ctx.channel.send("You have been added to the list!")

@bot.event
async def send_dm(ctx, *, message):
    for user_id in user_ids:
        user = bot.get_user(user_id)
        try:
            await user.send(message)
            print(f'Sent DM to {user.name} ({user.id}): {message}')
        except Exception as e:
            print(f'Failed to send DM to {user.name} ({user.id}): {str(e)}')


@bot.command()
async def shutdown(ctx):
    print("yatta")
    await ctx.bot.close()


def jokes(f):
    data = requests.get(f)
    tt = json.loads(data.text)
    return tt


load_dotenv()
bot.run(os.getenv("TOKEN"))
