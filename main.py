# bot.py
import os

import discord
import numpy
import math
from dotenv import load_dotenv
from discord.ext import commands
from dateutil import tz

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='cs')


@bot.command(name='userla', help="Shows the users last activity on server")
async def userla(ctx, actual_page: int):
    last_activity = []
    channel_index = 0
    user_index = 0
    user_la = f""
    num_pages = math.ceil(numpy.size(ctx.guild.members)/10)
    offset = (10*(actual_page-1))
    max_index = 10*actual_page
    members = ctx.guild.members[offset:max_index]
    for user in members:
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
            user_la += f'**{user.display_name}** last activity on {lastest_activity}\n'
        else:
            user_la += f'**{user.display_name}** has no recent activity on text channel\n'
        user_index += 1
        last_activity = []
    embed = discord.Embed(title="Users last activity", color=0x85fd2c)
    embed.add_field(name="User", value=user_la, inline=False)
    embed.add_field(name="Page", value=f'{actual_page}/{num_pages}', inline=False)
    embed.add_field(name="Help", value='To navigate through pages, use **csuserla _PAGE\_NUMBER_**', inline=False)
    await ctx.send(embed=embed)


@userla.error
async def userla_error(ctx, error):
    embed = discord.Embed(title="Oops...", color=0x85fd2c)
    embed.add_field(name="Error", value="I've found an error on handling your request,"
                                        " maybe you forgot to specify the page?", inline=False)
    embed.add_field(name="Help", value='To navigate through pages, use **csuserla _PAGE\_NUMBER_**', inline=False)
    await ctx.send(embed=embed)

bot.run(TOKEN)
