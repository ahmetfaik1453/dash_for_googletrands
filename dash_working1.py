import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from pytrends.request import TrendReq
from datetime import datetime
import time
import webbrowser

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Google Trends Keyword Suggestions"),
    
    # Input for keywords
    html.Div([
        html.Label("Keywords (comma separated):"),
        dcc.Input(id='keyword-input', value='recession,stock market', type='text', style={'width': '50%'}),
    ]),
    
    # Date range inputs
    html.Div([
        html.Label("Start Date (YYYY-MM-DD):"),
        dcc.Input(id='start-date', value="2004-01-01", type='text', style={'width': '20%'}),
        html.Label("End Date (YYYY-MM-DD):"),
        dcc.Input(id='end-date', value=datetime.today().strftime('%Y-%m-%d'), type='text', style={'width': '20%'}),
    ]),
    
    # Country dropdown
    html.Div([
        html.Label("Select Country:"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[
                {'label': 'US', 'value': 'US'},
                {'label': 'GB', 'value': 'GB'},
                {'label': 'AU', 'value': 'AU'},
                {'label': 'IN', 'value': 'IN'},
                {'label': 'Global', 'value': 'global'}
            ],
            value='US'
        )
    ]),
    
    # Graph
    dcc.Graph(id='trends-graph', config={'displayModeBar': True}, style={'height': '80vh'}),
    
    # Status
    html.Div(id='status', style={'marginTop': '20px'})
])

@app.callback(
    Output('trends-graph', 'figure'),
    Output('status', 'children'),
    Input('keyword-input', 'value'),
    Input('start-date', 'value'),
    Input('end-date', 'value'),
    Input('country-dropdown', 'value')
)
def update_graph(keywords, start_date, end_date, country):
    pytrends = TrendReq()
    keywords_list = [kw.strip() for kw in keywords.split(',')]
    timeframe = f"{start_date} {end_date}"
    geo = country

    # Check for invalid date format
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return {'data': [], 'layout': go.Layout(title='Error')}, "Invalid date format. Please use YYYY-MM-DD."

    try:
        # Try fetching global data first
        if geo == 'global':
            geo = ''
        pytrends.build_payload(keywords_list, timeframe=timeframe, geo=geo)
        time.sleep(1)  # Delay of 1 second
        data = pytrends.interest_over_time()
        
        if data.empty and geo == '':
            # If no data for global, try country-specific data
            status = "Global data not available. Trying country-specific data."
            geo_list = ['US', 'GB', 'AU', 'IN']
            traces = []
            for g in geo_list:
                pytrends.build_payload(keywords_list, timeframe=timeframe, geo=g)
                time.sleep(1)
                data = pytrends.interest_over_time()
                if not data.empty:
                    for keyword in keywords_list:
                        traces.append(go.Scatter(x=data.index, y=data[keyword], mode='lines', name=f"{keyword} ({g})", line=dict(width=2)))
            figure = {
                'data': traces,
                'layout': go.Layout(
                    title='Google Trends (Logarithmic Scale)',
                    xaxis={
                        'title': 'Date',
                        'rangeslider': {'visible': True},
                        'showline': True,
                        'linewidth': 1,
                        'linecolor': 'black'
                    },
                    yaxis={
                        'title': 'Interest (Log Scale)',
                        'type': 'log',
                        'showline': True,
                        'linewidth': 1,
                        'linecolor': 'black'
                    },
                    hovermode='x unified',
                    margin={'l': 40, 'r': 0, 't': 40, 'b': 40},
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(255,255,255,0.9)'
                )
            }
        elif not data.empty:
            traces = []
            for keyword in keywords_list:
                traces.append(go.Scatter(x=data.index, y=data[keyword], mode='lines', name=keyword, line=dict(width=2)))
            figure = {
                'data': traces,
                'layout': go.Layout(
                    title='Google Trends (Logarithmic Scale)',
                    xaxis={
                        'title': 'Date',
                        'rangeslider': {'visible': True},
                        'showline': True,
                        'linewidth': 1,
                        'linecolor': 'black'
                    },
                    yaxis={
                        'title': 'Interest (Log Scale)',
                        'type': 'log',
                        'showline': True,
                        'linewidth': 1,
                        'linecolor': 'black'
                    },
                    hovermode='x unified',
                    margin={'l': 40, 'r': 0, 't': 40, 'b': 40},
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(255,255,255,0.9)'
                )
            }
            status = "Data successfully fetched and plotted."
        else:
            figure = {'data': [], 'layout': go.Layout(title='No Data Available')}
            status = "No data available to plot."
    except Exception as e:
        figure = {'data': [], 'layout': go.Layout(title='Error')}
        status = f"An error occurred: {e}"

    return figure, status

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    # Ensure the server is fully started before opening the browser
    time.sleep(2)  # Adjust this sleep duration if necessary
    webbrowser.open('http://127.0.0.1:8050/')
