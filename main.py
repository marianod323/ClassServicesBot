# bot.py
import os

# import discord
# import numpy
# import math
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='cs')


@bot.command(name='userla', help="Shows the users last activity on server")
async def help_cmd(ctx):
    # for user in ctx.guild.members:
    # math.ceil(numpy.size(ctx.guild.members)/10)
    last_activity = []
    lastest_activity = []
    channel_index = 0
    user_index = 0
    for user in ctx.guild.members:
        for channel in ctx.guild.channels:
            if channel.type[0] == 'text':
                async for message in channel.history(limit=150):
                    if message.author == user:
                        last_activity.append(message.created_at)
                        break
                channel_index += 1
        lastest_activity.insert(user_index, last_activity[0])
        for activity in last_activity:
            if activity > lastest_activity[user_index]:
                lastest_activity.insert(user_index, activity)
        user_ls = f'User {user} last activity on {lastest_activity[user_index]}'
        last_activity = []
        user_index += 1
        await ctx.send(user_ls)
        break

bot.run(TOKEN)
