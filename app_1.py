import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import calendar

# Initialize the Dash app
app = dash.Dash(__name__)

# Define color scheme for commodities
COMMODITY_COLORS = {
    'Coffee': '#6F4E37',
    'Cocoa': '#7B3F00',
    'Corn': '#FFC300',
    'Soybeans': '#228B22',
    'Cotton': '#F8F8FF'
}

# Create detailed event data
def create_events_data():
    events = []
    
    # Coffee Events - Brazil
    events.extend([
        {'commodity': 'Coffee', 'region': 'Brazil', 'event': 'Harvest Season', 'start_week': 1, 'end_week': 13, 'risk_level': 'Medium', 'description': 'Monitor for excessive rain disrupting harvest'},
        {'commodity': 'Coffee', 'region': 'Brazil', 'event': 'Frost Risk Period', 'start_week': 14, 'end_week': 22, 'risk_level': 'High', 'description': 'Critical frost risk in southern regions'},
        {'commodity': 'Coffee', 'region': 'Brazil', 'event': 'Peak Frost Risk', 'start_week': 23, 'end_week': 35, 'risk_level': 'Critical', 'description': 'Maximum frost risk during flowering'},
        {'commodity': 'Coffee', 'region': 'Brazil', 'event': 'Cherry Development', 'start_week': 36, 'end_week': 44, 'risk_level': 'Medium', 'description': 'Need adequate moisture'},
        {'commodity': 'Coffee', 'region': 'Brazil', 'event': 'Cherry Maturation', 'start_week': 45, 'end_week': 52, 'risk_level': 'Low', 'description': 'Monitor rainfall patterns'},
    ])
    
    # Coffee Events - Vietnam
    events.extend([
        {'commodity': 'Coffee', 'region': 'Vietnam', 'event': 'Dry Season', 'start_week': 1, 'end_week': 13, 'risk_level': 'High', 'description': 'Irrigation critical'},
        {'commodity': 'Coffee', 'region': 'Vietnam', 'event': 'Flowering', 'start_week': 14, 'end_week': 22, 'risk_level': 'High', 'description': 'Early monsoon critical'},
        {'commodity': 'Coffee', 'region': 'Vietnam', 'event': 'Growing Season', 'start_week': 23, 'end_week': 39, 'risk_level': 'Medium', 'description': 'Monitor for excessive rainfall'},
        {'commodity': 'Coffee', 'region': 'Vietnam', 'event': 'Harvest', 'start_week': 40, 'end_week': 52, 'risk_level': 'Medium', 'description': 'Dry conditions needed'},
    ])
    
    # Cocoa Events - West Africa
    events.extend([
        {'commodity': 'Cocoa', 'region': 'West Africa', 'event': 'Harmattan Winds', 'start_week': 1, 'end_week': 13, 'risk_level': 'High', 'description': 'Dry winds stress on trees'},
        {'commodity': 'Cocoa', 'region': 'West Africa', 'event': 'Critical Rains', 'start_week': 14, 'end_week': 26, 'risk_level': 'Critical', 'description': 'Early rains crucial for main crop'},
        {'commodity': 'Cocoa', 'region': 'West Africa', 'event': 'Dry Spell', 'start_week': 27, 'end_week': 35, 'risk_level': 'Medium', 'description': 'Monitor for drought stress'},
        {'commodity': 'Cocoa', 'region': 'West Africa', 'event': 'Main Harvest', 'start_week': 36, 'end_week': 48, 'risk_level': 'Medium', 'description': 'Excessive rain problematic'},
        {'commodity': 'Cocoa', 'region': 'West Africa', 'event': 'Mid-crop Development', 'start_week': 49, 'end_week': 52, 'risk_level': 'Low', 'description': 'Moderate moisture needed'},
    ])
    
    # Corn Events - USA
    events.extend([
        {'commodity': 'Corn', 'region': 'USA', 'event': 'Field Preparation', 'start_week': 10, 'end_week': 17, 'risk_level': 'Medium', 'description': 'Soil temperature/moisture critical'},
        {'commodity': 'Corn', 'region': 'USA', 'event': 'Planting Window', 'start_week': 14, 'end_week': 22, 'risk_level': 'High', 'description': 'Avoid wet fields'},
        {'commodity': 'Corn', 'region': 'USA', 'event': 'Pollination', 'start_week': 23, 'end_week': 31, 'risk_level': 'Critical', 'description': 'Heat/drought stress critical'},
        {'commodity': 'Corn', 'region': 'USA', 'event': 'Grain Fill', 'start_week': 32, 'end_week': 39, 'risk_level': 'High', 'description': 'High moisture needs'},
        {'commodity': 'Corn', 'region': 'USA', 'event': 'Harvest', 'start_week': 40, 'end_week': 48, 'risk_level': 'Medium', 'description': 'Dry conditions preferred'},
    ])
    
    # Corn Events - Brazil
    events.extend([
        {'commodity': 'Corn', 'region': 'Brazil', 'event': 'Safrinha Planting', 'start_week': 1, 'end_week': 13, 'risk_level': 'High', 'description': 'Rainfall critical after soybeans'},
        {'commodity': 'Corn', 'region': 'Brazil', 'event': 'Development', 'start_week': 14, 'end_week': 26, 'risk_level': 'Medium', 'description': 'Frost risk in south'},
        {'commodity': 'Corn', 'region': 'Brazil', 'event': 'Harvest', 'start_week': 27, 'end_week': 39, 'risk_level': 'Low', 'description': 'Dry weather needed'},
    ])
    
    # Soybeans Events - Brazil
    events.extend([
        {'commodity': 'Soybeans', 'region': 'Brazil', 'event': 'Planting', 'start_week': 36, 'end_week': 48, 'risk_level': 'High', 'description': 'Adequate moisture crucial'},
        {'commodity': 'Soybeans', 'region': 'Brazil', 'event': 'Pod Development', 'start_week': 49, 'end_week': 52, 'risk_level': 'High', 'description': 'Consistent rainfall needed'},
        {'commodity': 'Soybeans', 'region': 'Brazil', 'event': 'Pod Development Cont.', 'start_week': 1, 'end_week': 9, 'risk_level': 'High', 'description': 'Consistent rainfall needed'},
        {'commodity': 'Soybeans', 'region': 'Brazil', 'event': 'Harvest', 'start_week': 1, 'end_week': 13, 'risk_level': 'Medium', 'description': 'Varies by region'},
    ])
    
    # Soybeans Events - USA
    events.extend([
        {'commodity': 'Soybeans', 'region': 'USA', 'event': 'Planting', 'start_week': 14, 'end_week': 22, 'risk_level': 'High', 'description': 'Soil conditions critical'},
        {'commodity': 'Soybeans', 'region': 'USA', 'event': 'Flowering', 'start_week': 23, 'end_week': 31, 'risk_level': 'Critical', 'description': 'Stress sensitive period'},
        {'commodity': 'Soybeans', 'region': 'USA', 'event': 'Pod Fill', 'start_week': 32, 'end_week': 39, 'risk_level': 'High', 'description': 'Moisture critical'},
        {'commodity': 'Soybeans', 'region': 'USA', 'event': 'Harvest', 'start_week': 36, 'end_week': 44, 'risk_level': 'Medium', 'description': 'Dry conditions needed'},
    ])
    
    # Cotton Events - India
    events.extend([
        {'commodity': 'Cotton', 'region': 'India', 'event': 'Planting', 'start_week': 14, 'end_week': 26, 'risk_level': 'High', 'description': 'Monsoon onset timing'},
        {'commodity': 'Cotton', 'region': 'India', 'event': 'Peak Monsoon', 'start_week': 27, 'end_week': 39, 'risk_level': 'High', 'description': 'Excess rain risk'},
        {'commodity': 'Cotton', 'region': 'India', 'event': 'Boll Development', 'start_week': 40, 'end_week': 52, 'risk_level': 'Medium', 'description': 'Dry conditions needed'},
        {'commodity': 'Cotton', 'region': 'India', 'event': 'Harvest', 'start_week': 49, 'end_week': 52, 'risk_level': 'Low', 'description': 'Harvest period'},
        {'commodity': 'Cotton', 'region': 'India', 'event': 'Harvest Cont.', 'start_week': 1, 'end_week': 9, 'risk_level': 'Low', 'description': 'Harvest continues'},
    ])
    
    # Cotton Events - USA
    events.extend([
        {'commodity': 'Cotton', 'region': 'USA', 'event': 'Planting', 'start_week': 14, 'end_week': 22, 'risk_level': 'High', 'description': 'Temperature critical'},
        {'commodity': 'Cotton', 'region': 'USA', 'event': 'Flowering/Boll', 'start_week': 23, 'end_week': 35, 'risk_level': 'Critical', 'description': 'Heat/drought stress'},
        {'commodity': 'Cotton', 'region': 'USA', 'event': 'Harvest Prep', 'start_week': 36, 'end_week': 44, 'risk_level': 'High', 'description': 'Hurricane risk'},
        {'commodity': 'Cotton', 'region': 'USA', 'event': 'Main Harvest', 'start_week': 40, 'end_week': 48, 'risk_level': 'Medium', 'description': 'Dry conditions needed'},
    ])
    
    return pd.DataFrame(events)

