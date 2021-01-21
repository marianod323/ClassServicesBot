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
            to_zone = tz.gettz('Etc/GMT' + server_timezone)
            lastest_activity = lastest_activity.replace(tzinfo=from_zone)
            lastest_activity = lastest_activity.astimezone(to_zone).strftime(
                language.find("command[@name='userla']/item[@type='date']").text)
            user_la += f'**{user.display_name}** ' + \
                       language.find(
                           "command[@name='userla']/item[@type='field1_content']").text + f' {lastest_activity}\n'
        else:
            user_la += f'**{user.display_name}** ' + \
                       language.find("command[@name='userla']/item[@type='field2_content']").text + '\n'
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
    strings = [language.find("error[@name='userla_error']/item[@type='title']").text,
               language.find("error[@name='userla_error']/item[@type='field1_name']").text,
               language.find("error[@name='userla_error']/item[@type='field1_content']").text,
               language.find("error[@name='userla_error']/item[@type='field2_name']").text,
               language.find("error[@name='userla_error']/item[@type='field2_content']").text]

    embed = discord.Embed(title=strings[0], color=0x85fd2c)
    embed.add_field(name=strings[1], value=strings[2], inline=False)
    embed.add_field(name=strings[3], value=strings[4], inline=False)
    await ctx.send(embed=embed)


@bot.command(name='usercount')
async def usercount(ctx):
    strings = getusercountstrings(ctx)

    embed = discord.Embed(title=strings[0], color=0x85fd2c)
    embed.add_field(name=strings[1], value=strings[2], inline=False)
    embed.add_field(name=strings[3], value=strings[4], inline=False)
    await ctx.send(embed=embed)


def getusercountstrings(ctx):
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
    strings = [language.find("command[@name='usercount']/item[@type='title']").text,
               language.find("command[@name='usercount']/item[@type='field1_name']").text,
               str(users_count),
               language.find("command[@name='usercount']/item[@type='field2_name']").text,
               str(bot_count)]
    return strings


@bot.command(name='setlang')
async def setlang(ctx, language_to_set):
    pref_handler = PrefHandler(ctx.guild.id)
    language = pref_handler.get_lang()
    embed = discord.Embed(title=language.find("command[@name='setlang']/item[@type='title']").text, color=0x85fd2c)
    if (pref_handler.get_role() in list(
            role.name.lower() for role in ctx.author.roles)) or ctx.author.guild_permissions.administrator:
        if language_to_set == 'help':
            embed.add_field(name=language.find("command[@name='help']/item[@type='title']").text,
                            value=language.find("command[@name='setlang']/item[@type='howto']").text, inline=False)
            for command, lang in pref_handler.languages.items():
                embed.add_field(name=command, value=lang, inline=False)

        elif pref_handler.set_lang(language_to_set):
            embed.add_field(name=language.find("command[@name='setlang']/item[@type='success_title']").text,
                            value=language.find("command[@name='setlang']/item[@type='success']").text, inline=False)
    else:
        embed.add_field(name=language.find("command[@name='setrole']/item[@type='fail_title']").text,
                        value=language.find("command[@name='setrole']/item[@type='fail']").text, inline=False)
    await ctx.send(embed=embed)


@bot.command(name='settz')
async def settz(ctx, tz_to_set):
    pref_handler = PrefHandler(ctx.guild.id)
    language = pref_handler.get_lang()
    embed = discord.Embed(title=language.find("command[@name='settz']/item[@type='title']").text, color=0x85fd2c)
    if (pref_handler.get_role() in list(
            role.name.lower() for role in ctx.author.roles)) or ctx.author.guild_permissions.administrator:
        if tz_to_set == 'help':
            embed.add_field(name='', value='', inline=False)
        if pref_handler.set_timezone(tz_to_set):
            embed.add_field(name=language.find("command[@name='settz']/item[@type='success_title']").text,
                            value=language.find("command[@name='settz']/item[@type='success']").text, inline=False)
    else:
        embed.add_field(name=language.find("command[@name='setrole']/item[@type='fail_title']").text,
                        value=language.find("command[@name='setrole']/item[@type='fail']").text, inline=False)
    await ctx.send(embed=embed)


