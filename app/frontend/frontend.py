from fastapi import FastAPI

from nicegui import ui


# v = ui.checkbox('visible', value=True)
# with ui.column().bind_visibility_from(v, 'value'):
#     ui.slider(min=1, max=3).bind_value(demo, 'number')
#     ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
#     ui.number().bind_value(demo, 'number')

def init(app: FastAPI) -> None:
    @ui.page('/')
    def show():
        ui.icon('thumb_up')
        ui.markdown('This is **Markdown**.')
        ui.html('This is <strong>HTML</strong>.')
        with ui.row():
            ui.label('CSS').style('color: #888; font-weight: bold')
            ui.label('Tailwind').classes('font-serif')
            ui.label('Quasar').classes('q-ml-xl')
        ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui', new_tab=True)

    ui.run_with(app)
