import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import json

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Australia Wildfire Dashboard"
server = app.server  # Expose the server variable for Gunicorn on Render

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

# Unique years and regions for dropdowns
years = sorted(df['Year'].unique())
regions = df['Region'].unique()

# Layout for the Dash app
app.layout = html.Div([
    html.H1("Australia Wildfire Dashboard", className="header-title"),

    # Region and Year selection dropdowns
    html.Div([
        html.Div([
            html.H2("Select Region"),
            dcc.Dropdown(
                id='region',
                options=[{'label': r, 'value': r} for r in regions],
                value='New South Wales',  # Default value
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

    # Chart grid
    html.Div([
        html.Div([dcc.Graph(id='plot1')], className="graph-container"),
        html.Div([dcc.Graph(id='plot2')], className="graph-container"),
        html.Div([dcc.Graph(id='plot3')], className="graph-container"),
        html.Div([dcc.Graph(id='plot4')], className="graph-container"),
    ], className="graph-grid"),

    # Footer
    html.Footer("Created by Aayush Yagol 2025", className="footer")

], className='dark-theme')  # Apply dark theme to root div


# Callback function to update all four charts based on region and year
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

    # Pie chart: Avg Fire Area by Month
    pie_data = dff.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(pie_data, names='Month', values='Estimated_fire_area',
                  title=f"{region}: Avg Fire Area by Month ({year})",
                  color_discrete_sequence=px.colors.sequential.Reds)

    # Bar chart: Avg Pixel Count by Month
    bar_data = dff.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(bar_data, x='Month', y='Count',
                  title=f"{region}: Avg Pixel Count by Month ({year})",
                  color='Count', color_continuous_scale='Inferno')

    # Line chart: Fire Brightness Trend
    line_data = dff.groupby('Month')['Mean_estimated_fire_brightness'].mean().reset_index()
    fig3 = px.line(line_data, x='Month', y='Mean_estimated_fire_brightness',
                   title=f"{region}: Fire Brightness Trend ({year})", markers=True)

    # Scatter plot: Radiative Power vs Brightness
    fig4 = px.scatter(dff, x='Mean_estimated_fire_brightness', y='Mean_estimated_fire_radiative_power',
                      title=f"{region}: Radiative Power vs Brightness ({year})",
                      color='Estimated_fire_area', size='Count')

    # Apply dark mode styling and consistent font to all figures
    for fig in [fig1, fig2, fig3, fig4]:
        fig.update_layout(
            paper_bgcolor="#1e1e1e",
            plot_bgcolor="#1e1e1e",
            font=dict(color="white", family="'Inter', 'Segoe UI', sans-serif", size=14),
            title_font=dict(size=22, family="'Inter', 'Segoe UI', sans-serif", color='white')
        )

    return fig1, fig2, fig3, fig4

# Run the Dash server
if __name__ == '__main__':
    app.run_server(debug=True)
