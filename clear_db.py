import sqlite3

def print_DB():
    for row in cursor.execute('select * from leaderboard;'):
        print(row)


connection = sqlite3.connect("./history/leaderboards.db")
cursor = connection.cursor()

print("Current Values")

print_DB()

print("Cleaning DB")

cursor.execute('delete from leaderboard where id is not 0;')

print("New Values")

print_DB()

connection.commit()



import os
 
dir = 'test/'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))



