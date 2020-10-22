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
async def help(ctx):

        embed = discord.Embed(title="RLBot help", colour=discord.Colour(0x1406EF))
        embed.set_footer(text="e:)")
        embed.add_field(name="**$Rank** (Check all ranks)", value="Rank Steam {ID}\nRank PSN {PSN}\nRank XBOX {gamertag}\n\n", inline=False)
        embed.add_field(name="**$Feed** (check recent matches)", value="Feed Steam {ID}\nFeed PSN {PSN}\nFeed XBOX {gamertag}\n\n", inline=False)
        embed.add_field(name="**$Duel** (Check 1v1 rank)", value="Duel Steam {ID}\nDuel PSN {PSN}\nDuel XBOX {gamertag}\n\n", inline=False)
        embed.add_field(name="**$Doubles** (Check 2v2 rank)", value="Doubles Steam {ID}\nDoubles PSN {PSN}\nDoubles XBOX {gamertag}\n\n", inline=False)
        embed.add_field(name="**$Standard** (Check 3v3 rank)", value="Standard Steam {ID}\nStandard PSN {PSN}\nStandard XBOX {gamertag}\n\n", inline=False)
        embed.add_field(name="**$Tourney** (Check Tournament rank)", value="Tourney Steam {ID}\nTourney PSN {PSN}\nTourney XBOX {gamertag}\n\n", inline=False)
        await ctx.send(embed=embed)

def getData(platform, player):
    url = f"https://api.tracker.gg/api/v2/rocket-league/standard/profile/{platform}/{player}"
    header = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en",
        "referrer": "https://rocketleague.tracker.network/rocket-league/live",
        "referrerPolicy": "no-referrer-when-downgrade"
    }
    data = requests.get(url, headers=header)
    return data.json()

def getsessData(platform, player):
    url = f"https://api.tracker.gg/api/v2/rocket-league/standard/profile/{platform}/{player}/sessions?"
    header = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en",
        "referrer": "https://rocketleague.tracker.network/rocket-league/live",
        "referrerPolicy": "no-referrer-when-downgrade"
    }
    data = requests.get(url, headers=header)
    return data.json()

