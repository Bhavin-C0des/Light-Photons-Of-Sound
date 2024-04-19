import os
import discord
from discord.ext import commands
import google.generativeai as genai
import asyncio

genai_token = os.environ['genai_token']
DiscordToken = os.environ['DiscordToken']

genai.configure(api_key=genai_token)

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}


model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config)

convo = model.start_chat(history=[
])

  
intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event  
async def on_ready():
  print ("Connection established")

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  print(f'{message.author}: {message.content}')

  if message.content.startswith('!quiz'):
  
    topic = message.content[6:]
    convo.send_message(f"Generate an MCQ question on the topic {topic}")
    question = convo.last.text
    print(convo.last.text)
    await message.channel.send(question)

    convo.send_message(f"which is the correct option(just say a, b, c or d)?\n{question}. Dont format or bold the text.")
    print(convo.last.text)
    
  
bot.run(DiscordToken)
    



  