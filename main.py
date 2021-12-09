import discord
import os
import time
import calendar
from datetime import datetime, timezone, timedelta
import random
from discord.ext import commands
from keep_alive import keep_alive

class User:

    name = ''

    #tasks = []

    def __init__(self, name):
        self.name = name
        self.tasks = []
        self.workTime = 1500
        self.breakTime = 300
        self.numCycles = 3

    def add(self, task):
        self.tasks.append(task)

    def view(self):
        if (len(self.tasks) == 0):
            return 'No tasks available. Add tasks and get working!'
        tasks = ''
        for i in range(len(self.tasks)):
            tasks += str(i + 1) + ': ' + self.tasks[i] + '\n'
        return tasks

    def remove(self, i):
        try:
            if (int(i) != -1):
                i = int(i)
                if (i <= len(self.tasks)):
                    x = self.tasks.pop(i - 1)
                    return x
                else:
                    return 'index not found'
        except:
            if (i in self.tasks):
                x = self.tasks[self.tasks.index(i)]
                self.tasks.remove(i)
                return x
            else:
                return 'item not found'

    def changeWorkTime(self, time):
        self.workTime = 60 * float(time)

    def changeBreakTime(self, time):
        self.breakTime = 60 * float(time)

    def changeCycles(self, numCycles):
        self.numCycles = int(numCycles)


userList = []

intents = discord.Intents.default()
intents.members = True
#client = discord.Client()
bot = commands.Bot(command_prefix='$', intents=intents)


#@client.event
@bot.command()
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


breakList = [
    "You can take a break now!",
    "You are a machine! Good job working through the time.", "Take a break!",
    "Congratulations, you made it through!"
]
workList = [
    "It's about drive. It's about power. We stay hungry. We devor. Put in the work. Put in the hours, and take what's ours."
]


def getTime():
    tzInfo = timezone(-timedelta(hours=5))
    return datetime.now(tzInfo).strftime(" %I:%M%p")


@bot.command()
async def name(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def bothelp(ctx):
    embed = discord.Embed(title="Commands",
                          color=discord.Colour.from_rgb(255, 192, 203))
    embed.add_field(
        name="Timer",
        value=
        "**setup** [no parameters] *must be done once added to server* \n**start** [no parameters] \n**set** [work time (in minutes)] [break time (in minutes)] [number of cycles]",
        inline=True)
    embed.add_field(
        name="Tasks",
        value=
        "**view** [no parameters] \n**add** [name of task] \n**remove** [name of task]"
    )
    await ctx.send(embed=embed)


@bot.command()
async def gettime(ctx):
    await ctx.send(getTime())


@bot.command()
async def start(ctx):
    await ctx.send("Clock start: Start working!")
    await ctx.send(getTime())
    user = findUser(ctx.author.name)
    for i in range(user.numCycles):
        time.sleep(user.workTime)
        await ctx.send(ctx.author.mention + " " + random.choice(breakList))
        await ctx.send(getTime())
        if (i % 3 == 0):
            time.sleep(user.breakTime * 3)
            await ctx.send(ctx.author.mention + " " + random.choice(workList))
            await ctx.send(getTime())
        else:
            time.sleep(user.breakTime)
            await ctx.send(ctx.author.mention + " " + random.choice(workList))
            await ctx.send(getTime())


@bot.command()
async def set(ctx, workTime, breakTime, numCycles):
    await ctx.send("Clock start: Start working!")
    await ctx.send(getTime())
    user = findUser(ctx.author.name)
    user.changeWorkTime(workTime)
    user.changeBreakTime(breakTime)
    user.changeCycles(numCycles)
    for i in range(user.numCycles):
        time.sleep(user.workTime)
        await ctx.send(ctx.author.mention + " " + random.choice(breakList))
        await ctx.send(getTime())
        if (i % 3 == 0 and i != 0):
            time.sleep(user.breakTime * 3)
            await ctx.send(ctx.author.mention + " " + random.choice(workList))
            await ctx.send(getTime())
        else:
            time.sleep(user.breakTime)
            await ctx.send(ctx.author.mention + " " + random.choice(workList))
            await ctx.send(getTime())


def findUser(name):
    for i in range(len(userList)):
        if (userList[i].name == name):
            return userList[i]


@bot.command()
async def view(ctx):
    user = findUser(ctx.author.name)
    await ctx.send(user.view())
    #for i in range(len(user.tasks)):
    #await ctx.send(user.viewTasks())


@bot.command()
async def add(ctx, *, args):
    user = findUser(ctx.author.name)
    user.add(args)
    await ctx.send("Added successfully!")
    await ctx.send("Your tasks are: \n" + user.view())



@bot.command()
async def remove(ctx, *, args):
    user = findUser(ctx.author.name)
    await ctx.send(str(user.remove(args)) + ' removed')
    await ctx.send("Your tasks are: \n" + user.view())


@bot.command()
async def setup(ctx):
    guild = ctx.guild
    async for user in guild.fetch_members():
        await ctx.send(user)
        print(user.name)
        name = str(user.name)
        x = User(name)
        userList.append(x)


@bot.command()
async def test(ctx):
    for i in range(len(userList)):
        await ctx.send(userList[i].name)
    print(len(userList))


# keep_alive()
bot.run(os.getenv('TOKEN'))