@bot.command()
async def rank(ctx, platform, player):

    livedata = getData(platform, player)

    try:
        avatar = livedata['data']['platformInfo']['avatarUrl']
        seasonReward = livedata['data']['segments'][0]['stats']['seasonRewardLevel']['metadata']['rankName']

        duelrank = livedata['data']['segments'][2]['stats']['tier']['metadata']['name']
        dueldiv = livedata['data']['segments'][2]['stats']['division']['metadata']['name']
        duelstreak = livedata['data']['segments'][2]['stats']['winStreak']['displayValue']
        duelMMR = livedata['data']['segments'][2]['stats']['rating']['value']

        doublesrank = livedata['data']['segments'][3]['stats']['tier']['metadata']['name']
        doublesdiv = livedata['data']['segments'][3]['stats']['division']['metadata']['name']
        doublesstreak = livedata['data']['segments'][3]['stats']['winStreak']['displayValue']
        doublesMMR = livedata['data']['segments'][3]['stats']['rating']['value']

        standardrank = livedata['data']['segments'][4]['stats']['tier']['metadata']['name']
        standarddiv = livedata['data']['segments'][4]['stats']['division']['metadata']['name']
        standardstreak = livedata['data']['segments'][4]['stats']['winStreak']['displayValue']
        standardMMR = livedata['data']['segments'][4]['stats']['rating']['value']

        hoopsrank = livedata['data']['segments'][5]['stats']['tier']['metadata']['name']
        hoopsdiv = livedata['data']['segments'][5]['stats']['division']['metadata']['name']
        hoopsstreak = livedata['data']['segments'][5]['stats']['winStreak']['displayValue']
        hoopsMMR = livedata['data']['segments'][5]['stats']['rating']['value']

        rumblerank = livedata['data']['segments'][6]['stats']['tier']['metadata']['name']
        rumblediv = livedata['data']['segments'][6]['stats']['division']['metadata']['name']
        rumblestreak = livedata['data']['segments'][6]['stats']['winStreak']['displayValue']
        rumbleMMR = livedata['data']['segments'][6]['stats']['rating']['value']

        dropshotrank = livedata['data']['segments'][7]['stats']['tier']['metadata']['name']
        dropshotdiv = livedata['data']['segments'][7]['stats']['division']['metadata']['name']
        dropshotstreak = livedata['data']['segments'][7]['stats']['winStreak']['displayValue']
        dropshotMMR = livedata['data']['segments'][7]['stats']['rating']['value']

        snowdayrank = livedata['data']['segments'][8]['stats']['tier']['metadata']['name']
        snowdaydiv = livedata['data']['segments'][8]['stats']['division']['metadata']['name']
        snowdaystreak = livedata['data']['segments'][8]['stats']['winStreak']['displayValue']
        snowdayMMR = livedata['data']['segments'][8]['stats']['rating']['value']

        tourneyrank = livedata['data']['segments'][9]['stats']['tier']['metadata']['name']
        tourneydiv = livedata['data']['segments'][9]['stats']['division']['metadata']['name']
        tourneystreak = livedata['data']['segments'][9]['stats']['winStreak']['displayValue']
        tourneyMMR = livedata['data']['segments'][9]['stats']['rating']['value']


        embed=discord.Embed(title=f"{player} Ranks", color=0x021ff7)
        embed.set_author(name="RLBot")
        embed.set_thumbnail(url=avatar)
        embed.add_field(name="**Season Reward**", value=f"{seasonReward}", inline=False)
        embed.add_field(name="**Duel**", value=f"{duelrank + ' ' + dueldiv} \nMMR: {duelMMR} \nStreak: {duelstreak}", inline=False)
        embed.add_field(name="**Doubles**", value=f"{doublesrank + ' ' + doublesdiv} \nMMR: {doublesMMR} \nStreak: {doublesstreak}", inline=False)
        embed.add_field(name="**Standard**", value=f"{standardrank + ' ' + standarddiv} \nMMR: {standardMMR} \nStreak: {standardstreak}", inline=False)
        embed.add_field(name="**Tournaments**", value=f"{tourneyrank + ' ' + tourneydiv} \nMMR: {tourneyMMR} \nStreak: {tourneyMMR}", inline=False)
        embed.add_field(name="**Hoops**", value=f"{hoopsrank + ' ' + hoopsdiv} \nMMR: {hoopsMMR}", inline=False)
        embed.add_field(name="**Rumble**", value=f"{rumblerank + ' ' + rumblediv} \nMMR: {rumbleMMR}", inline=False)
        embed.add_field(name="**Dropshot**", value=f"{dropshotrank + ' ' + dropshotdiv} \nMMR: {dropshotMMR}", inline=False)
        embed.add_field(name="**Snowday**", value=f"{snowdayrank + ' ' + snowdaydiv} \nMMR: {snowdayMMR}", inline=False)
        embed.set_footer(text="e:)")

        await ctx.send(embed=embed)

    except:

        try:

            avatar = livedata['data']['platformInfo']['avatarUrl']
            seasonReward = livedata['data']['segments'][0]['stats']['seasonRewardLevel']['metadata']['rankName']

            duelrank = livedata['data']['segments'][2]['stats']['tier']['metadata']['name']
            dueldiv = livedata['data']['segments'][2]['stats']['division']['metadata']['name']
            duelstreak = livedata['data']['segments'][2]['stats']['winStreak']['displayValue']
            duelMMR = livedata['data']['segments'][2]['stats']['rating']['value']

            doublesrank = livedata['data']['segments'][3]['stats']['tier']['metadata']['name']
            doublesdiv = livedata['data']['segments'][3]['stats']['division']['metadata']['name']
            doublesstreak = livedata['data']['segments'][3]['stats']['winStreak']['displayValue']
            doublesMMR = livedata['data']['segments'][3]['stats']['rating']['value']

            standardrank = livedata['data']['segments'][4]['stats']['tier']['metadata']['name']
            standarddiv = livedata['data']['segments'][4]['stats']['division']['metadata']['name']
            standardstreak = livedata['data']['segments'][4]['stats']['winStreak']['displayValue']
            standardMMR = livedata['data']['segments'][4]['stats']['rating']['value']

            tourneyrank = livedata['data']['segments'][9]['stats']['tier']['metadata']['name']
            tourneydiv = livedata['data']['segments'][9]['stats']['division']['metadata']['name']
            tourneystreak = livedata['data']['segments'][9]['stats']['winStreak']['displayValue']
            tourneyMMR = livedata['data']['segments'][9]['stats']['rating']['value']

            embed=discord.Embed(title=f"{player} Ranks", color=0x021ff7)
            embed.set_author(name="RLBot")
            embed.set_thumbnail(url=avatar)
            embed.add_field(name="**Season Reward**", value=f"{seasonReward}", inline=False)
            embed.add_field(name="**Duel**", value=f"{duelrank + ' ' + dueldiv} \nMMR: {duelMMR} \nStreak: {duelstreak}", inline=False)
            embed.add_field(name="**Doubles**", value=f"{doublesrank + ' ' + doublesdiv} \nMMR: {doublesMMR} \nStreak: {doublesstreak}", inline=False)
            embed.add_field(name="**Standard**", value=f"{standardrank + ' ' + standarddiv} \nMMR: {standardMMR} \nStreak: {standardstreak}", inline=False)
            embed.set_footer(text="e:)")

            await ctx.send(embed=embed)

        except Exception as ex:
            await ctx.send(f"Error Code: {ex}")

