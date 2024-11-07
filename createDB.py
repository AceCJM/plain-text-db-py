import sys

dbName = sys.argv[1]
db = []

db.append(f"{dbName}\ntempGroup")
db.append('\nTemp,bool,false,True')

dbStr = "".join(db)
with open(f"{dbName}.txt", "w") as FILE:
    FILE.write(dbStr)
