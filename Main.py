import psycopg2
from dotenv import dotenv_values
from discord.ext import commands
import psycopg2 as psy
from datetime import date
import sys

bot = commands.Bot(command_prefix='+')

@bot.event
async def on_ready():
    print("Bot ready!")


@bot.event
async def on_member_join(member):
    print(member + " joined!")


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
    adder_disc_id = str(ctx.author.id)
    server_id = str(ctx.guild.id)
    cur.execute("SELECT userid FROM users WHERE discordid=%s AND serverid=%s;", (adder_disc_id, server_id))
    adder_rsp = cur.fetchall()
    if VERBOSE:
        print(adder_rsp)
    if len(adder_rsp) > 1:
        send_db_error(ctx, error_msg="Discord & Serverid double DB entry.")
        if VERBOSE:
            print(f"More than on entry in DB for discordID: {adder_disc_id} and serverID: {server_id}!\n")
            print(adder_rsp + "\n")
        return
    elif len(adder_rsp) == 1:
        adder_id = adder_rsp[0][0]
    else:
        ctx.send("You are trying to add a comment without being signed-up on this server\n"
                 "Please use \"+signup\" first.")
        return
    cur.execute("SELECT userid FROM users WHERE name=%s and serverid=%s;", (author, server_id))
    author_rsp = cur.fetchall()
    if VERBOSE:
        print(author_rsp)
    if len(author_rsp) > 1:
        send_db_error(ctx, error_msg="Name and Serverid double DB entry")
        if VERBOSE:
            print(f"More than on entry in DB for name: {author} and serverID: {server_id}!\n")
            print(author_rsp + "\n")
        return
    elif len(author_rsp) == 1:
        author_id = author_rsp[0][0]
    else:
        ctx.send("You are trying to add a quote to a user that does not exist.\n"
                 "Please check \"+users\" first.")
        return
    py_date = date.today()
    sql_date = psy.Date(py_date.year, py_date.month, py_date.day)
    sql = "INSERT INTO quotes (authorid, addedbyid, serverid, content, created) " \
          "VALUES (%s, %s, %s, %s, %s);"
    cur.execute(sql, (author_id, adder_id, server_id, quote, sql_date))
    conn.commit()
    await ctx.send("**\"" + quote + "\"" + " Author: " + author + "** was added!")


@bot.command(aliases=["users"])
async def show_users(ctx):
    server_id = str(ctx.guild.id)
    server_users = get_server_users(server_id)
    answer_string = "Following users exist on this server:\n"
    for user in server_users:
        answer_string += user[0] + "   "
    await ctx.send(answer_string)

@bot.command(aliases=["signup"])
async def sign_up(ctx, name=""):
    # Check if user already signed up:
    discord_id = str(ctx.author.id)
    server_id = str(ctx.guild.id)
    cur.execute("SELECT * FROM users WHERE discordid=%s AND serverid=%s", (discord_id, server_id))
    response = cur.fetchall()
    if len(response) > 1:
        send_db_error(ctx)
        if VERBOSE:
            print(response)
    elif len(response) != 0:
        if VERBOSE:
            print("Already signed up!")
            return
        await ctx.send("You are already signed-up on this server! :)")

    if name != "":
        user_name = name
    else:
        user_name = ctx.author.display_name
    if len(user_name) > 30:
        await ctx.send("Your Name on this server (or the one you specified is too long!\n"
                       "Specify a custom name with \"+signup *your name*\"\n"
                       "Names can be no longer than 30 characters.")
        return
    py_date = date.today()
    sql_date = psy.Date(py_date.year, py_date.month, py_date.day)
    sql = "INSERT INTO users (discordid, serverid, name, created) VALUES (%s, %s, %s, %s);"
    data = (discord_id, server_id, user_name, sql_date)
    if VERBOSE:
        print(f"Signup execute: {data}")
    cur.execute(sql, data)
    conn.commit()


@bot.command(aliases=["qby", "quotesby"])
async def quotes_by(ctx):
    #TODO REFACTOR SQL QUERRY LOGIC
    # TEST EXCEPTION
    raise psy.IntegrityError("Test exception")


async def send_db_error(ctx, error_msg):
    await ctx.send("Something seems wrong in the database. Please contact an admin.")
    if error_msg != "":
        raise psy.IntegrityError(error_msg)
    else:
        psy.IntegrityError()

def get_server_users(server_id):
    cur.execute("SELECT name FROM users WHERE serverid=%s;", (server_id,))
    return cur.fetchall()


if __name__ == '__main__':
    # Parse arguments
    if len(sys.argv) > 2:
        print("Wrong usage: try with -h for help!")
        exit(0)
    elif "-h" in sys.argv:
        print("Help:\n"
              "-v: verbose mode\n"
              "-h: print this help")
        exit(0)
    elif "-v" in sys.argv:
        VERBOSE = True
    else:
        VERBOSE = False

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
