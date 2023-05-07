from fastapi import FastAPI, Depends
from nicegui import ui
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import RedirectResponse
from twitchAPI import Twitch

from app.db.database import get_db
from app.frontend import theme, points
from app.frontend.session import session_clear, get_session_user
from app.frontend.session import set_session_from_user
from app.lib.twitch import twitch_oauth2_redirect, twitch_oauth2_fetch_token
from app.lib.auth import user_from_login
from app.settings import settings


# v = ui.checkbox('visible', value=True)
# with ui.column().bind_visibility_from(v, 'value'):
#     ui.slider(min=1, max=3).bind_value(demo, 'number')
#     ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
#     ui.number().bind_value(demo, 'number')


def init(app: FastAPI) -> None:
    @ui.page('/')
    def show(request: Request, db: Session = Depends(get_db)):
        with theme.frame('Home', request):
            if (user := get_session_user(request, db)) is not None:
                with ui.row():
                    with ui.card().style('max-width: 300px'):
                        ui.label("You are logged in!")
                        ui.link('Go to /points', '/points').classes(replace='text-white font-bold underline')

            with ui.row():
                with ui.card().style('max-width: 300px'):
                    ui.link('Install userscript', '/userscript/twitch-channel-points-logger.user.js').classes(
                        replace='text-white font-bold underline')
                    ui.markdown('You need an userscript extension such as TamperMonkey ('
                                '[Firefox](https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/), '
                                '[Chrome](https://chrome.google.com/webstore/detail/tampermonkey'
                                '/dhdgffkkebhmkfjojejmpbldmpobfkfo?hl=en))'
                                ' to use this.')
                with ui.card().style('max-width: 300px'):
                    ui.link('Source code', 'https://github.com/xorus/pointypoints', new_tab=True).classes(
                        replace='text-white font-bold underline')

    @app.get('/login')
    def login():
        url, state = twitch_oauth2_redirect('/auth/twitch')
        return RedirectResponse(url=url, status_code=302)

    @app.get('/logout')
    def logout(request: Request):
        session_clear(request)
        return RedirectResponse('/')

    @app.get('/auth/twitch')
    async def auth_twitch(request: Request, code: str, db: Session = Depends(get_db)):
        result = await twitch_oauth2_fetch_token(code)
        access_token = result.get('access_token')
        if access_token is None:
            with theme.frame('Home', request):
                ui.label('Received an invalid response from Twitch, something went wrong :(.')
                ui.link('Retry login with Twitch', '/login')
                return

        user_twitch = await Twitch(settings.twitch_client_id, authenticate_app=False)
        user_twitch.auto_refresh_auth = False
        await user_twitch.set_user_authentication(access_token, [], validate=False)

        if (me := (await user_twitch.get_users().__anext__())) is None:
            with theme.frame('Home', request):
                ui.label('We could not get an authorization token from Twitch.')
                ui.link('Retry login with Twitch', '/login')
                return

        user = user_from_login(me.id, me.display_name, me.profile_image_url, db)
        request.session.clear()
        set_session_from_user(request, user.id, me.display_name, me.profile_image_url)
        return RedirectResponse('/', status_code=302)

    ui.run_with(app, dark=True)
    points.init(app)
