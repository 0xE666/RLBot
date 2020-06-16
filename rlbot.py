import discord
import requests
import re
import json
import time
import urllib.request
from discord.ext.commands import Bot
import asyncio
from discord.ext import commands
import random
from bs4 import BeautifulSoup
from discord.utils import get
import os


bot = commands.Bot(command_prefix='$', case_insensitive=True)
bot.remove_command('help')

@bot.event
async def on_ready():
    activity = discord.Game(name="With Psyonix")
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=activity)
    print('-' * 30)
    print('Logged in as: ')
    print(bot.user)
    print('-' * 30)


@bot.command()
async def add(ctx, a: float, b: float):
    await ctx.send(a+b)

@bot.command()
async def minus(ctx, a: float, b: float):
    await ctx.send(a-b)

@bot.command()
@commands.has_role('eric')
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)

@bot.command()
@commands.has_role('eric')
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')
    await asyncio.sleep(15)
    await ctx.channel.purge(limit=1)

@bot.command()
@commands.has_role('eric')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            await asyncio.sleep(15)
            await ctx.channel.purge(limit=1)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(694810432359235604)
    await channel.send(f'{member.mention} has joined.')


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(694810432359235604)
    await channel.send(f'{member.mention} has left the server.')

@bot.command()
@commands.has_role('eric')
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)

@bot.command(aliases=['8ball', '8b', 'eb'])
async def _8ball(ctx, *, question):

    message = 'Let me consider your question for a moment human...'

    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Fuck You.",
                 "Fuck Off",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]


    await ctx.send(message)
    await asyncio.sleep(1.7)
    await ctx.channel.purge(limit=1)
    await asyncio.sleep(2)
    await ctx.send(f'{random.choice(responses)}')

@bot.command()
async def help(ctx):

        embed = discord.Embed(title="RLBot help", colour=discord.Colour(0x1406EF))
        embed.set_footer(text="e:)")
        embed.add_field(name="**$Rank** (Check all ranks)", value="Rank Steam {ID}\nRank PS4 {PSN}\nRank XBOX {gamertag}\n\n", inline=False)
        embed.add_field(name="**$Feed** (Latest Stats)", value="Feed Steam {ID}\nFeed PS4 {PSN}\nFeed XBOX {gamertag}\n\n", inline=False)
        embed.add_field(name="**$Duel** (Check 1v1 rank)", value="Duel Steam {ID}\nDuel PS4 {PSN}\nDuel XBOX {gamertag}\n\n", inline=False)
        embed.add_field(name="**$Doubles** (Check 2v2 rank)", value="Doubles Steam {ID}\nDoubles PS4 {PSN}\nDoubles XBOX {gamertag}\n\n", inline=False)
        embed.add_field(name="**$Standard** (Check 3v3 rank)", value="Standard Steam {ID}\nStandard PS4 {PSN}\nStandard XBOX {gamertag}\n\n", inline=False)
        await ctx.send(embed=embed)

def playerid(platform, player):
    url = f'https://rocketleague.tracker.network/profile/{platform}/{player}'
    overview_page = requests.get(url)
    soup = BeautifulSoup(overview_page.text, 'lxml')
    player_id = re.search(r'\d+', soup.find('i', class_='ion-record').parent['href'])[0]
    return player_id

