from hashlib import sha256

from authlib.integrations.httpx_client import AsyncOAuth2Client
from twitchAPI.twitch import Twitch

from app.settings import settings


# unused for now, but I have plans (tm)
class TwitchInstance:
    api = None

    async def init(self):
        self.api = await Twitch(settings.twitch_client_id, settings.twitch_client_secret)
        # self.api.authenticate_app()


twitch = TwitchInstance()

TWITCH_AUTH_URL = 'https://id.twitch.tv/oauth2/authorize'


def twitch_oauth2(redirect_path: str = '/auth/twitch') -> AsyncOAuth2Client:
    return AsyncOAuth2Client(
        settings.twitch_client_id,
        settings.twitch_client_secret,
        scope='',
        redirect_uri=f'{settings.base_url}{redirect_path}',
        token_endpoint_auth_method='client_secret_post'
    )


def twitch_oauth2_redirect(redirect_path: str = '/auth/twitch') -> (str, str):
    url, state = twitch_oauth2(redirect_path).create_authorization_url('https://id.twitch.tv/oauth2/authorize')
    return url, state


async def twitch_oauth2_fetch_token(code: str) -> dict:
    return await twitch_oauth2().fetch_token(f'https://id.twitch.tv/oauth2/token',
                                             grant_type='authorization_code', code=code)


def hash_twitch_id(twitch_id: str) -> str:
    return sha256(twitch_id.encode('utf-8')).hexdigest()

# auth = UserAuthenticator(twitch, [], force_verify=False)
# token, refreshToken = await auth.authenticate()
