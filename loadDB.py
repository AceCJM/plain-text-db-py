import sys

try:
    with open(f"{sys.argv[1]}.txt","r") as FILE:
        dbStr = FILE.read()
except:
    print("db not found")

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