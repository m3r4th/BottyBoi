from dotenv import dotenv_values
# import discord
from discord.ext import commands
import psycopg2 as psy
from datetime import date

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
async def add_q(ctx, author, quote):
    await ctx.send("**\"" + quote + "\"" + " Author: " + author + "** was added!")

@bot.command(aliases=["signup"])
async def sign_up(ctx, name=""):
    discord_id = ctx.author.id
    server_id = ctx.guild.id
    if name != "":
        user_name = name
    else:
        user_name = ctx.author.display_name
    py_date = date.today()
    sql_date = psy.Date(py_date.year, py_date.month, py_date.day)
    print(sql_date)
    sql = "INSERT INTO users (discordid, serverid, name, created) VALUES (%s, %s, %s, %s);"
    data = (discord_id, server_id, user_name, sql_date)
    cur.execute(sql, data)

if __name__ == '__main__':
    # Get token from .env
    token = dotenv_values("token.env").get("DISCORD_TOKEN")
    db_env = dotenv_values("db.env")
    db_name = db_env.get("DB_NAME")
    db_user = db_env.get("DB_USER")
    db_host = db_env.get("DB_HOST")
    db_port = db_env.get("DB_PORT")
    db_pw = db_env.get("DB_PASSWORD")
    conn = psy.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host, port=db_port)
    cur = conn.cursor()
    bot.run(token)
