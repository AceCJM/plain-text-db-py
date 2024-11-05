import sys,cryptography
import cryptography.fernet

with open(f"{sys.argv[1]}.txt","rb") as FILE:
    dbStrEncypt = FILE.read()

with open("filekey.key", "rb") as filekey:
    key = filekey.read()

fernet = cryptography.fernet.Fernet(key)
dbStr = str(fernet.decrypt(dbStrEncypt))

# Splits up imported db string into list for calling
db = []
dbList = dbStr.splitlines()
for i in dbList:
    if "," in i: 
        db.append(i.split(","))
    else: 
        db.append(i)        

# Prints db{name} in terminal line by line
for i in db:
    print(i)
print(db)