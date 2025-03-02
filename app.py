import os

from functools import lru_cache
from fastapi import FastAPI, Request, HTTPException, Depends
from authlib.integrations.starlette_client import OAuth
from authlib.jose import jwt, JoseError

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# FastAPI app setup
app = FastAPI()

# OAuth setup for token validation
oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID, 
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=GOOGLE_DISCOVERY_URL,
    client_kwargs={'scope': 'openid email profile'}
)

async def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    return await verify_token(token)

@lru_cache(maxsize=50_000) #todo: switch to expiration based cache
async def verify_token(token: str):
    if token is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        claims = jwt.decode(token, key=oauth.google.client_secret)
        claims.validate()
    except JoseError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return claims

@app.get('/')
async def index():
    return {"message": "Hello World"}

@app.get('/protected')
async def protected_route(user=Depends(get_current_user)):
    return {"message": "This is a protected route", "user": user}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)