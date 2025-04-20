import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import json

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Australia Wildfire Dashboard"

# Load dataset
df = pd.read_csv('Historical_Wildfires.csv')
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Map abbreviations to full state names
state_map = {
    'NSW': 'New South Wales',
    'VI': 'Victoria',
    'QL': 'Queensland',
    'SA': 'South Australia',
    'WA': 'Western Australia',
    'TA': 'Tasmania',
    'NT': 'Northern Territory'
}

df['Region'] = df['Region'].replace(state_map)

# Unique years for dropdown
years = sorted(df['Year'].unique())
regions = df['Region'].unique()

# App layout
app.layout = html.Div([
    html.H1("Australia Wildfire Dashboard", className="header-title"),

    html.Div([
        html.Div([
            html.H2("Select Region"),
            dcc.Dropdown(
                id='region',
                options=[{'label': r, 'value': r} for r in regions],
                value='New South Wales',
                className='dropdown',
                style={'color': '#000'}
            )
        ], className="control-container"),

        html.Div([
            html.H2("Select Year"),
            dcc.Dropdown(
                id='year',
                options=[{'label': y, 'value': y} for y in years],
                value=years[0],
                className='dropdown',
                style={'color': '#000'}
            )
        ], className="control-container")
    ], className="top-controls"),

    html.Div([
        html.Div([dcc.Graph(id='plot1')], className="graph-container"),
        html.Div([dcc.Graph(id='plot2')], className="graph-container"),
        html.Div([dcc.Graph(id='plot3')], className="graph-container"),
        html.Div([dcc.Graph(id='plot4')], className="graph-container"),
    ], className="graph-grid"),

    html.Footer("Created by Aayush Yagol 2025", className="footer")
], className='dark-theme')

# Update the plots
@app.callback(
    [Output('plot1', 'figure'),
     Output('plot2', 'figure'),
     Output('plot3', 'figure'),
     Output('plot4', 'figure')],
    [Input('region', 'value'),
     Input('year', 'value')]
)
def update_graphs(region, year):
    dff = df[(df['Region'] == region) & (df['Year'] == year)]

    pie_data = dff.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(pie_data, names='Month', values='Estimated_fire_area',
                  title=f"{region}: Avg Fire Area by Month ({year})",
                  color_discrete_sequence=px.colors.sequential.Reds)

    bar_data = dff.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(bar_data, x='Month', y='Count',
                  title=f"{region}: Avg Pixel Count by Month ({year})",
                  color='Count', color_continuous_scale='Inferno')

    line_data = dff.groupby('Month')['Mean_estimated_fire_brightness'].mean().reset_index()
    fig3 = px.line(line_data, x='Month', y='Mean_estimated_fire_brightness',
                   title=f"{region}: Fire Brightness Trend ({year})", markers=True)

    fig4 = px.scatter(dff, x='Mean_estimated_fire_brightness', y='Mean_estimated_fire_radiative_power',
                      title=f"{region}: Radiative Power vs Brightness ({year})",
                      color='Estimated_fire_area', size='Count')

    for fig in [fig1, fig2, fig3, fig4]:
        fig.update_layout(
            paper_bgcolor="#1e1e1e",
            plot_bgcolor="#1e1e1e",
            font=dict(color="white", family="'Inter', 'Segoe UI', sans-serif", size=14),
            title_font=dict(size=20, family="'Inter', 'Segoe UI', sans-serif", color='white')
        )

    return fig1, fig2, fig3, fig4

if __name__ == '__main__':
    app.run_server(debug=True)