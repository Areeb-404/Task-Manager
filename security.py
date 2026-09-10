from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
import os

# Securely read a secret key from the virtual environment, or fall back to a development default
SECRET_KEY = os.getenv("JWT_SECRET","superrrr-secret-change-in-dev")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

def create_access_token(data:dict)->str:
    # generate a signed token containing user identity and expiration

    # creating a copy of the payload data
    payload = data.copy()

    # calculating the expiration time (30 minutes from now)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # adding the 'exp' claim to the payload (crucial for jwt expiration check)
    payload.update({"exp":expire})

    # sign the token with our secret key using HS256
    encoded_jwt = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str)->dict | None:
    # Decode and verify a signed JWT token, Return the payload as a dictionary if valid, else return None if invalid/expired
    try:
        # the jwt.decode() function automatically verifies both the signature AND the 'exp' claim expiration time
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        return None
    except jwt.InvalidTokenError:
        print("Invalid Token Or Format")
        return None