@bot.command(name='setname')
async def setname(ctx, name_to_set):
    pref_handler = PrefHandler(ctx.guild.id)
    language = pref_handler.get_lang()
    embed = discord.Embed(title=language.find("command[@name='setname']/item[@type='title']").text, color=0x85fd2c)

    if ctx.author.name in pref_handler.get_names().keys():
        pref_handler.root.find("users/user[@username='" + ctx.author.name + "']").text = name_to_set
    else:
        username = ET.SubElement(pref_handler.root.find('users'), "user")
        username.set('username', ctx.author.name)
        username.text = name_to_set

    pref_handler.tree.write(pref_handler.file_name, encoding='utf-8')

    embed.add_field(name=language.find("command[@name='setname']/item[@type='success_title']").text,
                    value=language.find("command[@name='setname']/item[@type='success']").text, inline=False)
    await ctx.send(embed=embed)


@bot.command(name='setrole')
async def setrole(ctx, role_to_set):
    pref_handler = PrefHandler(ctx.guild.id)
    language = pref_handler.get_lang()
    embed = discord.Embed(title=language.find("command[@name='setrole']/item[@type='title']").text, color=0x85fd2c)

    if ctx.author.guild_permissions.administrator:
        if role_to_set.lower() in (role.name.lower() for role in ctx.guild.roles):
            embed.add_field(name=language.find("command[@name='setrole']/item[@type='success_title']").text,
                            value=language.find("command[@name='setrole']/item[@type='success']").text, inline=False)
            new_role = pref_handler.root.find('role')
            if new_role is None:
                new_role = ET.SubElement(pref_handler.root, 'role')
            new_role.text = role_to_set
            pref_handler.tree.write(pref_handler.file_name, encoding='utf-8')
        else:
            embed.add_field(name=language.find("command[@name='setrole']/item[@type='fail_title']").text,
                            value=language.find("command[@name='setrole']/item[@type='fail_2']").text, inline=False)
    else:
        embed.add_field(name=language.find("command[@name='setrole']/item[@type='fail_title']").text,
                        value=language.find("command[@name='setrole']/item[@type='fail']").text, inline=False)
    await ctx.send(embed=embed)


@bot.command(name='getnames')
async def getnames(ctx):
    pref_handler = PrefHandler(ctx.guild.id)
    language = pref_handler.get_lang()
    names = pref_handler.get_names()
    embed = discord.Embed(title=language.find("command[@name='getnames']/item[@type='title']").text, color=0x85fd2c)
    embed.add_field(name=language.find("command[@name='getnames']/item[@type='users']").text,
                    value="---", inline=False)
    for username, real_name in names.items():
        embed.add_field(name="@"+username, value=real_name, inline=False)
    await ctx.send(embed=embed)


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
    embed.add_field(name=prefix + language.find("command[@name='help']/item[@type='field5_name']").text,
                    value=language.find("command[@name='setlang']/item[@type='help']").text, inline=False)
    embed.add_field(name=prefix + language.find("command[@name='help']/item[@type='field6_name']").text,
                    value=language.find("command[@name='settz']/item[@type='help']").text, inline=False)
    embed.add_field(name=prefix + language.find("command[@name='help']/item[@type='field7_name']").text,
                    value=language.find("command[@name='setname']/item[@type='help']").text, inline=False)
    embed.add_field(name=prefix + language.find("command[@name='help']/item[@type='field8_name']").text,
                    value=language.find("command[@name='getnames']/item[@type='help']").text, inline=False)
    embed.add_field(name=prefix + language.find("command[@name='help']/item[@type='field4_name']").text,
                    value=language.find("command[@name='help']/item[@type='help']").text, inline=False)
    await ctx.send(embed=embed)


bot.run(TOKEN)
