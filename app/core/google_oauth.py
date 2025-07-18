from authlib.integrations.starlette_client import OAuth 
from app.core.config import config as settings
oauth = OAuth()

oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    jwks_uri = "https://www.googleapis.com/oauth2/v3/certs",
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'consent',  
    }
)
