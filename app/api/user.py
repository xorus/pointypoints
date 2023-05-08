from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse
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
    return f"""<!DOCTYPE html><html>
               <head>
                   <title>Xorus' Twitch Point Counter</title>
               </head>
               <body style="background: #121212; color: white; font-family: sans-serif;">
                   <p>{message}</p>
                   <p>Please close this window and try logging in again.</p>
                   <a href="/login_userscript" style="color: white">retry</p>
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

    @app.get('/login_userscript')
    async def login_twitch():
        url, state = twitch_oauth2_redirect('/api/auth/twitch')
        return RedirectResponse(url=url, status_code=302)

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
        # return {"access_token": access_token}

        return HTMLResponse(f"""<!DOCTYPE html><html>
                   <head>
                       <title>Xorus' Twitch Point Counter</title>
                   </head>
                   <body style="background: #121212; color: white; font-family: sans-serif; word-wrap: anywhere;">
                       <h1>Logged in as {me.display_name}</h1>
                       <div id="pointy-points-auto-access-token" data-token="{access_token}">
                           <p>Copy this token in the "Auth token" field:</p>
                           <div style="user-select: all;font-family: monospace;border: 1px dashed #777;
                           padding: 10px;margin-top: 10px;">{access_token}</div>
                           <p>This is a bit manual for now but it's a work in progress, sorry!</p>
                           <p>Once done, you can close this window :).</p>
                        </div>
                       <div class="pointy-points-auto-access-token-show" style="display: none;">
                           <p>You're all set!</p>
                           <p>Login process is complete, you can now close this window.</p>
                       </div>
                   </body>
               </html>
               """)
