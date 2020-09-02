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
async def starttwitchbot(ctx):
    global val
    live = []
    val = True
    while val == True:
        try:
            data = followed()
        except (KeyError, ValueError):
            sys.exit(1)
        numStreams = len(data['streams'])
        for i in range(0, numStreams):
            name = data["streams"][i]["channel"]["name"]
            game = data["streams"][i]["channel"]["game"]
            status = data["streams"][i]["channel"]["status"]
            viewers = str(data["streams"][i]["viewers"])
            stream = data["streams"][i]["stream_type"]
            prev = data['streams'][1]['preview']['medium']
            logo = data['streams'][1]['channel']['logo']
            try:
                if name in live:
                    pass
                elif stream == "live":
                    embed=discord.Embed(title=f"{name} is live", color=0x021ff7, url=f"https://twitch.tv/{name}")
                    embed.set_author(name="RLBot", icon_url=logo)
                    embed.set_thumbnail(url=prev)
                    embed.add_field(name=f"**{status}**", value=f"Viewers: {viewers} \nPlaying: {game}", inline=False)
                    embed.set_footer(text="e:)")
                    await ctx.send(embed=embed)
                    live.append(name)
            except:
                await asyncio.sleep(30)
                live.clear()

@bot.command()
async def stoptwitchbot(ctx):
    val = False

@bot.command()
async def add(ctx, a: float, b: float):
    await ctx.send(a+b)

@bot.command()
async def minus(ctx, a: float, b: float):
    await ctx.send(a-b)

@bot.command()
@commands.has_role('admin')
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)

@bot.command()
@commands.has_role('admin')
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')
    await asyncio.sleep(15)
    await ctx.channel.purge(limit=1)

@bot.command()
@commands.has_role('admin')
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
    channel = bot.get_channel(724820415293423686)
    await channel.send(f'{member.mention} has joined.')


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(724820415293423686)
    await channel.send(f'{member.mention} has left the server.')

@bot.command()
@commands.has_role('admin')
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

def getid(streamer):
    headers = {
               'Accept': 'application/vnd.twitchtv.v5+json',
               'Client-ID': 'qi3zqqr8r1rlrip1zlkwghx2iyxm5v',
               'Authorization': 'OAuth c5dbysxbjylvf0kosg0998zdbyq0pv',
               }
    try:
        response = requests.get(f'https://api.twitch.tv/kraken/users?login={streamer}', headers=headers)
        data = response.json()
    except (KeyError, ValueError):
        sys.exit(1)
    id = data["users"][0]["_id"]
    return id

def followed():
    headers = {
               'Accept': 'application/vnd.twitchtv.v5+json',
               'Client-ID': 'qi3zqqr8r1rlrip1zlkwghx2iyxm5v',
               'Authorization': 'OAuth c5dbysxbjylvf0kosg0998zdbyq0pv',
               }
    try:
        response = requests.get('https://api.twitch.tv/kraken/streams/followed', headers=headers)
        data = response.json()
    except (KeyError, ValueError):
        sys.exit(1)
    return data

def follow(target):
    headers = {
               'Accept': 'application/vnd.twitchtv.v5+json',
               'Client-ID': 'qi3zqqr8r1rlrip1zlkwghx2iyxm5v',
               'Authorization': 'OAuth 6iea3qukkeoc8kwnac9143a7l688ob',
               }

    mine = getid("virtuetwitchbot")
    h = getid(target)
    try:
        response = requests.put(f'https://api.twitch.tv/kraken/users/{mine}/follows/channels/{h}', headers=headers)
        data = response.json()
    except (KeyError, ValueError):
        sys.exit(1)

@bot.command(aliases=['addstreamer', 'addtwitch'])
async def addst(ctx, streamer):
        try:
            follow(streamer)
            await ctx.send(f'Successfully followed {streamer}')
        except:
            await ctx.send(f'Failed to follo {streamer}')