@bot.command()
async def rank(ctx, platform, player):

    player_id = playerid(platform, player)
    live_url = 'https://rocketleague.tracker.network/live/data'
    data = json.dumps({'playerIds': [player_id]})
    live_data = requests.post(live_url, data=data).json()

    try:
        '''Unranked'''
        unrankedMMR = live_data['players'][0]['Stats'][0]['Value']['ValueInt']

        '''Standard Ranked Modes'''
        duelMMR = live_data['players'][0]['Stats'][10]['Value']['ValueInt']
        duelRank = live_data['players'][0]['Stats'][10]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][10]['Other']['subtitle2']
        duelStreak = live_data['players'][0]['Stats'][10]['Other']['winstreak']

        doublesMMR = live_data['players'][0]['Stats'][11]['Value']['ValueInt']
        doublesRank = live_data['players'][0]['Stats'][11]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][11]['Other']['subtitle2']
        doublesStreak = live_data['players'][0]['Stats'][11]['Other']['winstreak']

        solostandardMMR = live_data['players'][0]['Stats'][12]['Value']['ValueInt']
        solostandardRank = live_data['players'][0]['Stats'][12]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][12]['Other']['subtitle2']
        solostandardStreak = live_data['players'][0]['Stats'][12]['Other']['winstreak']

        standardMMR = live_data['players'][0]['Stats'][13]['Value']['ValueInt']
        standardRank =  live_data['players'][0]['Stats'][13]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][13]['Other']['subtitle2']
        standardStreak = live_data['players'][0]['Stats'][13]['Other']['winstreak']

        '''Extra Modes'''
        hoopsMMR = live_data['players'][0]['Stats'][14]['Value']['ValueInt']
        hoopsRank = live_data['players'][0]['Stats'][14]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][14]['Other']['subtitle2']

        rumbleMMR = live_data['players'][0]['Stats'][15]['Value']['ValueInt']
        rumbleRank = live_data['players'][0]['Stats'][15]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][15]['Other']['subtitle2']

        dropshotMMR = live_data['players'][0]['Stats'][16]['Value']['ValueInt']
        dropshotRank = live_data['players'][0]['Stats'][16]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][15]['Other']['subtitle2']

        snowdayMMR = live_data['players'][0]['Stats'][17]['Value']['ValueInt']
        snowdayRank = live_data['players'][0]['Stats'][17]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][15]['Other']['subtitle2']

        embed=discord.Embed(title=f"{player} Ranks", color=0x021ff7)
        embed.set_author(name="RLBot")
        embed.add_field(name="**Duel**", value=f"{duelRank} \nMMR: {duelMMR} \nStreak: {duelStreak}", inline=False)
        embed.add_field(name="**Doubles**", value=f"{doublesRank} \nMMR: {doublesMMR} \nStreak: {doublesStreak}", inline=False)
        embed.add_field(name="**Standard**", value=f"{standardRank} \nMMR: {standardMMR} \nStreak: {standardStreak}", inline=False)
        embed.add_field(name="**Solo Standard**", value=f"{solostandardRank} \nMMR: {solostandardMMR} \nStreak: {solostandardStreak}", inline=False)
        embed.add_field(name="**Hoops**", value=f"{hoopsRank} \nMMR: {hoopsMMR}", inline=False)
        embed.add_field(name="**Rumble**", value=f"{rumbleRank} \nMMR: {rumbleMMR}", inline=False)
        embed.add_field(name="**Dropshot**", value=f"{dropshotRank} \nMMR: {dropshotMMR}", inline=False)
        embed.add_field(name="**Snowday**", value=f"{snowdayRank} \nMMR: {snowdayMMR}", inline=False)
        embed.set_footer(text="e:)")

        await ctx.send(embed=embed)

    except:

        try:

            '''Unranked'''
            unrankedMMR = live_data['players'][0]['Stats'][0]['Value']['ValueInt']

            '''Standard Ranked Modes'''
            duelMMR = live_data['players'][0]['Stats'][10]['Value']['ValueInt']
            duelRank = live_data['players'][0]['Stats'][10]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][10]['Other']['subtitle2']
            duelStreak = live_data['players'][0]['Stats'][10]['Other']['winstreak']

            doublesMMR = live_data['players'][0]['Stats'][11]['Value']['ValueInt']
            doublesRank = live_data['players'][0]['Stats'][11]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][11]['Other']['subtitle2']
            doublesStreak = live_data['players'][0]['Stats'][11]['Other']['winstreak']

            solostandardMMR = live_data['players'][0]['Stats'][12]['Value']['ValueInt']
            solostandardRank = live_data['players'][0]['Stats'][12]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][12]['Other']['subtitle2']
            solostandardStreak = live_data['players'][0]['Stats'][12]['Other']['winstreak']

            standardMMR = live_data['players'][0]['Stats'][13]['Value']['ValueInt']
            standardRank =  live_data['players'][0]['Stats'][13]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][13]['Other']['subtitle2']
            standardStreak = live_data['players'][0]['Stats'][13]['Other']['winstreak']

            embed=discord.Embed(title=f"{player} Ranks", color=0x021ff7)
            embed.set_author(name="RLBot")
            embed.add_field(name="**Duel**", value=f"{duelRank} \nMMR: {duelMMR} \nStreak: {duelStreak}", inline=False)
            embed.add_field(name="**Doubles**", value=f"{doublesRank} \nMMR: {doublesMMR} \nStreak: {doublesStreak}", inline=False)
            embed.add_field(name="**Standard**", value=f"{solostandardRank} \nMMR: {solostandardMMR} \nStreak: {solostandardStreak}", inline=False)
            embed.set_footer(text="e:)")

            await ctx.send(embed=embed)

        except Exception as ex:
            await ctx.send(f"Error Code: {ex}")