# Create weather thresholds data
def create_thresholds_data():
    thresholds = [
        {'commodity': 'Coffee', 'temp_min': 2, 'temp_max': 30, 'rainfall_min': 1200, 'rainfall_max': 1800, 'critical_stage': 'Flowering/Frost'},
        {'commodity': 'Cocoa', 'temp_min': 15, 'temp_max': 35, 'rainfall_min': 1250, 'rainfall_max': 2500, 'critical_stage': 'Pod Development'},
        {'commodity': 'Corn', 'temp_min': 0, 'temp_max': 35, 'rainfall_min': 450, 'rainfall_max': 600, 'critical_stage': 'Pollination'},
        {'commodity': 'Soybeans', 'temp_min': 0, 'temp_max': 35, 'rainfall_min': 450, 'rainfall_max': 700, 'critical_stage': 'Pod Fill'},
        {'commodity': 'Cotton', 'temp_min': 5, 'temp_max': 40, 'rainfall_min': 500, 'rainfall_max': 1200, 'critical_stage': 'Boll Development'},
    ]
    return pd.DataFrame(thresholds)

# Load data
events_df = create_events_data()
thresholds_df = create_thresholds_data()

# Create weekly labels
week_labels = []
for month in range(1, 13):
    month_name = calendar.month_abbr[month]
    weeks_in_month = 4 if month != 12 else 5
    for week in range(weeks_in_month):
        week_num = len(week_labels) + 1
        if week_num <= 52:
            week_labels.append(f'W{week_num}-{month_name}')

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("Agricultural Weather Monitoring Dashboard", 
                style={'text-align': 'center', 'color': '#2c3e50', 'margin-bottom': '30px'}),
        html.P("Track critical weather events for Coffee, Cocoa, Corn, Soybeans, and Cotton across major producing regions",
               style={'text-align': 'center', 'color': '#7f8c8d', 'font-size': '18px'})
    ], style={'padding': '20px', 'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
              'color': 'white', 'margin-bottom': '30px'}),
    
    html.Div([
        # Control Panel
        html.Div([
            html.Div([
                html.Label("Select Commodity:", style={'font-weight': 'bold', 'margin-bottom': '5px'}),
                dcc.Dropdown(
                    id='commodity-dropdown',
                    options=[{'label': 'All Commodities', 'value': 'All'}] + 
                            [{'label': c, 'value': c} for c in events_df['commodity'].unique()],
                    value='All',
                    style={'width': '100%'}
                ),
            ], style={'margin-bottom': '20px'}),
            
            html.Div([
                html.Label("Select Region:", style={'font-weight': 'bold', 'margin-bottom': '5px'}),
                dcc.Dropdown(
                    id='region-dropdown',
                    options=[],
                    value='All',
                    style={'width': '100%'}
                ),
            ], style={'margin-bottom': '20px'}),
            
            html.Div([
                html.Label("Current Week:", style={'font-weight': 'bold', 'margin-bottom': '5px'}),
                dcc.Slider(
                    id='week-slider',
                    min=1,
                    max=52,
                    value=datetime.now().isocalendar()[1],
                    marks={i: {'label': week_labels[i-1] if i % 4 == 1 else '', 
                           'style': {'fontSize': '10px'}} for i in range(1, 53)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ], style={'margin-bottom': '20px'}),
        ], style={'width': '25%', 'padding': '20px', 'background': '#f8f9fa', 
                  'border-radius': '10px', 'margin-right': '20px'}),
        
        # Main Content Area
        html.Div([
            # Timeline Chart
            dcc.Graph(id='timeline-chart', style={'height': '500px'}),
            
            # Risk Assessment Cards
            html.Div(id='risk-cards', style={'margin-top': '20px'}),
            
            # Weather Thresholds
            html.Div([
                html.H3("Critical Weather Thresholds", style={'color': '#2c3e50', 'margin-bottom': '15px'}),
                html.Div(id='threshold-display')
            ], style={'margin-top': '30px', 'padding': '20px', 'background': '#f8f9fa', 
                     'border-radius': '10px'}),
        ], style={'width': '73%'}),
    ], style={'display': 'flex', 'padding': '20px'}),
    
    # Weekly Focus Section
    html.Div([
        html.H3("This Week's Focus", style={'color': '#2c3e50', 'margin-bottom': '15px'}),
        html.Div(id='weekly-focus', style={'padding': '20px', 'background': '#fff3cd', 
                                          'border-left': '5px solid #ffc107', 'border-radius': '5px'})
    ], style={'margin': '20px', 'padding': '20px', 'background': '#ffffff', 
              'border-radius': '10px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'})
])

