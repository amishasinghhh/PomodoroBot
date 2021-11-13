import discord
import os
import time
import calendar
from datetime import datetime, timezone, timedelta
import random

#timezone = 
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

breakList = ["You can take a break now!", "25 minutes of work are up! Take a break.", "Congratulations, you made it through 25 minutes!"] 
workList = ["It's about drive. It's about power. We stay hungry. We devor. Put in the work. Put in the hours, and take what's ours."]




@client.event
async def on_message(message):
    def getTime():
      tzInfo = timezone(-timedelta(hours = 5))
      return datetime.now(tzInfo).strftime(" %I:%M%p")
    if message.author == client.user:
        return
    if message.content.startswith('$'):
      fullMessage=""
      args = message.content.split("$")
      for x in args:
        fullMessage+=x
    if fullMessage == "time":
      await message.channel.send(getTime())
      #Returns TIMEEEEE
    if fullMessage == "start":
      await message.channel.send("Clock start")
      await message.channel.send(getTime())
      time.sleep(5)
      #await message.channel.send(message.author.mention + " " + random.choice(breakList))
      #await message.channel.send(getTime())
      time.sleep(5)
      await message.channel.send(message.author.mention  + " " + random.choice(workList))
      time.sleep(5)
      await message.channel.send(message.author.mention + " " + random.choice(breakList))
    if fullMessage == "test":
      print(message.author)



#commands

      #if fullMessage=

client.run(os.getenv('TOKEN'))