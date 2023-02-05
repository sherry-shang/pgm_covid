from app_whole import app
from Layouts_LongCOVID import SidePanel1, tab11, tab12
from dash import html
from dash.dependencies import Output, Input

#dash.register_page(__name__, path='/', name='page 1') # '/' is home page
#from database import transforms
layout = html.Div([
                        SidePanel1.layout
                   ])

@app.callback(Output("tabs-content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return tab11.layout
    elif at == "tab-2":
        return tab12.layout


if __name__ == '__main__':
    app.run_server(debug = True)