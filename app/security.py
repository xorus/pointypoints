from authlib.integrations.httpx_client import AsyncOAuth2Client
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse, HTMLResponse
from twitchAPI import Twitch

from app.db.database import get_db
from app.db.user import create_user_from_twitch, get_user_by_twitch_id, update_existing_token_and_info
from app.lib.auth import create_access_token, RequireUserToken
from app.settings import settings


def twitch_client():
    return AsyncOAuth2Client(
        settings.twitch_client_id,
        settings.twitch_client_secret,
        scope='',
        redirect_uri=f'{settings.base_url}/auth/twitch',
        token_endpoint_auth_method='client_secret_post'
    )


def init(app: FastAPI) -> None:
    @app.get('/me')
    async def me(current_user: RequireUserToken):
        return current_user

    @app.get('/login/twitch')
    async def login_twitch():
        url, state = twitch_client().create_authorization_url('https://id.twitch.tv/oauth2/authorize')
        return RedirectResponse(url=url, status_code=302)

    @app.get('/auth/twitch')
    async def auth_twitch(code, db: Session = Depends(get_db)):
        result = await twitch_client().fetch_token(
            f'https://id.twitch.tv/oauth2/token',
            grant_type='authorization_code',
            code=code)

        access_token = result.get('access_token')
        if access_token is None:
            print("invalid auth")
            return HTMLResponse("""
            <html>
                <head>
                    <title>Some HTML in here</title>
                </head>
                <body>
                    <a href="/login/twitch">Login with Twitch</a>
                </body>
            </html>
            """, status_code=401)
            # raise ValueError('Access token is not present in the response')

        print(f"valid auth {access_token}")
        user_twitch = await Twitch(settings.twitch_client_id, authenticate_app=False)
        user_twitch.auto_refresh_auth = False
        await user_twitch.set_user_authentication(access_token, [], validate=False)

        if (me := (await user_twitch.get_users().__anext__())) is None:
            return HTMLResponse("""
            <html>
                <head>
                    <title>Some HTML in here</title>
                </head>
                <body>
                    <a href="/login/twitch">Login with Twitch (2)</a>
                </body>
            </html>
                """, status_code=401)

        existing = get_user_by_twitch_id(me.id, db)
        if existing is not None:
            existing.profile_image_url = me.profile_image_url
            existing.display_name = me.display_name
            user = update_existing_token_and_info(existing, db)
        else:
            user = create_user_from_twitch(me.id, me.display_name, me.profile_image_url, db)

        return create_access_token(user.id, user.display_name)
