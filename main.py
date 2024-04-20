import os
import discord
from discord.ext import commands
import google.generativeai as genai
import asyncio
import random
import requests
import tabulate


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

  if message.content.startswith("!ask"):
    subject = message.content[5:]
    convo.send_message(subject)
    response = (convo.last.text)
    await message.channel.send(response)
    
  
  if message.content.startswith('!quiz'):


    responses.clear()
    topic = message.content[6:]
    convo.send_message(f"Generate an MCQ question on the topic {topic} with only 4 options. Don't repeat the same question too many times.")
    question = convo.last.text
    await message.channel.send(question)
    convo.send_message(f"which is the correct option(just say A, B, C or D)?\n{question}. Do not bold it. After you state the correct option, briefly explain the answer.")
    answer = convo.last.text
    correct_option = answer[0]
    correct_option = correct_option.lower()
    print(correct_option)
    await message.channel.send("You have 20 seconds to answer this, good luck!")
    await asyncio.sleep(20)
    await message.channel.send(f"The correct option is : {answer}")

    if correct_option not in responses.values():
      await message.channel.send(":frowning: No one got the right answer. Better luck next time!")
      sad_gif_choice = (random.randint(1, 5))
      if sad_gif_choice == 1:
        await message.channel.send("https://giphy.com/gifs/spongebob-squarepants-sad-OPU6wzx8JrHna")

      if sad_gif_choice == 2:
        await message.channel.send("https://giphy.com/gifs/blackish-anthony-anderson-dre-johnson-d2lcHJTG5Tscg")

      if sad_gif_choice == 3:
        await message.channel.send("https://giphy.com/gifs/house-boyfriends-qQdL532ZANbjy")

      if sad_gif_choice == 4:
        await message.channel.send("https://giphy.com/gifs/inside-out-gif-10tIjpzIu8fe0")

      if sad_gif_choice == 5:
        await message.channel.send("https://giphy.com/gifs/sesamestreet-oscar-sesame-street-the-grouch-XRSSo3az6LHkOQFs0O")

     

    else:
      val_list= list(responses.values())
      key_list = list(responses.keys())
      position = val_list.index(correct_option)
      winner = key_list[position]
      await message.channel.send(f"\n**Congratulations {winner}! You got the right answer!**:tada:")
      leaderboard.update({winner : leaderboard.get(winner, 0) + 1})
      w_gif_choice = (random.randint(1, 5))
      if w_gif_choice == 1:
        await message.channel.send("https://giphy.com/gifs/moodman-Q81NcsY6YxK7jxnr4v")

      if w_gif_choice == 2:
        await message.channel.send("https://giphy.com/gifs/mr-gif-9Ai5dIk8xvBm0")

      if w_gif_choice == 3:
        await message.channel.send("https://giphy.com/gifs/approval-approve-13zeE9qQNC5IKk")

      if w_gif_choice == 4:
        await message.channel.send("https://giphy.com/gifs/spongebob-cartoon-nickelodeon-thumbs-3o7abGQa0aRJUurpII")

      if w_gif_choice == 5:
        await message.channel.send("https://giphy.com/gifs/Friends-episode-1-season-9-friends-tv-mGK1g88HZRa2FlKGbz")
    
  if message.content.startswith('!leaderboard'):
    sorted_dict = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True
    await message.channel.send("\t\t\t***LEADERBOARD***\n" + leaderboard)

  if message.content.startswith('!translate'):

    mssg = message.content
    language = mssg.split()[1]
    lang_index = mssg.find(language)
    text = mssg[lang_index+len(language)+1:]
    
    convo.send_message(f"Translate the : {text} into the language {language}. After giving the text, in brackets add the pronounciation of the text")
    translation = convo.last.text
    await message.channel.send(translation)
                       
  if message.content.startswith('!news'):
     
    query_params = {
      "source": "bbc-news",
      "sortBy": "top",
      "apiKey": "0448e25fef724b4ba156c7cd22aeb7f9"
      
    }
    
    main_url = " https://newsapi.org/v1/articles"
    res = requests.get(main_url, params=query_params)
    open_bbc_page = res.json()

    article = open_bbc_page["articles"]
 
    results = []
     
    for ar in article:
        results.append(ar["title"])
         
    for i in range(len(results)):
         
       
        await message.channel.send(f"{i + 1}. {results[i]}")
 

  if message.content.startswith('!help') :
    await message.channel.send("**Commands:**\n!ask <question> - asks Google's AI (Gemini) \n!quiz <topic> - asks Gemini to generate a multiple choice question on the topic \n!answer<option> Answer the question that Gemini asked you, compete with your friends, first one to answer gets a point! \n!leaderboard - shows the leaderboard\n!translate <language> <text> - translates the text into the language you specify\n!news - shows the top headlines from BBC news") 

bot.run(DiscordToken)

  