import sys, cryptography
import cryptography.fernet

dbName = sys.argv[1]
db = []

with open("filekey.key", "rb") as filekey:
    key = filekey.read()

fernet = cryptography.fernet.Fernet(key)

db.append(f"{dbName}\ntempGroup")
db.append('\nTemp,bool,false,True')

dbStr = "".join(db)
with open(f"{dbName}.txt", "w") as FILE:
    FILE.write(dbStr)

with open(f"{dbName}.txt", "rb") as FILE:
    dbStr = FILE.read()

encrypted = fernet.encrypt(dbStr)

with open(f"{dbName}.txt", "wb") as FILE:
    FILE.write(encrypted)