# Callbacks
@app.callback(
    Output('region-dropdown', 'options'),
    Output('region-dropdown', 'value'),
    Input('commodity-dropdown', 'value')
)
def update_region_dropdown(commodity):
    if commodity == 'All':
        regions = events_df['region'].unique()
    else:
        regions = events_df[events_df['commodity'] == commodity]['region'].unique()
    
    options = [{'label': 'All Regions', 'value': 'All'}] + \
              [{'label': r, 'value': r} for r in regions]
    
    return options, 'All'

@app.callback(
    Output('timeline-chart', 'figure'),
    Input('commodity-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('week-slider', 'value')
)
def update_timeline(commodity, region, current_week):
    # Filter data
    filtered_df = events_df.copy()
    if commodity != 'All':
        filtered_df = filtered_df[filtered_df['commodity'] == commodity]
    if region != 'All':
        filtered_df = filtered_df[filtered_df['region'] == region]
    
    # Create Gantt chart
    fig = go.Figure()
    
    # Define colors for risk levels
    risk_colors = {
        'Critical': '#e74c3c',
        'High': '#f39c12',
        'Medium': '#3498db',
        'Low': '#2ecc71'
    }
    
    # Group by commodity for better visualization
    for comm in filtered_df['commodity'].unique():
        comm_df = filtered_df[filtered_df['commodity'] == comm]
        
        for _, row in comm_df.iterrows():
            # Create week range for x-axis
            weeks = list(range(row['start_week'], row['end_week'] + 1))
            y_pos = f"{row['commodity']} - {row['region']}"
            
            fig.add_trace(go.Scatter(
                x=weeks,
                y=[y_pos] * len(weeks),
                mode='lines+markers',
                name=f"{row['event']}",
                line=dict(color=risk_colors[row['risk_level']], width=15),
                marker=dict(size=8),
                hovertemplate=f"<b>{row['event']}</b><br>" +
                            f"Region: {row['region']}<br>" +
                            f"Risk: {row['risk_level']}<br>" +
                            f"Week: %{{x}}<br>" +
                            f"{row['description']}<extra></extra>"
            ))
    
    # Add current week indicator
    fig.add_vline(x=current_week, line_dash="dash", line_color="red", 
                  annotation_text=f"Current Week ({current_week})")
    
    fig.update_layout(
        title="Agricultural Event Timeline",
        xaxis_title="Week of Year",
        yaxis_title="Commodity - Region",
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 53, 4)),
            ticktext=[week_labels[i-1] for i in range(1, 53, 4)],
            range=[max(1, current_week-10), min(52, current_week+15)]
        ),
        height=500,
        hovermode='closest',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