@bot.command()
async def help(ctx):

        embed = discord.Embed(title="RLBot help", colour=discord.Colour(0x1406EF))
        embed.set_footer(text="e:)")
        embed.add_field(name="**$Rank** (Check all ranks)", value="Rank Steam {ID}\nRank PSN {PSN}\nRank XBOX {gamertag}\n\n", inline=False)
        embed.add_field(name="**$Duel** (Check 1v1 rank)", value="Duel Steam {ID}\nDuel PSN {PSN}\nDuel XBOX {gamertag}\n\n", inline=False)
        embed.add_field(name="**$Doubles** (Check 2v2 rank)", value="Doubles Steam {ID}\nDoubles PSN {PSN}\nDoubles XBOX {gamertag}\n\n", inline=False)
        embed.add_field(name="**$Standard** (Check 3v3 rank)", value="Standard Steam {ID}\nStandard PSN {PSN}\nStandard XBOX {gamertag}\n\n", inline=False)
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


        solostandardrank = livedata['data']['segments'][4]['stats']['tier']['metadata']['name']
        solostandarddiv = livedata['data']['segments'][4]['stats']['division']['metadata']['name']
        solostandardstreak = livedata['data']['segments'][4]['stats']['winStreak']['displayValue']
        solostandardMMR = livedata['data']['segments'][4]['stats']['rating']['value']

        standardrank = livedata['data']['segments'][5]['stats']['tier']['metadata']['name']
        standarddiv = livedata['data']['segments'][5]['stats']['division']['metadata']['name']
        standardstreak = livedata['data']['segments'][5]['stats']['winStreak']['displayValue']
        standardMMR = livedata['data']['segments'][5]['stats']['rating']['value']

        hoopsrank = livedata['data']['segments'][6]['stats']['tier']['metadata']['name']
        hoopsdiv = livedata['data']['segments'][6]['stats']['division']['metadata']['name']
        hoopsstreak = livedata['data']['segments'][6]['stats']['winStreak']['displayValue']
        hoopsMMR = livedata['data']['segments'][6]['stats']['rating']['value']

        rumblerank = livedata['data']['segments'][7]['stats']['tier']['metadata']['name']
        rumblediv = livedata['data']['segments'][7]['stats']['division']['metadata']['name']
        rumblestreak = livedata['data']['segments'][7]['stats']['winStreak']['displayValue']
        rumbleMMR = livedata['data']['segments'][7]['stats']['rating']['value']

        dropshotrank = livedata['data']['segments'][8]['stats']['tier']['metadata']['name']
        dropshotdiv = livedata['data']['segments'][8]['stats']['division']['metadata']['name']
        dropshotstreak = livedata['data']['segments'][8]['stats']['winStreak']['displayValue']
        dropshotMMR = livedata['data']['segments'][8]['stats']['rating']['value']

        snowdayrank = livedata['data']['segments'][9]['stats']['tier']['metadata']['name']
        snowdaydiv = livedata['data']['segments'][9]['stats']['division']['metadata']['name']
        snowdaystreak = livedata['data']['segments'][9]['stats']['winStreak']['displayValue']
        snowdayMMR = livedata['data']['segments'][9]['stats']['rating']['value']

        embed=discord.Embed(title=f"{player} Ranks", color=0x021ff7)
        embed.set_author(name="RLBot")
        embed.set_thumbnail(url=avatar)
        embed.add_field(name="**Season Reward**", value=f"{seasonReward}", inline=False)
        embed.add_field(name="**Duel**", value=f"{duelrank + ' ' + dueldiv} \nMMR: {duelMMR} \nStreak: {duelstreak}", inline=False)
        embed.add_field(name="**Doubles**", value=f"{doublesrank + ' ' + doublesdiv} \nMMR: {doublesMMR} \nStreak: {doublesstreak}", inline=False)
        embed.add_field(name="**Standard**", value=f"{standardrank + ' ' + standarddiv} \nMMR: {standardMMR} \nStreak: {standardstreak}", inline=False)
        embed.add_field(name="**Solo Standard**", value=f"{solostandardrank + ' ' + solostandarddiv} \nMMR: {solostandardMMR} \nStreak: {solostandardstreak}", inline=False)
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


            solostandardrank = livedata['data']['segments'][4]['stats']['tier']['metadata']['name']
            solostandarddiv = livedata['data']['segments'][4]['stats']['division']['metadata']['name']
            solostandardstreak = livedata['data']['segments'][4]['stats']['winStreak']['displayValue']
            solostandardMMR = livedata['data']['segments'][4]['stats']['rating']['value']

            standardrank = livedata['data']['segments'][5]['stats']['tier']['metadata']['name']
            standarddiv = livedata['data']['segments'][5]['stats']['division']['metadata']['name']
            standardstreak = livedata['data']['segments'][5]['stats']['winStreak']['displayValue']
            standardMMR = livedata['data']['segments'][5]['stats']['rating']['value']

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

    doublesrank = livedata['data']['segments'][3]['stats']['tier']['metadata']['name']
    doublesdiv = livedata['data']['segments'][3]['stats']['division']['metadata']['name']
    doublesstreak = livedata['data']['segments'][3]['stats']['winStreak']['displayValue']
    doublesMMR = livedata['data']['segments'][3]['stats']['rating']['value']


    solostandardrank = livedata['data']['segments'][4]['stats']['tier']['metadata']['name']
    solostandarddiv = livedata['data']['segments'][4]['stats']['division']['metadata']['name']
    solostandardstreak = livedata['data']['segments'][4]['stats']['winStreak']['displayValue']
    solostandardMMR = livedata['data']['segments'][4]['stats']['rating']['value']

    standardrank = livedata['data']['segments'][5]['stats']['tier']['metadata']['name']
    standarddiv = livedata['data']['segments'][5]['stats']['division']['metadata']['name']
    standardstreak = livedata['data']['segments'][5]['stats']['winStreak']['displayValue']
    standardMMR = livedata['data']['segments'][5]['stats']['rating']['value']

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

    duelrank = livedata['data']['segments'][2]['stats']['tier']['metadata']['name']
    dueldiv = livedata['data']['segments'][2]['stats']['division']['metadata']['name']
    duelstreak = livedata['data']['segments'][2]['stats']['winStreak']['displayValue']
    duelMMR = livedata['data']['segments'][2]['stats']['rating']['value']

    doublesrank = livedata['data']['segments'][3]['stats']['tier']['metadata']['name']
    doublesdiv = livedata['data']['segments'][3]['stats']['division']['metadata']['name']
    doublesstreak = livedata['data']['segments'][3]['stats']['winStreak']['displayValue']
    doublesMMR = livedata['data']['segments'][3]['stats']['rating']['value']


    solostandardrank = livedata['data']['segments'][4]['stats']['tier']['metadata']['name']
    solostandarddiv = livedata['data']['segments'][4]['stats']['division']['metadata']['name']
    solostandardstreak = livedata['data']['segments'][4]['stats']['winStreak']['displayValue']
    solostandardMMR = livedata['data']['segments'][4]['stats']['rating']['value']

    standardrank = livedata['data']['segments'][5]['stats']['tier']['metadata']['name']
    standarddiv = livedata['data']['segments'][5]['stats']['division']['metadata']['name']
    standardstreak = livedata['data']['segments'][5]['stats']['winStreak']['displayValue']
    standardMMR = livedata['data']['segments'][5]['stats']['rating']['value']

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

    duelrank = livedata['data']['segments'][2]['stats']['tier']['metadata']['name']
    dueldiv = livedata['data']['segments'][2]['stats']['division']['metadata']['name']
    duelstreak = livedata['data']['segments'][2]['stats']['winStreak']['displayValue']
    duelMMR = livedata['data']['segments'][2]['stats']['rating']['value']

    doublesrank = livedata['data']['segments'][3]['stats']['tier']['metadata']['name']
    doublesdiv = livedata['data']['segments'][3]['stats']['division']['metadata']['name']
    doublesstreak = livedata['data']['segments'][3]['stats']['winStreak']['displayValue']
    doublesMMR = livedata['data']['segments'][3]['stats']['rating']['value']


    solostandardrank = livedata['data']['segments'][4]['stats']['tier']['metadata']['name']
    solostandarddiv = livedata['data']['segments'][4]['stats']['division']['metadata']['name']
    solostandardstreak = livedata['data']['segments'][4]['stats']['winStreak']['displayValue']
    solostandardMMR = livedata['data']['segments'][4]['stats']['rating']['value']

    standardrank = livedata['data']['segments'][5]['stats']['tier']['metadata']['name']
    standarddiv = livedata['data']['segments'][5]['stats']['division']['metadata']['name']
    standardstreak = livedata['data']['segments'][5]['stats']['winStreak']['displayValue']
    standardMMR = livedata['data']['segments'][5]['stats']['rating']['value']

    embed=discord.Embed(title=f"{player} Ranks", color=0x021ff7)
    embed.set_author(name="RLBot")
    embed.set_thumbnail(url=avatar)
    embed.add_field(name="**Duel**", value=f"{duelrank + ' ' + dueldiv} \nMMR: {duelMMR} \nStreak: {duelstreak}", inline=False)
    embed.set_footer(text="e:)")

    await ctx.send(embed=embed)

