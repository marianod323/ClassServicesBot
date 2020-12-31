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
    num_pages = math.ceil(numpy.size(ctx.guild.members) / 10)
    offset = (10 * (actual_page - 1))
    max_index = 10 * actual_page
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
            lastest_activity = lastest_activity.astimezone(to_zone).strftime(
                language.find("command[@name='userla']/item[@type='date']").text)
            user_la += f'**{user.display_name}** ' + \
                       language.find(
                           "command[@name='userla']/item[@type='field1_content']").text + f' {lastest_activity}\n'
        else:
            user_la += f'**{user.display_name}** ' + \
                       language.find("command[@name='userla']/item[@type='field2_content']") + '\n'
        user_index += 1
        last_activity = []
    embed = discord.Embed(title=language.find("command[@name='userla']/item[@type='title']").text, color=0x85fd2c)
    embed.add_field(name=language.find("command[@name='userla']/item[@type='field1_name']").text,
                    value=user_la, inline=False)
    embed.add_field(name=language.find("command[@name='userla']/item[@type='field2_name']").text,
                    value=f'{actual_page}/{num_pages}', inline=False)
    embed.add_field(name=language.find("command[@name='userla']/item[@type='field3_name']").text,
                    value=language.find("command[@name='userla']/item[@type='field3_content']").text, inline=False)
    await ctx.send(embed=embed)


@userla.error
async def userla_error(ctx, error):
    pref_handler = PrefHandler(ctx.guild.id)
    language = pref_handler.get_lang()

    embed = discord.Embed(title=language.find("command[@name='userla_error']/item[@type='title']").text, color=0x85fd2c)
    embed.add_field(name=language.find("command[@name='userla_error']/item[@type='field1_name']").text,
                    value=language.find("command[@name='userla_error']/item[@type='field1_content']").text, inline=False)
    embed.add_field(name=language.find("command[@name='userla_error']/item[@type='field2_name']").text,
                    value=language.find("command[@name='userla_error']/item[@type='field2_content']").text, inline=False)
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
    embed = discord.Embed(title=language.find("command[@name='usercount']/item[@type='title']").text, color=0x85fd2c)
    embed.add_field(name=language.find("command[@name='usercount']/item[@type='field1_name']").text,
                    value=str(users_count), inline=False)
    embed.add_field(name=language.find("command[@name='usercount']/item[@type='field2_name']").text,
                    value=str(bot_count), inline=False)
    await ctx.send(embed=embed)


@bot.command(name='setlang')
async def setlang(ctx):
    await ctx.send('oi')


@bot.command(name='help')
async def help(ctx):
    pref_handler = PrefHandler(ctx.guild.id)
    language = pref_handler.get_lang()
    prefix = language.find("command[@name='help']/item[@type='prefix']").text
    embed = discord.Embed(title=language.find("command[@name='help']/item[@type='title']").text, color=0x85fd2c)
    embed.add_field(name=language.find("command[@name='help']/item[@type='field1_name']").text,
                    value=language.find("command[@name='help']/item[@type='field1_content']").text, inline=False)
    embed.add_field(name=prefix + language.find("command[@name='help']/item[@type='field2_name']").text,
                    value=language.find("command[@name='userla']/item[@type='help']").text, inline=False)
    embed.add_field(name=prefix + language.find("command[@name='help']/item[@type='field3_name']").text,
                    value=language.find("command[@name='usercount']/item[@type='help']").text, inline=False)
    embed.add_field(name=prefix + language.find("command[@name='help']/item[@type='field4_name']").text,
                    value=language.find("command[@name='help']/item[@type='help']").text, inline=False)
    await ctx.send(embed=embed)


bot.run(TOKEN)
