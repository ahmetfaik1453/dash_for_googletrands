Google Trends Keyword Analysis Dashboard
This project is a Google Trends dashboard built with Dash and Plotly, designed to help users analyze the search interest of specific keywords over time. With options to input keywords, select a date range, and choose a region, this tool visualizes trends in a logarithmic scale, providing insights into shifts in interest.

Features
Keyword Input: Enter multiple keywords separated by commas to explore their search trends.
Date Range Selection: Define a start and end date in YYYY-MM-DD format for custom analysis.
Country Selection: Choose from specific countries or global trends. If global data is unavailable, the tool attempts country-specific data for fallback regions (US, GB, AU, IN).
Logarithmic Scale Visualization: Displays trends on a logarithmic scale, making fluctuations in search interest clearer and more interpretable.
Status Updates: Real-time messages display errors or availability updates for the data.
Installation
To run this app, you’ll need the following libraries. Install them with:

bash
Copy code
pip install dash plotly pytrends
Usage
Run the Application
Start the app by running:

bash
Copy code
python app.py
Open the Dashboard
Once started, the app will automatically open in your default browser at http://127.0.0.1:8050/.

Input Data

Keywords: Enter keywords separated by commas, e.g., recession, stock market.
Date Range: Specify start and end dates (e.g., 2004-01-01 to today’s date).
Country: Choose a country from the dropdown (e.g., US or global).
The graph will update automatically based on your inputs.

How It Works
This code initializes a Dash application with the following components:

Input Fields: dcc.Input for keywords and dates.
Dropdown Menu: dcc.Dropdown for selecting a country.
Graph Display: dcc.Graph to visualize trends.
A callback function retrieves data with pytrends, constructs a plot, and handles errors or empty data by providing clear feedback in the app.

Example
Keywords: recession, stock market
Date Range: 2004-01-01 to today’s date
Country: US or global
