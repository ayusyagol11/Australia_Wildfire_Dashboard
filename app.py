import pandas as pd
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

# Initialize the Dash application. Dash is a framework that allows us to build web-based analytical apps in Python.
# '__name__' tells Flask (which Dash is built on) where to look for assets.
# We apply the 'DARKLY' Bootstap theme here to ensure responsive scaling and native dark-mode styling.
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Set the title of the web page (what shows up in the browser tab)
app.title = "Australia Wildfire Dashboard"

# Expose the underlying Flask server variable. This is needed if you want to deploy the app to the internet (like on Render or Heroku) using a production server like Gunicorn.
server = app.server

# -----------------------------------------------------------------------------------------
# STEP 1: DATA INGESTION & PREPARATION
# -----------------------------------------------------------------------------------------

# Read the CSV dataset into a Pandas DataFrame. A DataFrame is like a powerful Excel spreadsheet inside Python.
df = pd.read_csv('Historical_Wildfires.csv')

# Convert the raw 'Date' strings into actual Python Datetime objects.
# We pass format='mixed' to tell Pandas to use an optimized parser, which is much faster than letting it guess row entirely from scratch.
dates = pd.to_datetime(df['Date'], format='mixed')

# Extract human-readable month names (e.g., 'January') and the year from the Datetime objects
df['Month'] = dates.dt.month_name()
df['Year'] = dates.dt.year

# Create a dictionary to map the shortened state abbreviations into full state names for a better user experience
state_map = {
    'NSW': 'New South Wales',
    'VI': 'Victoria',
    'QL': 'Queensland',
    'SA': 'South Australia',
    'WA': 'Western Australia',
    'TA': 'Tasmania',
    'NT': 'Northern Territory'
}
# Apply the dictionary replacement to the 'Region' column
df['Region'] = df['Region'].replace(state_map)

# PERFORMANCE OPTIMIZATION: 
# Instead of doing heavy math every time the user clicks a button, we calculate the averages for our charts right now when the app starts.
# We group by Region, Year, and Month, and take the mean (average) of the values we care about.
global_pie_data = df.groupby(['Region', 'Year', 'Month'])['Estimated_fire_area'].mean().reset_index()
global_bar_data = df.groupby(['Region', 'Year', 'Month'])['Count'].mean().reset_index()
global_line_data = df.groupby(['Region', 'Year', 'Month'])['Mean_estimated_fire_brightness'].mean().reset_index()

# Get a sorted list of all unique years and regions to populate our dropdown menus later
years = sorted(df['Year'].unique())
regions = df['Region'].unique()

# -----------------------------------------------------------------------------------------
# STEP 2: FRONTEND LAYOUT (USER INTERFACE)
# -----------------------------------------------------------------------------------------

# Define the HTML structure of our dashboard inside a responsive DBC Container
app.layout = dbc.Container([
    
    # Main Dashboard Header Row
    dbc.Row(
        dbc.Col(html.H1("Australia Wildfire Dashboard", className="text-center my-4"), width=12)
    ),

    # The top control panel containing our Dropdown filters and High-Level KPIs
    dbc.Row([
        # Filters Column
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Filter Dashboard", className="card-title"),
                    html.Label("Select Region:"),
                    dcc.Dropdown(
                        id='region',
                        options=[{'label': r, 'value': r} for r in regions],
                        value='New South Wales',
                        className='mb-3 text-dark'
                    ),
                    html.Label("Select Year:"),
                    dcc.Dropdown(
                        id='year',
                        options=[{'label': y, 'value': y} for y in years],
                        value=years[0],
                        className='text-dark'
                    )
                ])
            ], className="mb-4 h-100 shadow-sm")
        ], md=4), # Takes up 4/12 columns on medium screens

        # KPI Metric Cards Column
        dbc.Col([
            dbc.Row([
                # KPI Card 1: Total Estimated Area Burnt
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Total Area Burnt", className="card-title text-warning"),
                            html.H2(id="kpi-area", className="card-text fw-bold text-white")
                        ])
                    ], className="mb-4 h-100 shadow-sm border-warning"), width=6
                ),
                # KPI Card 2: Total Fire Hotspots (Pixels)
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Total Fire Hotspots", className="card-title text-danger"),
                            html.H2(id="kpi-pixels", className="card-text fw-bold text-white")
                        ])
                    ], className="mb-4 h-100 shadow-sm border-danger"), width=6
                )
            ], className="h-100")
        ], md=8), # Takes up 8/12 columns on medium screens
    ], className="mb-4"),

    # The Grid containing our four Plotly graphs.
    # We wrap them in dcc.Loading components so users see a spinning circle during any cold starts.
    dcc.Loading(
        type="circle",
        color="#ffc107",
        children=dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id='plot1'), className="mb-4 shadow-sm"), md=6),
            dbc.Col(dbc.Card(dcc.Graph(id='plot2'), className="mb-4 shadow-sm"), md=6),
        ])
    ),

    dcc.Loading(
        type="circle", 
        color="#ffc107",
        children=dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id='plot3'), className="mb-4 shadow-sm"), md=6),
            dbc.Col(dbc.Card(dcc.Graph(id='plot4'), className="mb-4 shadow-sm"), md=6),
        ])
    ),

    # Simple footer
    dbc.Row(
        dbc.Col(html.Footer("Created by Aayush Yagol 2025", className="text-center text-muted my-4"), width=12)
    )

], fluid=True, className="p-4")  # fluid=True makes it expand to fill the window securely


