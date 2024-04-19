import os
import discord
from discord.ext import commands
import google.generativeai as genai
import asyncio

genai_token = os.environ['genai_token']
DiscordToken = os.environ['DiscordToken']

leaderboard = {}
responses = {}

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

  if message.content.startswith('!answer'):
    global guess
    global guesser
    guesser = message.author
    guess = message.content[8]
    print(f"{guesser} guessed {guess}")
    responses.update({str(guesser) : guess})

  if message.content.startswith('!quiz'):

    responses.clear()
    topic = message.content[6:]
    convo.send_message(f"Generate an MCQ question on the topic {topic} with only 4 options")
    question = convo.last.text
    await message.channel.send(question)
    convo.send_message(f"which is the correct option(just say A, B, C or D)?\n{question}. Do not bold it. After you state the correct option, briefly explain the answer.")
    answer = convo.last.text
    correct_option = answer[0]
    correct_option = correct_option.lower()
    print(correct_option)
    await message.channel.send("You have 30 seconds to answer this, good luck!")
    await asyncio.sleep(30)
    await message.channel.send(f"The correct option is : {answer}")

    if correct_option not in responses.values():
      await message.channel.send(":( No one got the right answer. Better luck next time!")

    else:
      val_list= list(responses.values())
      key_list = list(responses.keys())
      position = val_list.index(correct_option)
      winner = key_list[position]
      await message.channel.send(f"\n**Congratulations {winner}! You got the right answer!**:tada:")
        
    
    
  
bot.run(DiscordToken)
    



  