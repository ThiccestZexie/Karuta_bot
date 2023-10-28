import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os
from dotenv import load_dotenv


description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

class Settings:
    def __init__(self):
        self.karuta_bot_id = 646937666251915264 # Change if needed
        self.karuta_bot_name = "Karuta" # Change if needed 
        self.expected_channel_id  = 1154079321913307167 # Change if needed

   