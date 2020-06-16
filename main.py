# bot.py
import os

# import discord
# import numpy
# import math
from dotenv import load_dotenv
from discord.ext import commands
from dateutil import tz

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='cs')


@bot.command(name='userla', help="Shows the users last activity on server")
async def help_cmd(ctx):
    # for user in ctx.guild.members:
    # math.ceil(numpy.size(ctx.guild.members)/10)
    last_activity = []
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

        if last_activity:
            lastest_activity = last_activity[0]
            for activity in last_activity:
                if activity > lastest_activity:
                    lastest_activity = activity
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
            lastest_activity = lastest_activity.replace(tzinfo=from_zone)
            lastest_activity = lastest_activity.astimezone(to_zone).strftime("%d/%m/%Y, %H:%M")
            user_ls = f'User {user.mention} last activity on {lastest_activity}'
        else:
            user_ls = f'User {user.mention} has no recent activity on text channel'
        user_index += 1
        last_activity = []
        await ctx.send(user_ls)

bot.run(TOKEN)
