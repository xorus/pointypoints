from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
# import plotly.graph_objects as go
from fastapi import FastAPI, Depends, HTTPException
from nicegui import ui
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.db.database import get_db
from app.db.point_value import get_unique_channels, get_newest_entry, get_points_from_to
from app.frontend import theme
from app.frontend.session import get_session_user


def init(app: FastAPI) -> None:
    @ui.page('/points')
    def show(request: Request, db: Session = Depends(get_db)):
        """show the connected user's current channel"""
        with theme.frame('Home', request):
            user = get_session_user(request, db)
            if user is None:
                raise HTTPException(status_code=401)

            ui.label("Channel list:")

            channel_list = get_unique_channels(user.id, db)
            for channel in channel_list:
                with ui.card():
                    ui.link(channel, f'/points/{channel}').classes(replace='text-white font-bold underline')

            if len(channel_list) == 0:
                ui.label("No channels")

    @ui.page('/points/{channel}')
    def show(request: Request, channel: str, db: Session = Depends(get_db)):
        """show the connected user's current channel"""
        with theme.frame('Home', request):
            user = get_session_user(request, db)
            if user is None:
                raise HTTPException(status_code=401)

            newest_entry = get_newest_entry(user.id, channel, db)

            if newest_entry is None:
                raise HTTPException(status_code=404)

            # with ui.element('div'):
            with ui.row():
                ui.link('<- back', '/points').classes(replace='text-white font-bold underline')
                ui.label(f'Channel: {channel}')
                ui.label(f'Newest entry date: {newest_entry.date}')

            # date: now - 12 hours
            date_start = datetime.now() - timedelta(days=20)
            date_end = datetime.now()

            points = get_points_from_to(user.id, channel, date_start, date_end, db)
            df = pd.DataFrame(points, columns=['value', 'date'])

            # fig = go.Figure(go.Line(x=df['date'], y=df['value']))
            fig = px.line(df, x="date", y="value", title='Channel points over time', template='plotly_dark')
            ui.plotly(fig).classes('w-full').style('min-height: 80vh')

            # with ui.element('div'):
            #     print(newest_entry)
            #     ui.label(f'user={channel}')
            #     ui.label(f'channel={newest_entry.channel_name}')
            #     ui.label(f'channel={newest_entry.date}')

            # fig.show()
            # fig = go.Figure(go.Scatter(x=[1, 2, 3, 4], y=[1, 2, 3, 2.5]))
            # fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            # ui.run()