@bot.command()
async def duel(ctx, platform, player):

    player_id = playerid(platform, player)
    live_url = 'https://rocketleague.tracker.network/live/data'
    data = json.dumps({'playerIds': [player_id]})
    live_data = requests.post(live_url, data=data).json()

    try:
        '''Unranked'''
        unrankedMMR = live_data['players'][0]['Stats'][0]['Value']['ValueInt']

        '''Standard Ranked Modes'''
        duelMMR = live_data['players'][0]['Stats'][10]['Value']['ValueInt']
        duelRank = live_data['players'][0]['Stats'][10]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][10]['Other']['subtitle2']
        duelStreak = live_data['players'][0]['Stats'][10]['Other']['winstreak']

        doublesMMR = live_data['players'][0]['Stats'][11]['Value']['ValueInt']
        doublesRank = live_data['players'][0]['Stats'][11]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][11]['Other']['subtitle2']
        doublesStreak = live_data['players'][0]['Stats'][11]['Other']['winstreak']

        solostandardMMR = live_data['players'][0]['Stats'][12]['Value']['ValueInt']
        solostandardRank = live_data['players'][0]['Stats'][12]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][12]['Other']['subtitle2']
        solostandardStreak = live_data['players'][0]['Stats'][12]['Other']['winstreak']

        standardMMR = live_data['players'][0]['Stats'][13]['Value']['ValueInt']
        standardRank =  live_data['players'][0]['Stats'][13]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][13]['Other']['subtitle2']
        standardStreak = live_data['players'][0]['Stats'][13]['Other']['winstreak']

        '''Extra Modes'''
        hoopsMMR = live_data['players'][0]['Stats'][14]['Value']['ValueInt']
        hoopsRank = live_data['players'][0]['Stats'][14]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][14]['Other']['subtitle2']

        rumbleMMR = live_data['players'][0]['Stats'][15]['Value']['ValueInt']
        rumbleRank = live_data['players'][0]['Stats'][15]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][15]['Other']['subtitle2']

        dropshotMMR = live_data['players'][0]['Stats'][16]['Value']['ValueInt']
        dropshotRank = live_data['players'][0]['Stats'][16]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][15]['Other']['subtitle2']

        snowdayMMR = live_data['players'][0]['Stats'][17]['Value']['ValueInt']
        snowdayRank = live_data['players'][0]['Stats'][17]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][15]['Other']['subtitle2']

        embed=discord.Embed(title=f"{player} Duel Rank", color=0x021ff7)
        embed.set_author(name="RLBot")
        embed.add_field(name="**Duel**", value=f"{duelRank} \nMMR: {duelMMR} \nStreak: {duelStreak}", inline=False)
        embed.set_footer(text="e:)")

        await ctx.send(embed=embed)

    except:

        try:

            '''Unranked'''
            unrankedMMR = live_data['players'][0]['Stats'][0]['Value']['ValueInt']

            '''Standard Ranked Modes'''
            duelMMR = live_data['players'][0]['Stats'][10]['Value']['ValueInt']
            duelRank = live_data['players'][0]['Stats'][10]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][10]['Other']['subtitle2']
            duelStreak = live_data['players'][0]['Stats'][10]['Other']['winstreak']

            doublesMMR = live_data['players'][0]['Stats'][11]['Value']['ValueInt']
            doublesRank = live_data['players'][0]['Stats'][11]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][11]['Other']['subtitle2']
            doublesStreak = live_data['players'][0]['Stats'][11]['Other']['winstreak']

            solostandardMMR = live_data['players'][0]['Stats'][12]['Value']['ValueInt']
            solostandardRank = live_data['players'][0]['Stats'][12]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][12]['Other']['subtitle2']
            solostandardStreak = live_data['players'][0]['Stats'][12]['Other']['winstreak']

            standardMMR = live_data['players'][0]['Stats'][13]['Value']['ValueInt']
            standardRank =  live_data['players'][0]['Stats'][13]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][13]['Other']['subtitle2']
            standardStreak = live_data['players'][0]['Stats'][13]['Other']['winstreak']

            embed=discord.Embed(title=f"{player} Duel Rank", color=0x021ff7)
            embed.set_author(name="RLBot")
            embed.add_field(name="**Duel**", value=f"{duelRank} \nMMR: {duelMMR} \nStreak: {duelStreak}", inline=False)
            embed.set_footer(text="e:)")

            await ctx.send(embed=embed)

        except Exception as ex:
            await ctx.send(f"Error Code: {ex}")