# -----------------------------------------------------------------------------------------
# STEP 3: BACKEND LOGIC (INTERACTIVITY)
# -----------------------------------------------------------------------------------------

# The @app.callback decorator acts as the bridge between the Website and our Python code.
# It says: Whenever an 'Input' property changes (like the value of the dropdowns),
# run the function below, and spit the results into the 'Output' properties (the 'figure' attributes of our graphs).
@app.callback(
    [Output('kpi-area', 'children'),
     Output('kpi-pixels', 'children'),
     Output('plot1', 'figure'),
     Output('plot2', 'figure'),
     Output('plot3', 'figure'),
     Output('plot4', 'figure')],
    [Input('region', 'value'),
     Input('year', 'value')]
)
def update_graphs(region, year):
    # Filter the raw dataframe to match the user's selected Region and Year. 
    # We use this raw data entirely for the Scatter plot and KPIs.
    dff = df[(df['Region'] == region) & (df['Year'] == year)]

    # Calculate Top-Level KPI Metric Card strings
    total_area = dff['Estimated_fire_area'].sum()
    total_pixels = dff['Count'].sum()
    kpi_area_str = f"{total_area:,.2f} ha"
    kpi_pixels_str = f"{int(total_pixels):,}"

    # 1. Pie Chart: Avg Fire Area by Month
    pie_data = global_pie_data[(global_pie_data['Region'] == region) & (global_pie_data['Year'] == year)]
    fig1 = px.pie(pie_data, names='Month', values='Estimated_fire_area',
                  title=f"{region}: Avg Fire Area by Month ({year})",
                  color_discrete_sequence=px.colors.sequential.YlOrRd) # Updated to intuitive YlOrRd
    fig1.update_traces(hovertemplate="<b>%{label}</b><br>Average Area Burnt: %{value:.2f} hectares<extra></extra>")

    # 2. Bar Chart: Pixel Count by Month
    bar_data = global_bar_data[(global_bar_data['Region'] == region) & (global_bar_data['Year'] == year)]
    fig2 = px.bar(bar_data, x='Month', y='Count',
                  title=f"{region}: Avg Pixel Count by Month ({year})",
                  color='Count', color_continuous_scale='YlOrRd')
    fig2.update_traces(hovertemplate="In <b>%{x}</b>, there was an average of <b>%{y:.1f}</b> detected fire hotspot pixels.<extra></extra>")

    # 3. Line Chart: Track Fire Brightness over the months
    line_data = global_line_data[(global_line_data['Region'] == region) & (global_line_data['Year'] == year)]
    fig3 = px.line(line_data, x='Month', y='Mean_estimated_fire_brightness',
                   title=f"{region}: Fire Brightness Trend ({year})<br><i>(Unweighted satellite detection averages)</i>", markers=True)
    fig3.update_traces(hovertemplate="<b>%{x}</b><br>Mean Brightness: %{y:.1f} Kelvin<extra></extra>")

    # 4. Bubble Scatter Plot: Compare Radiative Power vs Brightness
    fig4 = px.scatter(dff, x='Mean_estimated_fire_brightness', y='Mean_estimated_fire_radiative_power',
                      title=f"{region}: Radiative Power vs Brightness ({year})<br><i>(Highlights potential outliers per hot spot)</i>",
                      color='Estimated_fire_area', size='Count',
                      color_continuous_scale='YlOrRd')
    fig4.update_traces(hovertemplate="<b>Brightness:</b> %{x:.1f} K<br><b>Radiative Power:</b> %{y:.1f} MW<br><b>Area:</b> %{marker.color:.1f} ha<br><b>Pixels:</b> %{marker.size}<extra></extra>")

    # Iterate through all four generated charts and apply a dark-mode theme
    # This edits the layout dictionaries to match the aesthetic of the external CSS file and DBC Darkly theme.
    for fig in [fig1, fig2, fig3, fig4]:
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", # Transparent background sets cleanly over the bootstrap cards
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="'Inter', 'Segoe UI', sans-serif", size=14),
            title_font=dict(size=18, family="'Inter', 'Segoe UI', sans-serif", color='white')
        )

    # Return exactly six objects, mapping to our two KPI card outputs and four graph outputs respectively.
    # Note: Returning them as a tuple (a, b, fig1...) is required in Dash to prevent backend unpacking errors.
    return (kpi_area_str, kpi_pixels_str, fig1, fig2, fig3, fig4)

# -----------------------------------------------------------------------------------------
# STEP 4: RUN SERVER
# -----------------------------------------------------------------------------------------

# The standard Python entry point. If we are running this script directly, start the local development server.
if __name__ == '__main__':
    app.run(debug=True)