@bot.command()
async def feed(ctx, platform, player):
    livedata = getData(platform, player)
    avatar = livedata['data']['platformInfo']['avatarUrl']
    livedata = getsessData(platform, player)

    result1 = livedata['data']['items'][0]['matches'][0]['metadata']['result']
    playlist1 = livedata['data']['items'][0]['matches'][0]['metadata']['playlist']
    MMR1 = livedata['data']['items'][0]['matches'][0]['stats']['rating']['displayValue']
    delta1 = livedata['data']['items'][0]['matches'][0]['stats']['rating']['metadata']['ratingDelta']
    tier1 = livedata['data']['items'][0]['matches'][0]['stats']['rating']['metadata']['tier']
    div1 = livedata['data']['items'][0]['matches'][0]['stats']['rating']['metadata']['division']

    result2 = livedata['data']['items'][0]['matches'][1]['metadata']['result']
    playlist2 = livedata['data']['items'][0]['matches'][1]['metadata']['playlist']
    MMR2 = livedata['data']['items'][0]['matches'][1]['stats']['rating']['displayValue']
    delta2 = livedata['data']['items'][0]['matches'][1]['stats']['rating']['metadata']['ratingDelta']
    tier2 = livedata['data']['items'][0]['matches'][1]['stats']['rating']['metadata']['tier']
    div2 = livedata['data']['items'][0]['matches'][1]['stats']['rating']['metadata']['division']

    result3 = livedata['data']['items'][0]['matches'][2]['metadata']['result']
    playlist3 = livedata['data']['items'][0]['matches'][2]['metadata']['playlist']
    MMR3 = livedata['data']['items'][0]['matches'][2]['stats']['rating']['displayValue']
    delta3 = livedata['data']['items'][0]['matches'][2]['stats']['rating']['metadata']['ratingDelta']
    tier3 = livedata['data']['items'][0]['matches'][2]['stats']['rating']['metadata']['tier']
    div3 = livedata['data']['items'][0]['matches'][2]['stats']['rating']['metadata']['division']

    result4 = livedata['data']['items'][0]['matches'][3]['metadata']['result']
    playlist4 = livedata['data']['items'][0]['matches'][3]['metadata']['playlist']
    MMR4 = livedata['data']['items'][0]['matches'][3]['stats']['rating']['displayValue']
    delta4 = livedata['data']['items'][0]['matches'][3]['stats']['rating']['metadata']['ratingDelta']
    tier4 = livedata['data']['items'][0]['matches'][3]['stats']['rating']['metadata']['tier']
    div4 = livedata['data']['items'][0]['matches'][3]['stats']['rating']['metadata']['division']

    result5 = livedata['data']['items'][0]['matches'][4]['metadata']['result']
    playlist5 = livedata['data']['items'][0]['matches'][4]['metadata']['playlist']
    MMR5 = livedata['data']['items'][0]['matches'][4]['stats']['rating']['displayValue']
    delta5 = livedata['data']['items'][0]['matches'][4]['stats']['rating']['metadata']['ratingDelta']
    tier5 = livedata['data']['items'][0]['matches'][4]['stats']['rating']['metadata']['tier']
    div5 = livedata['data']['items'][0]['matches'][4]['stats']['rating']['metadata']['division']

    embed=discord.Embed(title=f"{player}'s feed", color=0x021ff7)
    embed.set_author(name="RLBot")
    embed.set_thumbnail(url=avatar)
    embed.add_field(name=f"**{result1}**", value=f"{tier1 + ' ' + div1} \n{playlist1} \n{'MMR: ' + str(MMR1) } \n{'Change: ' + str(delta1)}\n ", inline=False)
    embed.add_field(name=f"**{result2}**", value=f"{tier2 + ' ' + div2} \n{playlist2} \n{'MMR: ' + str(MMR2) } \n{'Change: ' + str(delta2)}\n ", inline=False)
    embed.add_field(name=f"**{result3}**", value=f"{tier3 + ' ' + div3} \n{playlist3} \n{'MMR: ' + str(MMR3) } \n{'Change: ' + str(delta3)}\n ", inline=False)
    embed.add_field(name=f"**{result4}**", value=f"{tier4 + ' ' + div4} \n{playlist4} \n{'MMR: ' + str(MMR4) } \n{'Change: ' + str(delta4)}\n ", inline=False)
    embed.add_field(name=f"**{result5}**", value=f"{tier5 + ' ' + div5} \n{playlist5} \n{'MMR: ' + str(MMR5) } \n{'Change: ' + str(delta5)}\n ", inline=False)
    embed.set_footer(text="e:)")

    await ctx.send(embed=embed)

bot.run('NzEwNTE2NjcxMTg5NzQ1Njgz.Xr1mNw.FKVXiaH8isZFg8OVuX3xND7WbIw')