@bot.command()
async def doubles(ctx, platform, player):

    player_id = playerid(platform, player)
    live_url = 'https://rocketleague.tracker.network/live/data'
    data = json.dumps({'playerIds': [player_id]})
    live_data = requests.post(live_url, data=data).json()

    try:
        '''Unranked'''
        unrankedMMR = live_data['players'][0]['Stats'][0]['Value']['ValueInt']

        '''Standard Ranked Modes'''
        duelMMR = live_data['players'][0]['Stats'][10]['Value']['ValueInt']
        duelRank = live_data['players'][0]['Stats'][10]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][10]['Other']['subtitle2']
        duelStreak = live_data['players'][0]['Stats'][10]['Other']['winstreak']

        doublesMMR = live_data['players'][0]['Stats'][11]['Value']['ValueInt']
        doublesRank = live_data['players'][0]['Stats'][11]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][11]['Other']['subtitle2']
        doublesStreak = live_data['players'][0]['Stats'][11]['Other']['winstreak']

        solostandardMMR = live_data['players'][0]['Stats'][12]['Value']['ValueInt']
        solostandardRank = live_data['players'][0]['Stats'][12]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][12]['Other']['subtitle2']
        solostandardStreak = live_data['players'][0]['Stats'][12]['Other']['winstreak']

        standardMMR = live_data['players'][0]['Stats'][13]['Value']['ValueInt']
        standardRank =  live_data['players'][0]['Stats'][13]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][13]['Other']['subtitle2']
        standardStreak = live_data['players'][0]['Stats'][13]['Other']['winstreak']

        '''Extra Modes'''
        hoopsMMR = live_data['players'][0]['Stats'][14]['Value']['ValueInt']
        hoopsRank = live_data['players'][0]['Stats'][14]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][14]['Other']['subtitle2']

        rumbleMMR = live_data['players'][0]['Stats'][15]['Value']['ValueInt']
        rumbleRank = live_data['players'][0]['Stats'][15]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][15]['Other']['subtitle2']

        dropshotMMR = live_data['players'][0]['Stats'][16]['Value']['ValueInt']
        dropshotRank = live_data['players'][0]['Stats'][16]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][15]['Other']['subtitle2']

        snowdayMMR = live_data['players'][0]['Stats'][17]['Value']['ValueInt']
        snowdayRank = live_data['players'][0]['Stats'][17]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][15]['Other']['subtitle2']

        embed=discord.Embed(title=f"{player} Doubles Rank", color=0x021ff7)
        embed.set_author(name="RLBot")
        embed.add_field(name="**Doubles**", value=f"{doublesRank} \nMMR: {doublesMMR} \nStreak: {doublesStreak}", inline=False)
        embed.set_footer(text="e:)")

        await ctx.send(embed=embed)

    except:

        try:

            '''Unranked'''
            unrankedMMR = live_data['players'][0]['Stats'][0]['Value']['ValueInt']

            '''Standard Ranked Modes'''
            duelMMR = live_data['players'][0]['Stats'][10]['Value']['ValueInt']
            duelRank = live_data['players'][0]['Stats'][10]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][10]['Other']['subtitle2']
            duelStreak = live_data['players'][0]['Stats'][10]['Other']['winstreak']

            doublesMMR = live_data['players'][0]['Stats'][11]['Value']['ValueInt']
            doublesRank = live_data['players'][0]['Stats'][11]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][11]['Other']['subtitle2']
            doublesStreak = live_data['players'][0]['Stats'][11]['Other']['winstreak']

            solostandardMMR = live_data['players'][0]['Stats'][12]['Value']['ValueInt']
            solostandardRank = live_data['players'][0]['Stats'][12]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][12]['Other']['subtitle2']
            solostandardStreak = live_data['players'][0]['Stats'][12]['Other']['winstreak']

            standardMMR = live_data['players'][0]['Stats'][13]['Value']['ValueInt']
            standardRank =  live_data['players'][0]['Stats'][13]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][13]['Other']['subtitle2']
            standardStreak = live_data['players'][0]['Stats'][13]['Other']['winstreak']

            embed=discord.Embed(title=f"{player} Doubles Rank", color=0x021ff7)
            embed.set_author(name="RLBot")
            embed.add_field(name="**Doubles**", value=f"{doublesRank} \nMMR: {doublesMMR} \nStreak: {doublesStreak}", inline=False)
            embed.set_footer(text="e:)")

            await ctx.send(embed=embed)

        except Exception as ex:
            await ctx.send(f"Error Code: {ex}")

