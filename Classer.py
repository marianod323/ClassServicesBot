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
bot.remove_command('help')


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


@bot.command(name='usercount')
async def usercount(ctx):
    users_count = 0
    bot_count = 0
    members = ctx.guild.members
    pref_handler = PrefHandler(ctx.guild.id)
    language = pref_handler.get_lang()
    for user in members:
        if user.bot:
            bot_count += 1
        else:
            users_count += 1
    embed = discord.Embed(title=language[2][0].text, color=0x85fd2c)
    embed.add_field(name=language[2][2].text, value=str(users_count), inline=False)
    embed.add_field(name=language[2][3].text, value=str(bot_count), inline=False)
    await ctx.send(embed=embed)


@bot.command(name='help')
async def help(ctx):
    pref_handler = PrefHandler(ctx.guild.id)
    language = pref_handler.get_lang()
    embed = discord.Embed(title=language[3][0].text, color=0x85fd2c)
    embed.add_field(name=language[3][3].text, value=language[3][4].text, inline=False)
    embed.add_field(name=language[3][2].text+language[3][5].text, value=language[0][1].text, inline=False)
    embed.add_field(name=language[3][2].text+language[3][6].text, value=language[2][1].text, inline=False)
    embed.add_field(name=language[3][2].text+language[3][7].text, value=language[3][1].text, inline=False)
    await ctx.send(embed=embed)


bot.run(TOKEN)
