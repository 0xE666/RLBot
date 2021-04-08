import discord, requests, re, json, time, asyncio, random, os
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
from functions import *
import functions as RL

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
    embed.add_field(name="**$Rank** (Check all ranks)", value="Rank Steam {ID}\nRank Epic {ID}\nRank PSN {PSN}\nRank XBL {gamertag}\n\n", inline=False)
    embed.add_field(name="**$Duel** (Check 1v1 rank)", value="Duel Steam {ID}\nDuel Epic {ID}\nDuel PSN {PSN}\nDuel XBL {gamertag}\n\n", inline=False)
    embed.add_field(name="**$Doubles** (Check 2v2 rank)", value="Doubles Steam {ID}\nDoubles Epic {ID}\nDoubles PSN {PSN}\nDoubles XBL {gamertag}\n\n", inline=False)
    embed.add_field(name="**$Standard** (Check 3v3 rank)", value="Standard Steam {ID}\nStandard Epic {ID}\nStandard PSN {PSN}\nStandard XBL {gamertag}\n\n", inline=False)
    embed.add_field(name="**$Price** (Check price of item)", value="Price White Octane { e.g.Price Black Dieci -exotic}\n\n", inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=['ranks', 'ran', 'rankk'])
async def rank(ctx, platform, player):
    searchPlayer(platform, player)
    embed=discord.Embed(title=f"{RL.playerName} Ranks\n(Views: {RL.profileViews})", color=0x021ff7)
    embed.set_author(name="RLBot")
    if RL.avatar == 'None':
        embed.set_thumbnail(url='https://trackercdn.com/cdn/tracker.gg/rocket-league/ranks/s4-0.png')
    else:
        embed.set_thumbnail(url=RL.avatar)
    embed.add_field(name="**Season Reward**", value=f"{RL.seasonRewards}", inline=False)
    embed.add_field(name="**Duel**", value=f"{RL.duel}", inline=False)
    embed.add_field(name="**Doubles**", value=f"{RL.doubles}", inline=False)
    embed.add_field(name="**Standard**", value=f"{RL.standard}", inline=False)
    embed.add_field(name="**Hoops**", value=f"{RL.hoops}", inline=False)
    embed.add_field(name="**Rumble**", value=f"{RL.rumble}", inline=False)
    embed.add_field(name="**Dropshot**", value=f"{RL.dropshot}", inline=False)
    embed.add_field(name="**Snowday**", value=f"{RL.snowday}", inline=False)
    embed.set_footer(text="e:)")
    await ctx.send(embed=embed)

@bot.command(aliases=['ones', '1s', '1'])
async def duel(ctx, platform, player):
    searchPlayer(platform, player)
    embed=discord.Embed(title=f"{RL.playerName} Ranks\n(Views: {RL.profileViews})", color=0x021ff7)
    embed.set_author(name="RLBot")
    if RL.avatar == 'None':
        embed.set_thumbnail(url='https://trackercdn.com/cdn/tracker.gg/rocket-league/ranks/s4-0.png')
    else:
        embed.set_thumbnail(url=RL.avatar)
    embed.add_field(name="**Season Reward**", value=f"{RL.seasonRewards}", inline=False)
    embed.add_field(name="**Duel**", value=f"{RL.duel}", inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=['twos', '2s', '2'])
async def doubles(ctx, platform, player):
    searchPlayer(platform, player)
    embed=discord.Embed(title=f"{RL.playerName} Ranks\n(Views: {RL.profileViews})", color=0x021ff7)
    embed.set_author(name="RLBot")
    if RL.avatar == 'None':
        embed.set_thumbnail(url='https://trackercdn.com/cdn/tracker.gg/rocket-league/ranks/s4-0.png')
    else:
        embed.set_thumbnail(url=RL.avatar)
    embed.add_field(name="**Season Reward**", value=f"{RL.seasonRewards}", inline=False)
    embed.add_field(name="**Doubles**", value=f"{RL.doubles}", inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=['threes', '3s', '3'])
async def standard(ctx, platform, player):
    searchPlayer(platform, player)
    embed=discord.Embed(title=f"{RL.playerName} Ranks\n(Views: {RL.profileViews})", color=0x021ff7)
    embed.set_author(name="RLBot")
    if RL.avatar == 'None':
        embed.set_thumbnail(url='https://trackercdn.com/cdn/tracker.gg/rocket-league/ranks/s4-0.png')
    else:
        embed.set_thumbnail(url=RL.avatar)
    embed.add_field(name="**Season Reward**", value=f"{RL.seasonRewards}", inline=False)
    embed.add_field(name="**Standard**", value=f"{RL.standard}", inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=['prices', 'pric', 'check'])
async def price(ctx, *, item):
    itemInfo = grabItem(item)
    if itemInfo[0] == 'options':
        embed=discord.Embed(title=f"Multiple options for {item}", color=0x021ff7)
        embed.set_author(name="RLBot")
        embed.set_thumbnail(url=itemInfo[0]['pictureURL'])
        embed.add_field(name="**Options**", value=f"$price item -itemType (e.g. -exotic -uncommon -trail)", inline=False)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title=f"{itemInfo[2]}", color=0x021ff7, url=itemInfo[0])
        embed.set_author(name="RLBot")
        embed.set_thumbnail(url=itemInfo[1])
        embed.add_field(name=f"**{itemInfo[2]} Price**", value=f"{itemInfo[3]} Credits", inline=False)
        await ctx.send(embed=embed)



bot.run('TOKEN')