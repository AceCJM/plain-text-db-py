import cryptography,sys

import cryptography.fernet

token = cryptography.fernet.Fernet.generate_key()

with open(f"{sys.argv[1]}.key","wb") as filekey:
    filekey.write(token)