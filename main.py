import os
import discord
from discord.ext import commands
import openai
import asyncio


OpenAI_API = os.environ['OpenAIAPI']
DiscordToken = os.environ['DiscordToken']

intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event  
async def on_ready():
  print ("Connection established")

async def on_message(message):
  if message.author == bot.user:
    return
  print(f'{message.author}: {message.content}')
  
bot.run(DiscordToken)
    



  