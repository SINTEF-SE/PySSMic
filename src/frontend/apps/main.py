import dash_core_components as dcc
import dash_html_components as html

# TODO: Add/remove users from the neighbourhood
# TODO: Number of days simulated
# TODO: Configure simulated weather
# TODO: Review the use of green energy
# TODO: Specify which optimization algorithm to be used in simulation

layout = html.Div(children=[
    html.H1(children="CoSSMic Simulator"),

    dcc.Link('Go to Create Simulation', href='/apps/create_sim')
])
