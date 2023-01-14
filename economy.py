from utilities import DELETE, INSERT_INTO, UPDATE, GET
import sqlite3

connection = sqlite3.connect("data/database.db")
cursor = connection.cursor()

def insert_job(title, level, paycheck, multiplier):
    INSERT_INTO(table="Jobs", tableid="JobID", columns=["Title", "Level", "PayCheck", "Multiplier"], values=[title, level, paycheck, multiplier])
    

def remove_job(title):
    DELETE(table="Jobs", column="Title", value=title)
    
    
def insert_item(title, level, price, attack, defend):
    INSERT_INTO(table="Items", tableid="ItemID", columns=["Title", "Level", "Price", "Attack", "Defend"], values=[title, level, price, attack, defend])
    

def remove_item(title):
    DELETE(table="Items", column="Title", value=title)

    
def ework(memberID):
    player = cursor.execute(f"""
        SELECT * FROM Players WHERE Player = {memberID}
    """).fetchall()[0]
    
    jobId = player[2]
    money = player[3]
    
    job = cursor.execute(f"""
        SELECT * FROM Jobs WHERE JobID = {jobId}
    """).fetchall()[0]
    
    paycheck = job[3]
    multiplier = job[4]
    jobtitle = job[1]
    worked = player[6]+1
    level = job[2]
    
    
    money += paycheck * multiplier
    
    UPDATE("Players", "Player", memberID, "Money", money)
    UPDATE("Players", "Player", memberID, "Worked", worked)
    
    
    if worked // 10 >= level :
        level += 1
        new_job = cursor.execute(f"""
            SELECT * FROM Jobs WHERE Level = {level}
        """).fetchall()[0]
        new_job_id = new_job[0]
        jobtitle = new_job[1]
        UPDATE("Players", "Player", memberID, "JobID", new_job_id)
    
    return [cursor.execute(f"""
        SELECT * FROM Players WHERE Player = {memberID}
    """).fetchall()[0], jobtitle, worked]
    
    
def money(do, id, amount):
    player = GET("Players", "Player", id)
    money = player[3]
    if do :
        money += amount
    else :
        money -= amount
    UPDATE("Players", "Player", id, "Money", money)
    

def buy_item(id, item_id):
    item_id = int(item)
    player = GET("Players", "Player", id)
    money = player[3]
    item = GET("Items", "ItemID", item_id)
    price = item[3]
    inventory = GET("Inventories", "Inventory", id)
    bag = inventory[-1]    
    if money >= price :
        print("bought")
        
        
    else:
        print("not enough money")