import sqlite3
import json
import discord
from discord.ext import commands
from utilities import convert, INSERT_MEMBER, INSERT_MEMBERS, INSERT_PLAYERS, INSERT_INVENTORIES, SELECT,  DROP,  GET,  UPDATE
from economy import ework, insert_job, remove_job, insert_item, remove_item, buy_item

with open("info.json") as file :
    TOKEN = json.load(file).get("TOKEN")
    
connection = sqlite3.connect("data/database.db")
cursor = connection.cursor()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='m!', intents=discord.Intents.all())

def is_admin(ctx):
        if ctx.message.author.id == 664127746896822292: return True
        return False


# *********************************************#
#               admin  commands             #
# *********************************************#

@bot.command()
async def make_database(ctx):
    if is_admin(ctx):
        try:
            cursor.execute("""
                CREATE TABLE Members (
                    MemberID    INT    NOT NULL ,
                    NickName varchar(300),
                    Name varchar(300) NOT NULL,
                    Member int NOT NULL,
                    PRIMARY KEY (MemberID)
                )
            """)
        except :
            print("nope")
        try:
            cursor.execute("""
                CREATE TABLE Players (
                    PlayerID    INT    NOT NULL,
                    MemberID    INT    NOT NULL ,
                    JobID    INT    DEFAULT 1 ,
                    Money    INT    DEFAULT 1000 ,
                    Level    INT    DEFAULT 1 ,
                    Player    INT    NOT NULL ,
                    Worked INT DEFAULT 0 ,
                    FOREIGN KEY    (MemberID)    REFERENCES Persons(MemberID) ,
                    FOREIGN KEY (JobID)    REFERENCES Persons(JobID) ,
                    PRIMARY KEY (PlayerID)
                )
            """)
        except :
            print("nope")
        try:
            cursor.execute("""
                CREATE TABLE Inventories (
                    InventoryID INT NOT NULL PRIMARY KEY ,
                    MemberID    INT    NOT NULL ,
                    Inventory varchar(1000) NOT NULL ,
                    Bag TEXT DEFAULT "[]",
                    FOREIGN KEY    (MemberID)    REFERENCES Persons(MemberID) 
                )
            """)
        except :
            print("nope")
        try:
            INSERT_MEMBERS(bot.get_all_members())
        except :
            print("nope")
        try:
            INSERT_PLAYERS()
        except :
            print("nope")
        try:
            INSERT_INVENTORIES()
        except :
            print("nope")
        
        await ctx.message.channel.send("DATA BASE CREATED")
    else:
        await ctx.message.channel.send("You must be an ADMIN to use this command")


@bot.command()
async def drop_database(ctx):
    if is_admin(ctx):
        DROP("Members")
        DROP("Players")
        DROP("Inventories")
        await ctx.message.reply("DATABASE DELETED")
    else:
        await ctx.message.channel.send("You must be an ADMIN to use this command")
        
        
@bot.command()
async def drop(ctx, table):
    if is_admin(ctx):
        DROP(table)
        await ctx.message.reply("DATABASE DELETED")
    else:
        await ctx.message.channel.send("You must be an ADMIN to use this command")
        
        
@bot.command()
async def admin_members(ctx):
    if is_admin(ctx):
        await ctx.message.channel.send(str(
            SELECT("Members")
        ))
    else:
        await ctx.message.channel.send("You must be an ADMIN to use this command")

@bot.command()
async def admin_players(ctx):
    if is_admin(ctx):
        await ctx.message.channel.send(str(
            SELECT("Players")
        ))
    else:
        await ctx.message.channel.send("You must be an ADMIN to use this command")

    

@bot.command()
async def admin_jobs(ctx):
    if is_admin(ctx):
        await ctx.message.channel.send(str(
            SELECT("Jobs")
        ))
    else:
        await ctx.message.channel.send("You must be an ADMIN to use this command")


@bot.command()
async def admin_items(ctx):
    if is_admin(ctx):
        await ctx.message.channel.send(str(
            SELECT("Items")
        ))
    else:
        await ctx.message.channel.send("You must be an ADMIN to use this command")
    
    
@bot.command()
async def admin_inventories(ctx):
    if is_admin(ctx):
        await ctx.message.channel.send(str(
            SELECT("Inventories")
        ))
    else:
        await ctx.message.channel.send("You must be an ADMIN to use this command")
    

@bot.command()
async def add_job(ctx, title, level, paycheck, multiplier):
    if is_admin(ctx):
        insert_job(title , int(level) , int(paycheck) , int(multiplier))
        await ctx.message.channel.send("DONE")
    else:
        await ctx.message.channel.send("You must be an ADMIN to use this command")
        

@bot.command()
async def delete_job(ctx, title):
    if is_admin(ctx):
        remove_job(title)
        await ctx.message.channel.send("DONE")
    else:
        await ctx.message.channel.send("You must be an ADMIN to use this command")


@bot.command()
async def add_item(ctx, title, level, price, attack, defend):
    if is_admin(ctx):
        level, price, attack, defend = int(level), int(price), int(attack), int(defend)
        insert_item(title , level, price, attack, defend)
        await ctx.message.channel.send("DONE")
    else:
        await ctx.message.channel.send("You must be an ADMIN to use this command")
        

@bot.command()
async def delete_item(ctx, title):
    if is_admin(ctx):
        remove_item(title)
        await ctx.message.channel.send("DONE")
    else:
        await ctx.message.channel.send("You must be an ADMIN to use this command")


