from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from twitchAPI import Twitch

from app.db.database import get_db
from app.lib.auth import create_access_token, RequireUserToken
from app.lib.auth import user_from_login
from app.lib.twitch import twitch_oauth2_redirect, twitch_oauth2_fetch_token
from app.settings import settings


def twitch_login_error_html(message: str) -> str:
    """
    display a somewhat user-friendly error even though this is the api because of the pop-up flow.
    """
    return f"""
            <html>
               <head>
                   <title>Xorus' Twitch Point Counter</title>
               </head>
               <body style="background: #121212; color: white; font-family: sans-serif;">
                   <p>{message}</p>
                   <p>Please close this window and try logging in again.</p>
               </body>
           </html>
           """


def init(app: FastAPI) -> None:
    @app.get('/api/me')
    async def get_points(current_user: RequireUserToken):
        return current_user

    @app.get('/api/login/twitch')
    async def login_twitch():
        url, state = twitch_oauth2_redirect('/api/auth/twitch')
        return {"url": url}

    @app.get('/api/auth/twitch')
    async def auth_twitch(code: str, db: Session = Depends(get_db)):
        result = await twitch_oauth2_fetch_token(code)
        access_token = result.get('access_token')
        if access_token is None:
            return HTMLResponse(twitch_login_error_html("Received an invalid response from Twitch, something went "
                                                        "wrong :(."), status_code=401)

        user_twitch = await Twitch(settings.twitch_client_id, authenticate_app=False)
        user_twitch.auto_refresh_auth = False
        await user_twitch.set_user_authentication(access_token, [], validate=False)

        if (me := (await user_twitch.get_users().__anext__())) is None:
            return HTMLResponse(twitch_login_error_html("We could not get an authorization token from Twitch"),
                                status_code=401)

        user = user_from_login(me.id, me.display_name, me.profile_image_url, db)
        access_token = create_access_token(user.id, me.display_name, user.token)
        return {"access_token": access_token}
