import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Load the wildfire dataset
df = pd.read_csv('Historical_Wildfires.csv')

# Extract month and year from the 'Date' column
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Define the layout of the dashboard
app.layout = html.Div(
    children=[
        # Dashboard Title
        html.H1(
            'Australia Wildfire Dashboard',
            style={'textAlign': 'center', 'color': '#2E86C1', 'font-size': '32px', 'font-family': 'Arial, sans-serif', 'margin-bottom': '20px'}
        ),

        # Region and Year Selectors
        html.Div(
            [
                # Region Selection (Radio Items)
                html.Div(
                    [
                        html.H2('Select Region:', style={'margin-right': '2em', 'font-family': 'Arial, sans-serif', 'color': '#34495E'}),
                        dcc.RadioItems(
                            id='region',
                            options=[
                                {"label": "New South Wales", "value": "NSW"},
                                {"label": "Northern Territory", "value": "NT"},
                                {"label": "Queensland", "value": "QL"},
                                {"label": "South Australia", "value": "SA"},
                                {"label": "Tasmania", "value": "TA"},
                                {"label": "Victoria", "value": "VI"},
                                {"label": "Western Australia", "value": "WA"}
                            ],
                            value="NSW",  # Default selection
                            inline=True,
                            style={'font-family': 'Arial, sans-serif'}
                        )
                    ],
                    style={'margin-bottom': '20px'}
                ),

                # Year Selection (Dropdown)
                html.Div(
                    [
                        html.H2('Select Year:', style={'margin-right': '2em', 'font-family': 'Arial, sans-serif', 'color': '#34495E'}),
                        dcc.Dropdown(
                            id='year',
                            options=[{'label': year, 'value': year} for year in df['Year'].unique()],
                            value=2005,  # Default selection
                            style={'width': '50%', 'font-family': 'Arial, sans-serif'}
                        )
                    ],
                    style={'margin-bottom': '20px'}
                )
            ],
            style={'padding': '20px', 'border': '1px solid #D5D8DC', 'border-radius': '10px'}
        ),

        # Graphs Container
        html.Div(
            [
                # Plot 1: Monthly Average Estimated Fire Area (Pie Chart)
                html.Div(
                    [
                        dcc.Graph(id='plot1'),
                        html.P(
                            "This pie chart shows the distribution of the average estimated fire area by month. It helps identify which months had the largest fire areas.",
                            style={'font-family': 'Arial, sans-serif', 'color': '#34495E', 'text-align': 'center'}
                        )
                    ],
                    style={'width': '50%', 'display': 'inline-block'}
                ),

                # Plot 2: Monthly Average Count of Pixels for Presumed Vegetation Fires (Bar Chart)
                html.Div(
                    [
                        dcc.Graph(id='plot2'),
                        html.P(
                            "This bar chart shows the average count of fire pixels by month. It indicates how frequently fires occurred in each month.",
                            style={'font-family': 'Arial, sans-serif', 'color': '#34495E', 'text-align': 'center'}
                        )
                    ],
                    style={'width': '50%', 'display': 'inline-block'}
                ),

                # Plot 3: Mean Fire Brightness Over Time (Line Chart)
                html.Div(
                    [
                        dcc.Graph(id='plot3'),
                        html.P(
                            "This line chart tracks the average fire brightness over time. Higher brightness values indicate more intense fires.",
                            style={'font-family': 'Arial, sans-serif', 'color': '#34495E', 'text-align': 'center'}
                        )
                    ],
                    style={'width': '50%', 'display': 'inline-block'}
                ),

                # Plot 4: Fire Radiative Power vs. Fire Brightness (Scatter Plot)
                html.Div(
                    [
                        dcc.Graph(id='plot4'),
                        html.P(
                            "This scatter plot explores the relationship between fire radiative power and fire brightness. Larger and darker points represent fires with higher area and count.",
                            style={'font-family': 'Arial, sans-serif', 'color': '#34495E', 'text-align': 'center'}
                        )
                    ],
                    style={'width': '50%', 'display': 'inline-block'}
                )
            ],
            style={'margin-top': '20px'}
        )
    ],
    style={'font-family': 'Arial, sans-serif', 'padding': '20px'}
)

# Callback to update the graphs based on user input
@app.callback(
    [Output(component_id='plot1', component_property='figure'),
     Output(component_id='plot2', component_property='figure'),
     Output(component_id='plot3', component_property='figure'),
     Output(component_id='plot4', component_property='figure')],
    [Input(component_id='region', component_property='value'),
     Input(component_id='year', component_property='value')]
)
def update_graphs(input_region, input_year):
    """
    Callback function to update the graphs based on the selected region and year.
    """
    # Filter data for the selected region and year
    region_data = df[df['Region'] == input_region]
    year_data = region_data[region_data['Year'] == input_year]

    # Plot 1: Monthly Average Estimated Fire Area (Pie Chart)
    est_fire_area = year_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(
        est_fire_area,
        values='Estimated_fire_area',
        names='Month',
        title=f'{input_region}: Monthly Average Estimated Fire Area ({input_year})',
        color_discrete_sequence=px.colors.sequential.Blues
    )

    # Plot 2: Monthly Average Count of Pixels for Presumed Vegetation Fires (Bar Chart)
    veg_fire_count = year_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(
        veg_fire_count,
        x='Month',
        y='Count',
        title=f'{input_region}: Average Count of Pixels for Presumed Vegetation Fires ({input_year})',
        color='Count',
        color_continuous_scale='Viridis'
    )

    # Plot 3: Mean Fire Brightness Over Time (Line Chart)
    brightness_over_time = year_data.groupby('Month')['Mean_estimated_fire_brightness'].mean().reset_index()
    fig3 = px.line(
        brightness_over_time,
        x='Month',
        y='Mean_estimated_fire_brightness',
        title=f'{input_region}: Mean Fire Brightness Over Time ({input_year})',
        markers=True
    )

    # Plot 4: Fire Radiative Power vs. Fire Brightness (Scatter Plot)
    fig4 = px.scatter(
        year_data,
        x='Mean_estimated_fire_brightness',
        y='Mean_estimated_fire_radiative_power',
        title=f'{input_region}: Fire Radiative Power vs. Fire Brightness ({input_year})',
        color='Estimated_fire_area',
        size='Count'
    )

    # Return the graphs
    return fig1, fig2, fig3, fig4

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)