@bot.command()
async def give_money(ctx, amount ,user):
    if is_admin(ctx):
        amount = int(amount)
        id = int(user[2:-1])
        money = GET("Players", "Player", id)[3]
        UPDATE("Players", "Player", id, "Money", money+amount)
        await ctx.message.channel.send("DONE")
    else:
        await ctx.message.channel.send("You must be an ADMIN to use this command")


@bot.command()
async def take_money(ctx, amount ,user):
    if is_admin(ctx):
        amount = int(amount)
        id = int(user[2:-1])
        money = GET("Players", "Player", id)[3]
        UPDATE("Players", "Player", id, "Money", money-amount)
        await ctx.message.channel.send("DONE")
    else:
        await ctx.message.channel.send("You must be an ADMIN to use this command")
        
        
@bot.command()
async def create_job_channels(ctx):
    if is_admin(ctx):
        category = bot.get_channel(1063477575491539078)
        jobs = SELECT("Jobs")
        print(ctx.message.guild)
        for i in jobs:
            title = i[1]
            await ctx.message.guild.create_text_channel(title, category = category)
        await ctx.message.channel.send("DONE")
    else:
        await ctx.message.channel.send("You must be an ADMIN to use this command")
        

@bot.command()
async def change_job_text(ctx, job, *args):
    if is_admin(ctx):
        text = ""
        for i in args :
            text+=f"{i} "
        UPDATE("Jobs", "Title", f"'{job}'", "Text", text)
        await ctx.message.channel.send("DONE")
    else:
        await ctx.message.channel.send("You must be an ADMIN to use this command")

# *********************************************#
#               normal commands             #
# *********************************************#

@bot.event
async def on_ready():
    print("Ready")
    a = await bot.fetch_channel(745528903136837692)
    await a.send("پدرت بیدار شد")
    
@bot.event
async def on_member_join(member):
    INSERT_MEMBER(member)


@bot.command()
async def ding (ctx):
    await ctx.message.author.send("dong")


@bot.command()
async def id (ctx):
    await ctx.message.channel.send(f"""
        Your Id : {ctx.message.author.id}
    """)
        
        
# *********************************************#
#            economy commands            #
# *********************************************#
        
        
@commands.cooldown(1, 3600, commands.BucketType.user)
@bot.command()
async def work(ctx):
    data = ework(ctx.message.author.id)
    job = data[1]
    job_description = GET("Jobs", "Title", job)[-1]
    money = data[0][3]
    worked = data[2]
    msg = discord.Embed(title="کونتون پاره شد", description=f"""
        **پول شما : {money} :moneybag: **
        **شغل : {job} :oncoming_automobile: **
        **انقدر کار کردین : {worked} :pick: **
    """, color=0x7692FF)
    print("here")
    await ctx.message.channel.send(embed = msg)
    
    msg = discord.Embed(title=f"""
        {ctx.message.author.name} {job_description}
    """,
    color=0x84A98C
    )
    print(job.lower())

    for channel in bot.get_all_channels():
        if channel.name == job.lower():
            await channel.send(embed=msg)
    
        
        
@work.error
async def work_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"You are in cooldown",description=f"Try again in {convert(error.retry_after)}", color=discord.Color.red())
        await ctx.send(embed=em)
        
@bot.command()
async def profile(ctx):
    id = ctx.message.author.id
    player = GET("Players", "Player", id)
    member = GET("Members", "Member", id)
    job = GET("Jobs", "JobID", player[2])
    name , jobtitle, money, level, worked = member[2], job[1], player[3], player[4], player[6]
    
    msg = discord.Embed(title=f"""
        Your Profile :page_facing_up:
    """,
    description=f"""
        **Id : {id}**
        **Name : {name} :identification_card: **
        **Job : {jobtitle} :oncoming_automobile: **
        **Money : {money} :coin: **
        **Level : {level} :straight_ruler: **
        **You have worked {worked} times :pick: **
    """, color=0x2EC4B6
    )
    
    await ctx.message.channel.send(embed = msg)


@bot.command()
async def items(ctx):
    item_list = SELECT("Items")
    sorted = []
    for data in item_list :
        sorted.append({
            "id": data[0],
            "title": data[1],
            "level": data[2],
            "price": data[3],
            "attack": data[4],
            "defend": data[5]
        })
    desc = """"""
    for data in sorted :
        desc += f"""
            **Item Id : {data["id"]}**
                **- Name : {data["title"]}**
                **- Level : {data["level"]}**
                **- Price : {data["price"]}**
                **- Attack : {data["attack"]}**
                **- Defend : {data["defend"]}**
                
        """
    desc += f"""
    
    
        write m!buy *ITEM ID* in order to buy the item
        
        
    """
    msg = discord.Embed(
        title=f"""
            :hammer: :axe: Items :hammer_pick: :carpentry_saw: 
        """,
        description=desc,
        color=0x3E92CC
    )
    
    await ctx.message.channel.send(embed=msg)


@bot.command()
async def buy (ctx, item_id=None):
    if item_id is None:
        await ctx.message.reply(f"""**You need to pass an item id in order to buy an item ( run m!items to get item ids )**""")
    else:
        result = buy_item(ctx.message.author.id, item_id)
        if  result[0] == 200:
            msg = discord.Embed(
                title=f"""
                    Success Item bought :white_check_mark:
                """,
                description=f"""
                    ** Item : {result[2]} **
                    ** Account balance : {result[1]} **
                """,
                color=0x4bb543
            )
        elif result[0] == 400 :
            msg = discord.Embed(
                title=f"""
                    Fail Not enough money :x:
                """,
                description=f""" 
                    ** Item : {result[2]} **
                    ** Price : {result[3]} **
                    ** Account balance : {result[1]} **
                """,
                color=0xFA113D
            )
        await ctx.message.channel.send(embed=msg)


bot.run(TOKEN)