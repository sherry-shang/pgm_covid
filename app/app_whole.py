import dash
from dash import html, dcc, Dash
import dash_bootstrap_components as dbc
#external_stylesheets = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
app = Dash(__name__,  external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])


server = app.server
app.config.suppress_callback_exceptions = True