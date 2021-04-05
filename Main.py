from dotenv import dotenv_values
# Get Token from .env
token = dotenv_values("token.env").get("DISCORD_TOKEN")
#Set prefix and initalize
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='+')

@bot.event
async def on_ready():
    print("Bot ready!")

@bot.event
async def on_member_koin(member):
    print(member + " joined")

@bot.event
async def on_member_remove(member):
    pass

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! " + str(round(bot.latency * 1000)) + "ms")

@bot.command()
async def ding(ctx):
    await ctx.send("Dong!")

@bot.command(aliases=["addq"])
async def addQ(ctx, author, quote):
    await ctx.send("**\"" + quote + "\"" + " Author: " + author + "** was added!")

bot.run(token)
