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
                          color=discord.Colour.from_rgb(88, 101, 242))
    embed.add_field(
        name="Timer",
        value=
        "`$setup` must be done once added to server \n`$start` starts timer with either default or custom settings \n`$set [work time in minutes] [break time in minutes] [number of cycles]` allows user to set custom times",
        inline=True)
    embed.add_field(
        name="Tasks",
        value=
        "`$view` displays list of current tasks\n`$add [name of task]` adds task to current list of tasks\n`$remove [name of task]` removes task from current list of tasks"
    )
    await ctx.send(embed=embed)


@bot.command()
async def gettime(ctx):
    await ctx.send(getTime())


@bot.command()
async def start(ctx):
    startEmbed = discord.Embed(title="Clock start: Start working!",
                          color=discord.Colour.from_rgb(88, 101, 242))
    startEmbed.add_field(
        name="The time right now is:",
        value=getTime(),
        inline=True)
    await ctx.send(embed=startEmbed)
    user = findUser(ctx.author.name)
    for i in range(user.numCycles):
        time.sleep(user.workTime)
        breakTimeEmbed = discord.Embed(title="Break time!", color=discord.Colour.from_rgb(88, 101, 242))
        breakTimeEmbed.add_field(
        name=random.choice(breakList),
        value="The time right now is " + str(getTime()),
        inline=True)
        await ctx.send(ctx.author.mention)
        await ctx.send(embed=breakTimeEmbed)
        workTimeEmbed = discord.Embed(title="Work time!", color=discord.Colour.from_rgb(88, 101, 242))
        workTimeEmbed.add_field(
        name=random.choice(workList),
        value="The time right now is " + str(getTime()),
        inline=True)
        if (i % 3 == 0):
            time.sleep(user.breakTime * 3)
            await ctx.send(ctx.author.mention)
            await ctx.send(embed=workTimeEmbed)
        else:
            time.sleep(user.breakTime)
            await ctx.send(ctx.author.mention)
            await ctx.send(embed=workTimeEmbed)


@bot.command()
async def set(ctx, workTime, breakTime, numCycles):
    startEmbed = discord.Embed(title="Clock start: Start working!",
                          color=discord.Colour.from_rgb(88, 101, 242))
    startEmbed.add_field(
        name="The time right now is:",
        value=getTime(),
        inline=True)
    await ctx.send(embed=startEmbed)
    user = findUser(ctx.author.name)
    user.changeWorkTime(workTime)
    user.changeBreakTime(breakTime)
    user.changeCycles(numCycles)
    for i in range(user.numCycles):
        time.sleep(user.workTime)
        breakTimeEmbed = discord.Embed(title="Break time!", color=discord.Colour.from_rgb(88, 101, 242))
        breakTimeEmbed.add_field(
        name=random.choice(breakList),
        value="The time right now is " + str(getTime()),
        inline=True)
        await ctx.send(ctx.author.mention)
        await ctx.send(embed=breakTimeEmbed)
        workTimeEmbed = discord.Embed(title="Work time!", color=discord.Colour.from_rgb(88, 101, 242))
        workTimeEmbed.add_field(
        name=random.choice(workList),
        value="The time right now is " + str(getTime()),
        inline=True)
        if (i % 3 == 0 and i != 0):
            time.sleep(user.breakTime * 3)
            await ctx.send(ctx.author.mention)
            await ctx.send(embed=workTimeEmbed)
        else:
            time.sleep(user.breakTime)
            await ctx.send(ctx.author.mention)
            await ctx.send(embed=workTimeEmbed)


def findUser(name):
    for i in range(len(userList)):
        if (userList[i].name == name):
            return userList[i]


@bot.command()
async def view(ctx):
    user = findUser(ctx.author.name)
    viewEmbed = discord.Embed(title="Here's a list of your tasks!",
                          color=discord.Colour.from_rgb(88, 101, 242))
    viewEmbed.add_field(
        name="Tasks:",
        value=user.view(),
        inline=True)
    await ctx.send(embed=viewEmbed)
    #for i in range(len(user.tasks)):
    #await ctx.send(user.viewTasks())


@bot.command()
async def add(ctx, *, args):
    user = findUser(ctx.author.name)
    user.add(args)
    viewEmbed = discord.Embed(title="Task added successfully!",
                          color=discord.Colour.from_rgb(88, 101, 242))
    viewEmbed.add_field(
        name="Tasks:",
        value=user.view(),
        inline=True)
    await ctx.send(embed=viewEmbed)
    #await ctx.send("Added successfully!")
    #await ctx.send("Your tasks are: \n" + user.view())



@bot.command()
async def remove(ctx, *, args):
    user = findUser(ctx.author.name)
    user.remove(args)
    viewEmbed = discord.Embed(title="Task removed successfully!",
                          color=discord.Colour.from_rgb(88, 101, 242))
    viewEmbed.add_field(
        name="Tasks:",
        value=user.view(),
        inline=True)
    await ctx.send(embed=viewEmbed)


@bot.command()
async def setup(ctx):
    guild = ctx.guild
    userListText=""
    async for user in guild.fetch_members():
        print(user.name)
        name = str(user.name)
        x = User(name)
        userList.append(x)
        userListText+=name
        userListText+="\n"
    embed = discord.Embed(title="Setup complete!",
                          color=discord.Colour.from_rgb(88, 101, 242))
    embed.add_field(
        name="Created profiles for:",
        value=userListText,
        inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def test(ctx):
    for i in range(len(userList)):
        await ctx.send(userList[i].name)
    print(len(userList))


# keep_alive()
bot.run(os.getenv('TOKEN'))
