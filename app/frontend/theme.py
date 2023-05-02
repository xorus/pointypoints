from contextlib import contextmanager

from nicegui import ui
from starlette.requests import Request

from .session import get_session_info

smol = 'gap: 0.3rem'
semi_transparent = 'opacity: 0.5'

@contextmanager
def frame(nav_title: str, request: Request):
    ui.colors(primary="#481258")
    with ui.header().classes('justify-between text-white'):
        with ui.row().style(smol):
            ui.label('Xorus\' Twitch Point Logger').classes('font-bold')
            ui.label('/').style(semi_transparent)
            ui.label(nav_title)
        with ui.row().style(smol):
            user = get_session_info(request)
            if user is not None:
                ui.link('Logout', '/logout').classes(replace='text-white')
                ui.label('/').style(semi_transparent)
                with ui.row().style(smol):
                    ui.label(f'{user.display_name}')
                    ui.avatar(f'img:{user.profile_image_url}', rounded=True).classes(
                        'rounded-full'
                    ).style('width: auto; height: auto;')
            else:
                ui.link('Login (via Twitch)', '/login').classes(replace='text-white')
    with ui.row().classes('container mx-auto'):
        yield
