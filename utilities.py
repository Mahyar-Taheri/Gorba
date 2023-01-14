import sqlite3
import json

connection = sqlite3.connect("data/database.db")
cursor = connection.cursor()

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60      
    return "%d:%02d:%02d" % (hour, minutes, seconds)
    

def INSERT_MEMBERS (members) :
    pk = 1
    for member in members:
        if member.bot == False:
            nick, name, id = member.nick, member.name, member.id
            if nick is None :
                insert_member = f"""
                   INSERT INTO Members (MemberID,Member,Name) VALUES ({pk}, {id}, '{name}')
                """
            else:
                insert_member = f"""
                    INSERT INTO Members (MemberID,Member,Name,NickName) VALUES ({pk}, {id}, '{name}', '{nick}')
                 """
                 
            cursor.execute(insert_member)
            pk += 1
    connection.commit()
    

def INSERT_MEMBER (member):
    pk = cursor.execute("""
        SELECT * FROM Members ORDER BY MemberId DESC LIMIT 1
    """).fetchall()[0][0]+1
    
    if member.bot == False:
        nick, name, id = member.nick, member.name, member.id
        if nick is None :
            insert_member = f"""
               INSERT INTO Members (MemberID,Member,Name) VALUES ({pk}, {id}, '{name}')
            """
        else:
            insert_member = f"""
                INSERT INTO Members (MemberID,Member,Name,NickName) VALUES ({pk}, {id}, '{name}', '{nick}')
             """
             
        cursor.execute(insert_member)
        connection.commit()
        
        
def INSERT_PLAYERS ():
    least_pk = cursor.execute("""
    SELECT MAX(PlayerId) FROM Players
    """).fetchall()[0][0]
    max_pk = cursor.execute("""
    SELECT MAX(MemberId) FROM Members
    """).fetchall()[0][0]
    
    if least_pk is None :
        least_pk = 1
        
    if least_pk == max_pk :
        return 0
    
    members = cursor.execute(f"""
        SELECT * FROM Members WHERE MemberID BETWEEN {least_pk} AND {max_pk}
    """).fetchall()
    
    for member in members :
        pk = member[0]
        id = member[-1]
        cursor.execute(f"""
            INSERT INTO Players (PlayerID,MemberID, Player) VALUES ({pk}, {pk}, {id})
        """)
    
    connection.commit()


def INSERT_INVENTORIES ():
    least_pk = cursor.execute("""
    SELECT MAX(InventoryID) FROM Inventories
    """).fetchall()[0][0]
    max_pk = cursor.execute("""
    SELECT MAX(MemberId) FROM Members
    """).fetchall()[0][0]
    
    if least_pk is None :
        least_pk = 1
        
    if least_pk == max_pk :
        return 0
    
    members = cursor.execute(f"""
        SELECT * FROM Members WHERE MemberID BETWEEN {least_pk} AND {max_pk}
    """).fetchall()
    
    for member in members :
        pk = member[0]
        id = member[-1]
        cursor.execute(f"""
            INSERT INTO Inventories (InventoryID,MemberID, Inventory) VALUES ({pk}, {pk}, {id})
        """)
    
    connection.commit()


def UPDATE_PLAYERS (id ,update_this, to_this):
    if type(to_this) == type(0):
        cursor.execute(f"""
            UPDATE Players SET {update_this} =  {to_this} WHERE Player = {id}
        """)
    elif type(to_this) == type(""):
        cursor.execute(f"""
            UPDATE Players SET {update_this} =  "{to_this}" WHERE Player = {id}
        """)
    connection.commit()
    
    return cursor.execute(f"""
        SELECT * FROM Players WHERE Player = {id}
    """).fetchall()
    
    
def SELECT(table):
    return cursor.execute(f"""
        SELECT * FROM {table}
    """).fetchall()
    
    
    
def INSERT_INTO(table, tableid, columns, values):
    pk = cursor.execute(f"""
        SELECT MAX({tableid}) FROM {table}
    """).fetchall()[0][0]
    if pk is None: pk = 1
    else: pk+=1
    
    
    str_columns = ""
    
    for column in columns :
        if type(column) == type(""):
            str_columns += f""" "{column}" ,"""
    str_columns = str_columns[:-1]
    
    str_values = ""
    
    for value in values :
        if type(value) == type(""):
            str_values += f""" "{value}" ,"""
        elif type(value) == type(0):
            str_values += f""" {value} ,"""
    str_values = str_values[:-1]
    
    cursor.execute(f"""
         INSERT INTO {table} ("{tableid}" ,{str_columns}) VALUES ({pk} , {str_values})
    """)
    
    connection.commit()
    

def DELETE (table, column , value):
    if type(value) == type(""):
        cursor.execute(f"""
            DELETE FROM {table} WHERE {column} = "{value}"
        """)
    elif type(value) == type(0):
        cursor.execute(f"""
            DELETE FROM {table} WHERE {column} = {value}
        """)
    connection.commit()
    
    
def UPDATE (table, column, value, this_column, to_this):
    if type(to_this) == type(0):
     cursor.execute(f"""
            UPDATE {table} SET {this_column} =  {to_this} WHERE {column} = {value}
        """)
    elif type(to_this) == type(""):
     cursor.execute(f"""
            UPDATE {table} SET {this_column} =  "{to_this}" WHERE {column} = {value}
        """)
    connection.commit()
    
def DROP(table):
    cursor.execute(f"""
        DROP TABLE {table}
    """)
    

def GET (table, column, value):
    if type(value) == type(""):
        value = f"""  "{value}"  """

    return cursor.execute(f"""
        SELECT * FROM {table} WHERE {column} = {value}
    """).fetchall()[0]
    
# UPDATE("Items", "ItemId", 7, "Title", "Katana")
# DROP("Inventories")