"""CSC111 Project 2: LACK's Franchise Analyzer

This module contains the functions responsible for the data visualization.

Created by Leandro Hamaguchi, Aryan Nair, Carlos Solares, and Karan Singh. (LACK)
TODO: Finish file dosctring!
TODO: Add RI and IA to every class (update if needed)!
TODO: Explain, in the docstring, new terms created (e.g. cluster, vertex type, etc.)
"""
import plotly.graph_objects as go


def visualize_map(final_data: dict, edge_data: set):
    """
    Creates a map visualization of the region we're considering, i.e., where the Franchises, Transit points and the
    Landmarks are located.
    """
    vertices = {}
    for vertex in final_data:
        vertices[vertex.item] = {'coordinates': final_data[vertex].vertex_data['coordinates'],
                                 'cluster': final_data[vertex].vertex_data['cluster']}
    # Connections (lines) between vertices
    connections = edge_data

    fig = go.Figure()

    # Add lines for each connection
    for conn in connections:
        start_vertex, end_vertex = conn
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=[vertices[start_vertex]['coordinates'][0], vertices[end_vertex]['coordinates'][0]],
            lat=[vertices[start_vertex]['coordinates'][1], vertices[end_vertex]['coordinates'][1]],
            line=dict(width=2, color='black'),  # Customize line color here
        ))

    # Add markers for the vertices
    for vertex, details in vertices.items():
        if details['cluster'] == 0:
            c = 'light blue'
        elif details['cluster'] == 1:
            c = 'salmon'
        elif details['cluster'] == 2:
            c = 'green'
        elif details['cluster'] == 3:
            c = 'red'
        elif details['cluster'] == 4:
            c = 'sandybrown'
        elif details['cluster'] == 5:
            c = 'blue'
        elif details['cluster'] == 6:
            c = 'turquoise'
        elif details['cluster'] == 7:
            c = 'brown'
        elif details['cluster'] == 8:
            c = 'orange'
        elif details['cluster'] == 9:
            c = 'yellow'
        elif details['cluster'] == 10:
            c = 'coral'
        elif details['cluster'] == 11:
            c = 'purple'
        elif details['cluster'] == 12:
            c = 'palegoldenrod'
        elif details['cluster'] == 13:
            c = 'seashell'
        elif details['cluster'] == 14:
            c = 'olive'
        fig.add_trace(go.Scattermapbox(
            mode="markers+text",
            lon=[details['coordinates'][0]],
            lat=[details['coordinates'][1]],
            marker={'size': 10, 'color': c},
            name=vertex,
            text=vertex,
            textposition="top center"
        ))

    fig.update_layout(
        mapbox={
            'style': "open-street-map",
            'zoom': 5,  # Adjust the zoom level as needed
            'center': {'lon': 35, 'lat': 25}  # Center of the map for better visualization
        },
        showlegend=True,
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0}
    )

    fig.show()


def visualize_square_graph():
    """
    Creates a square graph visualization of the intangible Franchise data.
    """
