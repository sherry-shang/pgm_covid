#import dash_core_components as dcc
#import dash_html_components as html
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app_whole import app
from Layouts_LongCOVID import Long_COVID
from Layouts_Severity import Severity

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Long_COVID", href="/Long COVID"),
        dbc.DropdownMenuItem("Severity", href="/Severity"),

    ],
    nav = True,
    in_navbar = True,
    label = "Choose a network:",
)
'''
toast = html.Div(
    [
        dbc.Button(
            "README",
            id="positioned-toast-toggle",
            #color="primary",
            n_clicks=0,
        ),
        dbc.Modal(
            [dbc.ModalBody([html.H6('This is an interactive visualization tool for RAMEN identifies effective indicators for severe COVID and Long COVID patients.'),html.H6("You could use the 'Choose a network:' dropdown on the navbar to visualize the Severity network or the Long_COVID network."),
             html.H6("For each network, there is an offcanvas. You could open and close it."),
             html.H6("Through this offcanvas, you could see the basic statistics and customize the network. Also, you may select a clinical variable and the visualizaton toll will highlight the shortest path from the clincal variable node to Severity/Long_COVID node on the network."),
             html.H6("If you click the Heatmap tab, you may explore the correlation relationship between every two variables. For example: the number on heatmap when Asthma? is Yes and Red eye(Conjunctivits)? is No means a COVID patient has a probability of 0.1 to have asthma and do not have red eye."),
             html.H6("You could also look at the common differential expression genes with the highest fold change between clinical variables and Severity/Long_COVID.")]),
            dbc.ModalFooter(dbc.Button("Close",id='close',className='ms-auto',n_clicks=0)),],
            id="positioned-toast",
            is_open=False,
            #header="README",
            #is_open=False,
            #dismissable=True,
            #icon="primary",
            # top: 66 positions the toast below the navbar
            #style={"position": "fixed", "top": 66, "right": 10, "width": 450},
        ),
    ]
)
'''
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("COVID-19 DASH", className="ml-2")),
                    ],
                    align="center",
                    #no_gutters=True,
                    className="g-0",
                ),
                #href="/Long COVID",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown,dbc.Button(
            "README",
            id="positioned-toast-toggle",
            #color="primary",
            n_clicks=0,
            href='https://yellow-bearberry-007.notion.site/README-7339cf50dd20499a909ce3f25a14a336',
            target="_blank"
        ),], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)
'''
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)
'''
# embedding the navigation bar

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/Severity':
        return Severity.layout
    else:
        return Long_COVID.layout
'''
@app.callback(
    Output("positioned-toast", "is_open"),
    [Input("positioned-toast-toggle", "n_clicks"),Input('close','n_clicks')],
    [State("positioned-toast", "is_open")]
)
def open_toast(n1,n2,is_open):
    if n1 or n2:
        return not is_open
    return is_open
'''
if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(debug=True, host='0.0.0.0')