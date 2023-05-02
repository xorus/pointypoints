from fastapi import FastAPI, Depends
from nicegui import ui
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.db.database import get_db
from app.frontend import theme
from app.frontend.session import session_clear, get_session_user
from app.security import use_twitch_login


# v = ui.checkbox('visible', value=True)
# with ui.column().bind_visibility_from(v, 'value'):
#     ui.slider(min=1, max=3).bind_value(demo, 'number')
#     ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
#     ui.number().bind_value(demo, 'number')


def landing_content():
    with ui.card().style('max-width: 300px'):
        ui.link('Install userscript', '/userscript/twitch-channel-points-logger.user.js').classes(
            replace='text-white font-bold underline')
        ui.markdown('You need an userscript extension such as TamperMonkey ('
                    '[Firefox](https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/), '
                    '[Chrome](https://chrome.google.com/webstore/detail/tampermonkey'
                    '/dhdgffkkebhmkfjojejmpbldmpobfkfo?hl=en))'
                    ' to use this.')
    with ui.card():
        ui.link('Source code', 'https://github.com/xorus/pointypoints', new_tab=True).classes(
            replace='text-white font-bold underline')


def init(app: FastAPI) -> None:
    @ui.page('/')
    def show(request: Request, db: Session = Depends(get_db)):
        with theme.frame('Home', request):
            landing_content()

            if (user := get_session_user(request, db)) is not None:
                print(user)

    @app.get('/login')
    def show(request: Request):
        session_clear(request)
        request.session.update({'use_session_login': '1'})
        return use_twitch_login()

    @app.get('/logout')
    def show(request: Request):
        session_clear(request)
        return RedirectResponse('/')

    ui.run_with(app, dark=True)
