import sys,os

# Global Variables:
templateDB = "\ntempGroup\nTemp,bool,false,true" # Default DB contents
args = ["-c","-a","-r","-l","-ddb","-e","-dt","-dd"]



############################################################
#               DB FILE MANAGEMENT FUNCTIONS              #
############################################################
def deleteDB(fname):
    os.remove(f"{fname}.txt")

def createDB(dbName): # Creaates default DB & writes to file
    db = [dbName,templateDB]
    dbStr = "".join(db)
    with open(f"{dbName}.txt", "w") as FILE:
        FILE.write(dbStr)

def writeFile(fname,data): # Writes DB to file
    dbList = []
    for i in data: # Simplifies DB to lists
        dbList.append(i)
        if isinstance(data[i],str):
            dbList.append(data[i])
        elif isinstance(data[i],dict):
            for j in data[i]:
                dbList.append([j]+data[i][j])
    del dbList[0]

    dbSimpList = []
    for i in dbList: # Simplifies DB to one list
        if isinstance(i,list):
            dbSimpList.append(",".join(i))
        else:
            dbSimpList.append(i)
    dbStr = "\n".join(dbSimpList)

    try:
        with open(f"{fname}.txt", "w") as FILE: # Writes simplified DB to file
            FILE.write(dbStr)
    except:
        print("ERROR while writting to file\ndb may be corupt\nExiting")
        sys.exit()

def readFile(fname): # Reads data from File
    try:
        with open(f"{fname}.txt", "r") as FILE:
            cont = FILE.read()
        return cont
    except:
        print("ERROR while reading file\ndb MAY be corupt\nExiting")
        sys.exit()

def loadDB(fname): # Splits DB string & Iterates contents to a dictionary
    dbStr = readFile(fname)
    db = {"name": fname}
    group = {}
    names = []
    j = 0
    for i in dbStr.splitlines():
        j += 1
        if "," in i: # Deals with Entry information
            contents = i.split(",")
            name = contents[0]
            del contents[0]
            group[name] = contents

        elif j > 1: # Deals with Entry names
            names.append(i)
            db[names[len(names)-2]] = group
            group = {}

    db[names[len(names)-1]] = group
    return db

def printDB(fname): # Iterates DB and prints contents
    db = loadDB(fname)
    for i in db:
        if isinstance(db[i],dict):
            print("\n ",i)
            for j,k in db[i].items():
                print(j,":",k)
        else:
            print(i)


############################################################
#                DB DATA MANAGMENT FUNCTIONS               #
############################################################

def appendDB(db,group,name,type,imm,data): # Appends/replaces data in DB
    data = [type,imm,data]
    print(data)    
    try:
        db[group][name] = data
    except:
        db[group] = {name:data}
    writeFile(db["name"],db)
    
    return db

def readData(db,group,name):
    return db[group][name]

def changeValue(db,group,name,data):
    if db[group][name][1] == "true":
        return "immutable object"
    db[group][name][2] = data
    writeFile(db["name"],db)

def dataType(db,group,name):
    dtype = db[group][name][0]
    return dtype

def deleteData(db,group,name):
    if db[group][name][2] != "true":
        del db[group][name]
        writeFile(db["name"],db)
        return "success"
    else:
        return "immutable object"

def deleteGroup(db,group):
    del db[group]
    writeFile(db["name"],db)
    return "success"



############################################################
#                       CLI INTERFASE                      #
############################################################

if __name__ == "__main__":
    cli_args = sys.argv[1:]
    if cli_args[0] in args:
        print("MISSING DB NAME")
        exit
    dbName = cli_args[0]
    for i in cli_args:
        if i not in ["-c", "-ddb","-l"] and cli_args.index(i) == 1:
            db = loadDB(dbName)
            group = input("Group Name > ")
            name = input("Entry Name > ")
        if i == "-c":
            createDB(dbName)
        if i == "-l":
            printDB(dbName)
        if i == "-ddb":
            print(deleteDB(dbName))
        if i == "-a":
            data = input("Input Data > ")
            print(appendDB(db,group,data))
        if i == "-r":
            print(readData(db,group,name))
        if i == "-e":
            data = input("Input Data > ")
            print(changeValue(db,group,name,data))
        if i == "-dt":
            print(dataType(db,group,name))
