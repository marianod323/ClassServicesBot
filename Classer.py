# bot.py
import discord
import numpy
import math
from dotenv import load_dotenv
from discord.ext import commands
from dateutil import tz
from PrefHandler import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='cs-')


@bot.command(name='userla')
async def userla(ctx, actual_page: int):
    pref_handler = PrefHandler(ctx.guild.id)
    server_timezone = pref_handler.get_timezone()
    language = pref_handler.get_lang()
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
            lastest_activity = lastest_activity.astimezone(to_zone).strftime(language[0][2].text)
            user_la += f'**{user.display_name}** '+language[0][4].text+f' {lastest_activity}\n'
        else:
            user_la += f'**{user.display_name}** '+language[0][6].text+'\n'
        user_index += 1
        last_activity = []
    embed = discord.Embed(title=language[0][0].text, color=0x85fd2c)
    embed.add_field(name=language[0][3].text, value=user_la, inline=False)
    embed.add_field(name=language[0][5].text, value=f'{actual_page}/{num_pages}', inline=False)
    embed.add_field(name=language[0][7].text, value=language[0][8].text, inline=False)
    await ctx.send(embed=embed)


@userla.error
async def userla_error(ctx, error):
    pref_handler = PrefHandler(ctx.guild.id)
    language = pref_handler.get_lang()

    embed = discord.Embed(title=language[1][0].text, color=0x85fd2c)
    embed.add_field(name=language[1][1].text, value=language[1][2].text, inline=False)
    embed.add_field(name=language[1][3].text, value=language[1][4].text, inline=False)
    await ctx.send(embed=embed)

bot.run(TOKEN)
