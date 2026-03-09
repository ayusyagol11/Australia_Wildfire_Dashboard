import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px

# Initialize the Dash application. Dash is a framework that allows us to build web-based analytical apps in Python.
# '__name__' tells Flask (which Dash is built on) where to look for assets.
app = dash.Dash(__name__)

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

# Define the HTML structure of our dashboard inside app.layout
app.layout = html.Div([
    
    # Main Dashboard Header
    html.H1("Australia Wildfire Dashboard", className="header-title"),

    # The top control panel containing our Dropdown filters
    html.Div([
        
        # Region Dropdown
        html.Div([
            html.H2("Select Region"),
            dcc.Dropdown(
                id='region', # The ID tells our Python backend which dropdown this is
                options=[{'label': r, 'value': r} for r in regions], # Create dropdown choices from our unique regions list
                value='New South Wales',  # Set the default selected value
                className='dropdown',
                style={'color': '#000'} # Text inside the dropdown is black
            )
        ], className="control-container"),

        # Year Dropdown
        html.Div([
            html.H2("Select Year"),
            dcc.Dropdown(
                id='year',
                options=[{'label': y, 'value': y} for y in years],
                value=years[0], # Default to the very first year in the sorted list
                className='dropdown',
                style={'color': '#000'}
            )
        ], className="control-container")
        
    ], className="top-controls"),

    # The Grid containing our four Plotly graphs
    # We use dcc.Graph components to hold the charts that we will generate with Python below.
    html.Div([
        html.Div([dcc.Graph(id='plot1')], className="graph-container"),
        html.Div([dcc.Graph(id='plot2')], className="graph-container"),
        html.Div([dcc.Graph(id='plot3')], className="graph-container"),
        html.Div([dcc.Graph(id='plot4')], className="graph-container"),
    ], className="graph-grid"),

    # Simple footer
    html.Footer("Created by Aayush Yagol 2025", className="footer")

], className='dark-theme')  # Wrap the entire layout in a 'dark-theme' class for styling via CSS


# -----------------------------------------------------------------------------------------
# STEP 3: BACKEND LOGIC (INTERACTIVITY)
# -----------------------------------------------------------------------------------------

# The @app.callback decorator acts as the bridge between the Website and our Python code.
# It says: Whenever an 'Input' property changes (like the value of the dropdowns),
# run the function below, and spit the results into the 'Output' properties (the 'figure' attributes of our graphs).
@app.callback(
    [Output('plot1', 'figure'),
     Output('plot2', 'figure'),
     Output('plot3', 'figure'),
     Output('plot4', 'figure')],
    [Input('region', 'value'),
     Input('year', 'value')]
)
def update_graphs(region, year):
    # This function is triggered automatically by Dash when the user interacts with the page.
    # The 'region' and 'year' arguments are passed in from the Dropdowns.
    
    # Filter the raw dataframe to match the user's selected Region and Year. 
    # We use this raw data entirely for the Scatter plot.
    dff = df[(df['Region'] == region) & (df['Year'] == year)]

    # 1. Pie Chart: Filter our pre-calculated global pie data and create a Pie chart using Plotly Express (px).
    pie_data = global_pie_data[(global_pie_data['Region'] == region) & (global_pie_data['Year'] == year)]
    fig1 = px.pie(pie_data, names='Month', values='Estimated_fire_area',
                  title=f"{region}: Avg Fire Area by Month ({year})",
                  color_discrete_sequence=px.colors.sequential.Reds) # Red color theme

    # 2. Bar Chart: Filter pre-calculated bar data to show Pixel Count by Month
    bar_data = global_bar_data[(global_bar_data['Region'] == region) & (global_bar_data['Year'] == year)]
    fig2 = px.bar(bar_data, x='Month', y='Count',
                  title=f"{region}: Avg Pixel Count by Month ({year})",
                  color='Count', color_continuous_scale='Inferno') # the 'Inferno' color scale shows heat density

    # 3. Line Chart: Filter pre-calculated line data to track Fire Brightness over the months
    line_data = global_line_data[(global_line_data['Region'] == region) & (global_line_data['Year'] == year)]
    fig3 = px.line(line_data, x='Month', y='Mean_estimated_fire_brightness',
                   title=f"{region}: Fire Brightness Trend ({year})", markers=True)

    # 4. Bubble Scatter Plot: Compare Radiative Power vs Brightness using the raw filtered data
    fig4 = px.scatter(dff, x='Mean_estimated_fire_brightness', y='Mean_estimated_fire_radiative_power',
                      title=f"{region}: Radiative Power vs Brightness ({year})",
                      color='Estimated_fire_area', size='Count')

    # Iterate through all four generated charts and apply a dark-mode theme
    # This edits the layout dictionaries to match the aesthetic of the external CSS file.
    for fig in [fig1, fig2, fig3, fig4]:
        fig.update_layout(
            paper_bgcolor="#1e1e1e", # Dark background outside the chart lines
            plot_bgcolor="#1e1e1e",  # Dark background inside the chart lines
            font=dict(color="white", family="'Inter', 'Segoe UI', sans-serif", size=14),
            title_font=dict(size=22, family="'Inter', 'Segoe UI', sans-serif", color='white')
        )

    # Return exactly four objects, mapping to plot1, plot2, plot3, and plot4 respectively.
    # Note: Returning them as a tuple (fig1, fig2...) is required in Dash to prevent backend unpacking errors.
    return (fig1, fig2, fig3, fig4)

# -----------------------------------------------------------------------------------------
# STEP 4: RUN SERVER
# -----------------------------------------------------------------------------------------

# The standard Python entry point. If we are running this script directly, start the local development server.
if __name__ == '__main__':
    app.run_server(debug=True)
