import dash
from dash import html, dcc
import plotly.graph_objs as go
import numpy as np

# Generate a large dataset for the heatmap
data_size = 5500  # Adjust this to simulate different resolutions
x = np.linspace(0, 1, data_size)
y = np.linspace(0, 1, data_size)
X, Y = np.meshgrid(x, y)
Z = np.sin(X * 2 * np.pi) * np.cos(Y * 2 * np.pi)  # Example function for heatmap data

# Create the heatmap
heatmap = go.Figure(data=go.Heatmap(
    z=Z,
    x=x,
    y=y,
    colorscale='Viridis'
))

heatmap.update_layout(
    title='High-Resolution Heatmap',
    xaxis_nticks=36,
    yaxis_nticks=36
)

# Create a Dash application
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Graph(
        id='heavy-heatmap',
        figure=heatmap
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
