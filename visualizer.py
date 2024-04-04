"""CSC111 Project 2: LACK's Franchise Analyzer

This module contains the functions responsible for the data visualization.

Created by Leandro Hamaguchi, Aryan Nair, Carlos Solares, and Karan Singh. (LACK)
TODO: Finish file dosctring!
TODO: Add RI and IA to every class (update if needed)!
TODO: Explain, in the docstring, new terms created (e.g. cluster, vertex type, etc.)
"""
import plotly.graph_objects as go
from program_data import _WeightedVertex


def visualize_map(vertex_data: dict[str, _WeightedVertex], edge_data: set[tuple[str, str]],
                  cluster_color_code: dict[int, str]) -> None:
    """
    Creates a map visualization of the region we're considering, i.e., where the Franchises, Transit points and the
    Landmarks are located.
    """
    vertex_to_params = {}
    for item in vertex_data:
        vertex_to_params[item] = {'coordinates': vertex_data[item].coordinates,
                                  'cluster': vertex_data[item].cluster}
    # Connections (lines) between vertices
    connections = edge_data

    fig = go.Figure()

    # Add lines for each connection
    for conn in connections:
        start_vertex, end_vertex = conn
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=[vertex_to_params[start_vertex]['coordinates'][0], vertex_to_params[end_vertex]['coordinates'][0]],
            lat=[vertex_to_params[start_vertex]['coordinates'][1], vertex_to_params[end_vertex]['coordinates'][1]],
            line=dict(width=2, color='black'),  # Customize line color here
        ))

    # Add markers for the vertices
    for vertex_item, details in vertex_to_params.items():
        c = cluster_color_code[details['cluster']]
        fig.add_trace(go.Scattermapbox(
            mode="markers+text",
            lon=[details['coordinates'][0]],
            lat=[details['coordinates'][1]],
            marker={'size': 10, 'color': c},
            name=vertex_item,
            text=vertex_item,
            textposition="top center"
        ))

    fig.update_layout(
        mapbox={
            'style': "open-street-map",
            'zoom': 15,  # Adjust the zoom level as needed
            'center': {'lon': -79.392887, 'lat': 43.651471}  # Center of the map for better visualization
        },
        showlegend=True,
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0}
    )

    fig.show()


def visualize_square_graph():
    """
    Creates a square graph visualization of the intangible Franchise data.
    """
