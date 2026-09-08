import bcrypt


def hash_password(password : str)->str:
    # Takes a plain text password string and turns it into a secure bcrypt hash.
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes =  bcrypt.hashpw(pwd_bytes,salt)

    return hashed_bytes.decode('utf-8')


def verify_password(plain_password: str,hashed_password: str):
    # compare a plain text password against a stored hash to see if they match 
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    # securely verify they match (handles salt automatically)
    return bcrypt.checkpw(pwd_bytes,hashed_bytes)
