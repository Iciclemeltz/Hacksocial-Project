import pandas as pd
import plotly.graph_objects as go
import numpy as np
import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.express as px

# Read data from CSV files
df = pd.read_csv(r'Datasets\electricity_data.csv')
df = df[1110:]  # Exclude the first 1110 rows
df.reset_index(drop=True, inplace=True)
df.index = pd.to_datetime(df['Date'])

df2 = pd.read_csv(r'Datasets\electrical_appliance_consumption.csv')
df2 = df2[df2['year'] == 2021]
df2.reset_index(drop=True, inplace=True)

df3 = pd.read_csv(r'Datasets\electrical_forecast.csv')

df4 = pd.read_csv(r'Datasets\electricity_appliance_wise_data.csv')
df4['Date'] = pd.to_datetime(df4['Date'])
df4 = df4[df4['Date'].dt.year == 2021]
df4.reset_index(drop=True, inplace=True)

app = dash.Dash(__name__)
app.title = 'Electra.AI'

# Define dropdown options
party_data = [
    {'label': 'Time-Series Plot', 'value': 'Time-Series Plot'},
    {'label': 'Appliance-wise Consumption', 'value': 'Appliance-wise Consumption'},
    {'label': 'Electricity Consumption Forecast', 'value': 'Electricity Consumption Forecast'},
    {'label': 'Faulty Devices', 'value': 'Faulty Devices'}
]

# Define the app layout
app.layout = html.Div(children=[
    html.Div(className='row', children=[
        html.Div(className='four columns div-user-controls', children=[
            html.H2('Electra.AI Dashboard', style={'font-family': 'Trebuchet MS'}),
            html.Div(className='div-for-dropdown', children=[
                dcc.Dropdown(
                    id='stockselector',
                    options=party_data,
                    value=['Time-Series Plot'],
                    style={'backgroundColor': '#1E1E1E'},
                    placeholder="Select an Option"
                )
            ], style={'color': '#1E1E1E'})
        ]),
        html.Div(className='eight columns div-for-charts bg-grey', children=[
            dcc.Graph(id='timeseries', config={'displayModeBar': False})
        ])
    ])
])

@app.callback(Output('timeseries', 'figure'), [Input('stockselector', 'value')])
def update_timeseries(selected_dropdown_value):
    if selected_dropdown_value == 'Electricity Consumption Forecast':
        # Prepare data for the forecast plot
        df_sub = df3
        df_anoms = df_sub[df_sub['MAE'] >= 15]
        df_anoms.reset_index(drop=True, inplace=True)

        # Create the figure object
        fig = go.Figure()

        # Add traces for actual consumption and predicted consumption
        fig.add_trace(go.Scatter(x=df_sub['Date'], y=df_sub['Total_Consumption'], mode='lines',
                                 name='Actual Consumption', line_color="#19E2C5"))
        fig.add_trace(go.Scatter(x=df_sub['Date'], y=df_sub['Predicted_Consumption'], mode='lines',
                                 name='Predicted Consumption', line_color="#C6810B"))
        fig.add_trace(go.Scatter(x=df_anoms['Date'], y=df_anoms['Total_Consumption'], mode='markers',
                                 name='Excess Consumption'))

        # Update trace and layout properties
        fig.update_traces(marker=dict(size=5, line=dict(width=5, color='#C60B0