@app.callback(
    Output('risk-cards', 'children'),
    Input('commodity-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('week-slider', 'value')
)
def update_risk_cards(commodity, region, current_week):
    # Filter current week events
    current_events = events_df[
        (events_df['start_week'] <= current_week) & 
        (events_df['end_week'] >= current_week)
    ]
    
    if commodity != 'All':
        current_events = current_events[current_events['commodity'] == commodity]
    if region != 'All':
        current_events = current_events[current_events['region'] == region]
    
    # Create risk summary cards
    risk_counts = current_events['risk_level'].value_counts()
    
    cards = []
    risk_colors = {
        'Critical': '#e74c3c',
        'High': '#f39c12',
        'Medium': '#3498db',
        'Low': '#2ecc71'
    }
    
    for risk in ['Critical', 'High', 'Medium', 'Low']:
        count = risk_counts.get(risk, 0)
        cards.append(
            html.Div([
                html.H4(str(count), style={'margin': '0', 'font-size': '36px', 'color': risk_colors[risk]}),
                html.P(f"{risk} Risk", style={'margin': '0', 'color': '#7f8c8d'})
            ], style={'text-align': 'center', 'padding': '15px', 'background': 'white',
                     'border-radius': '10px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)',
                     'width': '22%', 'display': 'inline-block', 'margin': '1%'})
        )
    
    return html.Div(cards, style={'text-align': 'center'})

@app.callback(
    Output('threshold-display', 'children'),
    Input('commodity-dropdown', 'value')
)
def update_thresholds(commodity):
    if commodity == 'All':
        display_df = thresholds_df
    else:
        display_df = thresholds_df[thresholds_df['commodity'] == commodity]
    
    threshold_cards = []
    for _, row in display_df.iterrows():
        card = html.Div([
            html.H5(row['commodity'], style={'color': COMMODITY_COLORS.get(row['commodity'], '#333'),
                                            'margin-bottom': '10px'}),
            html.Div([
                html.Span(f"🌡️ {row['temp_min']}°C - {row['temp_max']}°C", 
                         style={'margin-right': '20px'}),
                html.Span(f"💧 {row['rainfall_min']}-{row['rainfall_max']}mm/year",
                         style={'margin-right': '20px'}),
                html.Span(f"⚠️ Critical: {row['critical_stage']}", 
                         style={'font-weight': 'bold'})
            ])
        ], style={'padding': '15px', 'background': 'white', 'border-radius': '5px',
                 'margin-bottom': '10px', 'box-shadow': '0 1px 3px rgba(0,0,0,0.1)'})
        threshold_cards.append(card)
    
    return threshold_cards

@app.callback(
    Output('weekly-focus', 'children'),
    Input('week-slider', 'value')
)
def update_weekly_focus(current_week):
    # Get current week events
    current_events = events_df[
        (events_df['start_week'] <= current_week) & 
        (events_df['end_week'] >= current_week)
    ]
    
    # Get critical and high risk events
    critical_events = current_events[current_events['risk_level'].isin(['Critical', 'High'])]
    
    if len(critical_events) == 0:
        return html.P("No critical events this week. Continue routine monitoring.")
    
    focus_items = []
    for _, event in critical_events.iterrows():
        focus_items.append(
            html.Li([
                html.Strong(f"{event['commodity']} in {event['region']}: "),
                f"{event['event']} - {event['description']} ",
                html.Span(f"({event['risk_level']} Risk)", 
                         style={'color': '#e74c3c' if event['risk_level'] == 'Critical' else '#f39c12',
                               'font-weight': 'bold'})
            ], style={'margin-bottom': '10px'})
        )
    
    return html.Ul(focus_items)

if __name__ == '__main__':
    app.run_server(debug=True)