@bot.command()
async def standard(ctx, platform, player):

    player_id = playerid(platform, player)
    live_url = 'https://rocketleague.tracker.network/live/data'
    data = json.dumps({'playerIds': [player_id]})
    live_data = requests.post(live_url, data=data).json()

    try:
        '''Unranked'''
        unrankedMMR = live_data['players'][0]['Stats'][0]['Value']['ValueInt']

        '''Standard Ranked Modes'''
        duelMMR = live_data['players'][0]['Stats'][10]['Value']['ValueInt']
        duelRank = live_data['players'][0]['Stats'][10]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][10]['Other']['subtitle2']
        duelStreak = live_data['players'][0]['Stats'][10]['Other']['winstreak']

        doublesMMR = live_data['players'][0]['Stats'][11]['Value']['ValueInt']
        doublesRank = live_data['players'][0]['Stats'][11]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][11]['Other']['subtitle2']
        doublesStreak = live_data['players'][0]['Stats'][11]['Other']['winstreak']

        solostandardMMR = live_data['players'][0]['Stats'][12]['Value']['ValueInt']
        solostandardRank = live_data['players'][0]['Stats'][12]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][12]['Other']['subtitle2']
        solostandardStreak = live_data['players'][0]['Stats'][12]['Other']['winstreak']

        standardMMR = live_data['players'][0]['Stats'][13]['Value']['ValueInt']
        standardRank =  live_data['players'][0]['Stats'][13]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][13]['Other']['subtitle2']
        standardStreak = live_data['players'][0]['Stats'][13]['Other']['winstreak']

        '''Extra Modes'''
        hoopsMMR = live_data['players'][0]['Stats'][14]['Value']['ValueInt']
        hoopsRank = live_data['players'][0]['Stats'][14]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][14]['Other']['subtitle2']

        rumbleMMR = live_data['players'][0]['Stats'][15]['Value']['ValueInt']
        rumbleRank = live_data['players'][0]['Stats'][15]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][15]['Other']['subtitle2']

        dropshotMMR = live_data['players'][0]['Stats'][16]['Value']['ValueInt']
        dropshotRank = live_data['players'][0]['Stats'][16]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][15]['Other']['subtitle2']

        snowdayMMR = live_data['players'][0]['Stats'][17]['Value']['ValueInt']
        snowdayRank = live_data['players'][0]['Stats'][17]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][15]['Other']['subtitle2']

        embed=discord.Embed(title=f"{player} Standard Rank", color=0x021ff7)
        embed.set_author(name="RLBot")
        embed.add_field(name="**Standard**", value=f"{standardRank} \nMMR: {standardMMR} \nStreak: {standardStreak}", inline=False)
        embed.set_footer(text="e:)")

        await ctx.send(embed=embed)

    except:

        try:

            '''Unranked'''
            unrankedMMR = live_data['players'][0]['Stats'][0]['Value']['ValueInt']

            '''Standard Ranked Modes'''
            duelMMR = live_data['players'][0]['Stats'][10]['Value']['ValueInt']
            duelRank = live_data['players'][0]['Stats'][10]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][10]['Other']['subtitle2']
            duelStreak = live_data['players'][0]['Stats'][10]['Other']['winstreak']

            doublesMMR = live_data['players'][0]['Stats'][11]['Value']['ValueInt']
            doublesRank = live_data['players'][0]['Stats'][11]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][11]['Other']['subtitle2']
            doublesStreak = live_data['players'][0]['Stats'][11]['Other']['winstreak']

            solostandardMMR = live_data['players'][0]['Stats'][12]['Value']['ValueInt']
            solostandardRank = live_data['players'][0]['Stats'][12]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][12]['Other']['subtitle2']
            solostandardStreak = live_data['players'][0]['Stats'][12]['Other']['winstreak']

            standardMMR = live_data['players'][0]['Stats'][13]['Value']['ValueInt']
            standardRank =  live_data['players'][0]['Stats'][13]['Other']['subtitle'] + ' ' + live_data['players'][0]['Stats'][13]['Other']['subtitle2']
            standardStreak = live_data['players'][0]['Stats'][13]['Other']['winstreak']

            embed=discord.Embed(title=f"{player} Standard Rank", color=0x021ff7)
            embed.set_author(name="RLBot")
            embed.add_field(name="**Standard**", value=f"{standardRank} \nMMR: {standardMMR} \nStreak: {standardStreak}", inline=False)
            embed.set_footer(text="e:)")

            await ctx.send(embed=embed)

        except Exception as ex:
            await ctx.send(f"Error Code: {ex}")


