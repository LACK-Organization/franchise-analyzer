"""
Title
"""
from main import *
import csv
import plotly.graph_objects as go






"""File that runs the main program
TODO: Finish file dosctring"""



def calculate_score(location1: str, graph: WeightedGraph, datafile: str) -> float:
    """
    Calculates and returns score for each Franchise based on intangible and tangible data.

    Tangible data includes physical/locational factors such as proximity to public transit, landmarks nearby, ...
    TODO (To be filled)

    Intangible data includes factors like customer reviews, customer service, infrastructure, number of
    daily customers, ... TO DO (To be filled)

    Preconditions:
        TODO: Fill this in
    """
    score = 0
    mcd_1 = ''
    mcd_2 = ''
    for v in graph.vertices:
        if isinstance(graph.vertices[v], int):
            for vertex in graph.vertices[v]:
                vertex_vertex = graph.vertices[v][vertex]
                if vertex_vertex.vertex_type == 'MCD' and vertex_vertex.item == 'QueenSpadina':
                    mcd_1 = vertex
                elif vertex_vertex.vertex_type == 'MCD' and vertex_vertex.item == 'AGO':
                    mcd_2 = vertex
    for point in graph.vertices:
        # path1 =







def visualize_map():
    """
    Creates a map visualization of the region we're considering, i.e., where the Franchises, Transit points and the
    Landmarks are located.
    """
    lon = [30, 30, 40, 30]
    lat = [20, 30, 20, 40]
    text = ['Vertex 1', 'Vertex 2', 'Vertex 3', 'Vertex 4']

    connections = [
        {'start': 0, 'end': 1},
        {'start': 0, 'end': 2},
        {'start': 2, 'end': 1},
        {'start': 2, 'end': 3}
    ]

    fig = go.Figure()

    for conn in connections:
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=[lon[conn['start']], lon[conn['end']]],
            lat=[lat[conn['start']], lat[conn['end']]],
            marker={'size': 10},
        ))

    fig.add_trace(go.Scattermapbox(
        mode="markers+text",
        lon=lon,
        lat=lat,
        marker={'size': 10},
        text=text,
        textposition="top center"
    ))

    fig.update_layout(
        mapbox={
            'style': "open-street-map",
            'zoom': 5,
            'center': {'lon': -79.393425, 'lat': 43.651707}  # Center of the map
        },
        showlegend=False,
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0}
    )

    fig.show()


def visualize_square_graph():
    """
    Creates a square graph visualization of the intangible Franchise data.
    """


def edge_data(vertex1: str | int, vertex2: str | int, edge_file: str) -> dict:
    """Return the data corresponding to the edge between vertex1 and vertex2."""

    with open(edge_file, 'r') as roads:
        reader = csv.reader(roads)
        mapping = {}
        for row in reader:
            if row[0] == vertex1 and row[1] == vertex2:
                mapping['vertex1'] = row[0]
                mapping['vertex2'] = row[1]
                mapping['distance'] = row[2]
                mapping['safety'] = row[3]
                mapping['road hierarchy'] = row[4]
                mapping['speed limit'] = row[5]
    return mapping





# Main program loop

state = True
print("What are the locations of the franchises you want to analyse?\n")
location1 = input("Write the name of the first location: ").strip()
location2 = input("\nWrite the name of the second location: ").strip()
get_franchise_locations(location1, location2)

# while not state:
