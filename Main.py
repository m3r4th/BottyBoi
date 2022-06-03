from dotenv import dotenv_values
# import discord
from discord.ext import commands

# Set prefix and initialize
bot = commands.Bot(command_prefix='+')

@bot.event
async def on_ready():
    print("Bot ready!")


@bot.event
async def on_member_join(member):
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

@bot.command(aliases=["guild"])
async def guild_id(ctx):
    await ctx.send(f"Guild-ID is {ctx.guild.id}")


@bot.command(aliases=["addq"])
async def addQ(ctx, author, quote):
    await ctx.send("**\"" + quote + "\"" + " Author: " + author + "** was added!")


if __name__ == '__main__':
    # Get token from .env
    token = dotenv_values("token.env").get("DISCORD_TOKEN")
    bot.run(token)