@bot.command()
async def feed(ctx, platform, player):

    player_id = playerid(platform, player)
    live_url = 'https://rocketleague.tracker.network/live/data'
    data = json.dumps({'playerIds': [player_id]})
    live_data = requests.post(live_url, data=data).json()

    try:

        mode0 = live_data['feed'][0]['Changes'][-1]['Field']
        mmr0 = live_data['feed'][0]['Changes'][-1]['Value']
        change0 = live_data['feed'][0]['Changes'][-1]['Delta']
        message0 = live_data['feed'][0]['Changes'][-1]['Message']


        mode1 = live_data['feed'][1]['Changes'][-1]['Field']
        mmr1 = live_data['feed'][1]['Changes'][-1]['Value']
        change1 = live_data['feed'][1]['Changes'][-1]['Delta']
        message1 = live_data['feed'][1]['Changes'][-1]['Message']

        mode2 = live_data['feed'][2]['Changes'][-1]['Field']
        mmr2 = live_data['feed'][2]['Changes'][-1]['Value']
        change2 = live_data['feed'][2]['Changes'][-1]['Delta']
        message2 = live_data['feed'][2]['Changes'][-1]['Message']

        mode3 = live_data['feed'][3]['Changes'][-1]['Field']
        mmr3 = live_data['feed'][3]['Changes'][-1]['Value']
        change3 = live_data['feed'][3]['Changes'][-1]['Delta']
        message3 = live_data['feed'][3]['Changes'][-1]['Message']

        mode4 = live_data['feed'][4]['Changes'][-1]['Field']
        mmr4 = live_data['feed'][4]['Changes'][-1]['Value']
        change4 = live_data['feed'][4]['Changes'][-1]['Delta']
        message4 = live_data['feed'][4]['Changes'][-1]['Message']

        mode5 = live_data['feed'][5]['Changes'][-1]['Field']
        mmr5 = live_data['feed'][5]['Changes'][-1]['Value']
        change5 = live_data['feed'][5]['Changes'][-1]['Delta']
        message5 = live_data['feed'][5]['Changes'][-1]['Message']

        mode6 = live_data['feed'][6]['Changes'][-1]['Field']
        mmr6 = live_data['feed'][6]['Changes'][-1]['Value']
        change6 = live_data['feed'][6]['Changes'][-1]['Delta']
        message6 = live_data['feed'][6]['Changes'][-1]['Message']

        mode7 = live_data['feed'][7]['Changes'][-1]['Field']
        mmr7 = live_data['feed'][7]['Changes'][-1]['Value']
        change7 = live_data['feed'][7]['Changes'][-1]['Delta']
        message7 = live_data['feed'][7]['Changes'][-1]['Message']


        embed=discord.Embed(title=f"{player} Latest Stats", color=0x021ff7)
        embed.set_author(name="RLBot")
        embed.add_field(name="**Feed**",
                            value=f"{mode0} \nMMR: {mmr0} \nMMR Change: {change0} \nMessage: {message0}\n\n" \
                                + f"{mode1} \nMMR: {mmr1} \nMMR Change: {change1} \nMessage: {message1}\n\n" \
                                + f"{mode2} \nMMR: {mmr2} \nMMR Change: {change2} \nMessage: {message2}\n\n" \
                                + f"{mode3} \nMMR: {mmr3} \nMMR Change: {change3} \nMessage: {message3}\n\n" \
                                + f"{mode4} \nMMR: {mmr4} \nMMR Change: {change4} \nMessage: {message4}\n\n" \
                                + f"{mode5} \nMMR: {mmr5} \nMMR Change: {change5} \nMessage: {message5}\n\n" \
                                + f"{mode6} \nMMR: {mmr6} \nMMR Change: {change6} \nMessage: {message6}\n\n" \
                                + f"{mode7} \nMMR: {mmr7} \nMMR Change: {change7} \nMessage: {message7}\n\n" ,
                            inline=False)
        embed.set_footer(text="e:)")

        await ctx.send(embed=embed)

    except:

        try:

            mode0 = live_data['feed'][0]['Changes'][-1]['Field']
            mmr0 = live_data['feed'][0]['Changes'][-1]['Value']
            change0 = live_data['feed'][0]['Changes'][-1]['Delta']
            message0 = live_data['feed'][0]['Changes'][-1]['Message']

            mode1 = live_data['feed'][1]['Changes'][-1]['Field']
            mmr1 = live_data['feed'][1]['Changes'][-1]['Value']
            change1 = live_data['feed'][1]['Changes'][-1]['Delta']
            message1 = live_data['feed'][1]['Changes'][-1]['Message']

            mode2 = live_data['feed'][2]['Changes'][-1]['Field']
            mmr2 = live_data['feed'][2]['Changes'][-1]['Value']
            change2 = live_data['feed'][2]['Changes'][-1]['Delta']
            message2 = live_data['feed'][2]['Changes'][-1]['Message']

            mode3 = live_data['feed'][3]['Changes'][-1]['Field']
            mmr3 = live_data['feed'][3]['Changes'][-1]['Value']
            change3 = live_data['feed'][3]['Changes'][-1]['Delta']
            message3 = live_data['feed'][3]['Changes'][-1]['Message']

            mode4 = live_data['feed'][4]['Changes'][-1]['Field']
            mmr4 = live_data['feed'][4]['Changes'][-1]['Value']
            change4 = live_data['feed'][4]['Changes'][-1]['Delta']
            message4 = live_data['feed'][4]['Changes'][-1]['Message']



            embed=discord.Embed(title=f"{player} Latest Stats", color=0x021ff7)
            embed.set_author(name="RLBot")
            embed.add_field(name="**Feed**",
                                value=f"{mode0} \nMMR: {mmr0} \nMMR Change: {change0} \nMessage: {message0}\n\n" \
                                    + f"{mode1} \nMMR: {mmr1} \nMMR Change: {change1} \nMessage: {message1}\n\n" \
                                    + f"{mode2} \nMMR: {mmr2} \nMMR Change: {change2} \nMessage: {message2}\n\n" \
                                    + f"{mode3} \nMMR: {mmr3} \nMMR Change: {change3} \nMessage: {message3}\n\n" \
                                    + f"{mode4} \nMMR: {mmr4} \nMMR Change: {change4} \nMessage: {message4}\n\n" ,
                                inline=False)
            embed.set_footer(text="e:)")

            await ctx.send(embed=embed)

        except Exception as ex:
            await ctx.send(f"Error Code: {ex}")

bot.run(TOKEN)
