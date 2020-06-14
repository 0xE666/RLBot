import discord
import requests
import re
import json
import time
import urllib.request
from discord.ext.commands import Bot
import asyncio
from discord.ext import commands

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
        embed.add_field(name="**$Rank** (Check all ranks)", value="**Rank Steam {ID}\n Rank PS4 {PSN}\n Rank XBOX {gamertag}**", inline=False)
        embed.add_field(name="**$Duel** (Check 1v1 rank)", value="**Duel Steam {ID}\n Duel PS4 {PSN}\n Duel XBOX {gamertag}**", inline=False)
        embed.add_field(name="**$Doubles** (Check 2v2 rank)", value="**Doubles Steam {ID}\n Doubles PS4 {PSN}\n Doubles XBOX {gamertag}**", inline=False)
        embed.add_field(name="**$Standard** (Check 3v3 rank)", value="**Standard Steam {ID}\n Standard PS4 {PSN}\n Standard XBOX {gamertag}**", inline=False)
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
        embed.add_field(name="**Duel**", value=f"{duelRank} \n MMR: {duelMMR} \n Streak: {duelStreak}", inline=False)
        embed.add_field(name="**Doubles**", value=f"{doublesRank} \n MMR: {doublesMMR} \n Streak: {doublesStreak}", inline=False)
        embed.add_field(name="**Standard**", value=f"{standardRank} \n MMR: {standardMMR} \n Streak: {standardStreak}", inline=False)
        embed.add_field(name="**Solo Standard**", value=f"{solostandardRank} \n MMR: {solostandardMMR} \n Streak: {solostandardStreak}", inline=False)
        embed.add_field(name="**Hoops**", value=f"{hoopsRank} \n MMR: {hoopsMMR}", inline=False)
        embed.add_field(name="**Rumble**", value=f"{rumbleRank} \n MMR: {rumbleMMR}", inline=False)
        embed.add_field(name="**Dropshot**", value=f"{dropshotRank} \n MMR: {dropshotMMR}", inline=False)
        embed.add_field(name="**Snowday**", value=f"{snowdayRank} \n MMR: {snowdayMMR}", inline=False)
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
            embed.add_field(name="**Duel**", value=f"{duelRank} \n MMR: {duelMMR} \n Streak: {duelStreak}", inline=False)
            embed.add_field(name="**Doubles**", value=f"{doublesRank} \n MMR: {doublesMMR} \n Streak: {doublesStreak}", inline=False)
            embed.add_field(name="**Standard**", value=f"{standardRank} \n MMR: {standardMMR} \n Streak: {standardStreak}", inline=False)
            embed.add_field(name="**Solo Standard**", value=f"{solostandardRank} \n MMR: {solostandardMMR} \n Streak: {solostandardStreak}", inline=False)
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

        embed=discord.Embed(title=f"{player} Ranks", color=0x021ff7)
        embed.set_author(name="RLBot")
        embed.add_field(name="**Duel**", value=f"{duelRank} \n MMR: {duelMMR} \n Streak: {duelStreak}", inline=False)
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
            embed.add_field(name="**Duel**", value=f"{duelRank} \n MMR: {duelMMR} \n Streak: {duelStreak}", inline=False)
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

        embed=discord.Embed(title=f"{player} Ranks", color=0x021ff7)
        embed.set_author(name="RLBot")
        embed.add_field(name="**Doubles**", value=f"{doublesRank} \n MMR: {doublesMMR} \n Streak: {doublesStreak}", inline=False)
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
            embed.add_field(name="**Doubles**", value=f"{doublesRank} \n MMR: {doublesMMR} \n Streak: {doublesStreak}", inline=False)
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

        embed=discord.Embed(title=f"{player} Ranks", color=0x021ff7)
        embed.set_author(name="RLBot")
        embed.add_field(name="**Standard**", value=f"{standardRank} \n MMR: {standardMMR} \n Streak: {standardStreak}", inline=False)
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
            embed.add_field(name="**Standard**", value=f"{standardRank} \n MMR: {standardMMR} \n Streak: {standardStreak}", inline=False)
            embed.set_footer(text="e:)")

            await ctx.send(embed=embed)

        except Exception as ex:
            await ctx.send(f"Error Code: {ex}")

bot.run('NzEwNTE2NjcxMTg5NzQ1Njgz.XsQ7GQ.VnSZ_ZEBeWQ0Q65wQMGMnWOfNEo')
