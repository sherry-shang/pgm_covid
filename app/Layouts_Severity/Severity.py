from app_whole import app
from Layouts_Severity import SidePanel, tab1, tab2
#import navbar
import dash_html_components as html
from dash.dependencies import Output, Input

#dash.register_page(__name__, name='page 2')
#from database import transforms
layout = html.Div([
                         SidePanel.layout
                   ])

@app.callback(Output("tabs-content1", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return tab1.layout
    elif at == "tab-2":
        return tab2.layout


if __name__ == '__main__':
    app.run_server(debug = True)