@bot.command()
async def duel(ctx, platform, player):

    livedata = getData(platform, player)
    avatar = livedata['data']['platformInfo']['avatarUrl']
    seasonReward = livedata['data']['segments'][0]['stats']['seasonRewardLevel']['metadata']['rankName']

    duelrank = livedata['data']['segments'][2]['stats']['tier']['metadata']['name']
    dueldiv = livedata['data']['segments'][2]['stats']['division']['metadata']['name']
    duelstreak = livedata['data']['segments'][2]['stats']['winStreak']['displayValue']
    duelMMR = livedata['data']['segments'][2]['stats']['rating']['value']

    embed=discord.Embed(title=f"{player} Ranks", color=0x021ff7)
    embed.set_author(name="RLBot")
    embed.set_thumbnail(url=avatar)
    embed.add_field(name="**Duel**", value=f"{duelrank + ' ' + dueldiv} \nMMR: {duelMMR} \nStreak: {duelstreak}", inline=False)
    embed.set_footer(text="e:)")

    await ctx.send(embed=embed)


@bot.command()
async def doubles(ctx, platform, player):

    livedata = getData(platform, player)
    avatar = livedata['data']['platformInfo']['avatarUrl']
    seasonReward = livedata['data']['segments'][0]['stats']['seasonRewardLevel']['metadata']['rankName']

    doublesrank = livedata['data']['segments'][3]['stats']['tier']['metadata']['name']
    doublesdiv = livedata['data']['segments'][3]['stats']['division']['metadata']['name']
    doublesstreak = livedata['data']['segments'][3]['stats']['winStreak']['displayValue']
    doublesMMR = livedata['data']['segments'][3]['stats']['rating']['value']

    embed=discord.Embed(title=f"{player} Ranks", color=0x021ff7)
    embed.set_author(name="RLBot")
    embed.set_thumbnail(url=avatar)
    embed.add_field(name="**Doubles**", value=f"{doublesrank + ' ' + doublesdiv} \nMMR: {doublesMMR} \nStreak: {doublesstreak}", inline=False)
    embed.set_footer(text="e:)")

    await ctx.send(embed=embed)

@bot.command()
async def standard(ctx, platform, player):
    livedata = getData(platform, player)
    avatar = livedata['data']['platformInfo']['avatarUrl']
    seasonReward = livedata['data']['segments'][0]['stats']['seasonRewardLevel']['metadata']['rankName']


    standardrank = livedata['data']['segments'][4]['stats']['tier']['metadata']['name']
    standarddiv = livedata['data']['segments'][4]['stats']['division']['metadata']['name']
    standardstreak = livedata['data']['segments'][4]['stats']['winStreak']['displayValue']
    standardMMR = livedata['data']['segments'][4]['stats']['rating']['value']


    embed=discord.Embed(title=f"{player} Ranks", color=0x021ff7)
    embed.set_author(name="RLBot")
    embed.set_thumbnail(url=avatar)
    embed.add_field(name="**Standard**", value=f"{standardrank + ' ' + standarddiv} \nMMR: {standardMMR} \nStreak: {standardstreak}", inline=False)
    embed.set_footer(text="e:)")

    await ctx.send(embed=embed)

@bot.command()
async def tourney(ctx, platform, player):
    livedata = getData(platform, player)
    avatar = livedata['data']['platformInfo']['avatarUrl']
    seasonReward = livedata['data']['segments'][0]['stats']['seasonRewardLevel']['metadata']['rankName']

    tourneyrank = livedata['data']['segments'][9]['stats']['tier']['metadata']['name']
    tourneydiv = livedata['data']['segments'][9]['stats']['division']['metadata']['name']
    tourneystreak = livedata['data']['segments'][9]['stats']['winStreak']['displayValue']
    tourneyMMR = livedata['data']['segments'][9]['stats']['rating']['value']


    embed=discord.Embed(title=f"{player} Ranks", color=0x021ff7)
    embed.set_author(name="RLBot")
    embed.set_thumbnail(url=avatar)
    embed.add_field(name="**Tournaments**", value=f"{tourneyrank + ' ' + tourneydiv} \nMMR: {tourneyMMR} \nStreak: {tourneystreak}", inline=False)
    embed.set_footer(text="e:)")

    await ctx.send(embed=embed)


bot.run('NzEwNTE2NjcxMTg5NzQ1Njgz.Xr1mNw.tJTerhfqAUt8oebMv2Hzz3S7eiU')
