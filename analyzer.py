"""CSC111 Project 2: LACK's Franchise Analyzer

This module contains the calculate score function, main program loop, and the visualization functions for
Franchise Analyzer.

Created by Leandro Hamaguchi, Aryan Nair, Carlos Solares, and Karan Singh. (LACK)
TODO: Finish file dosctring!
TODO: Add RI and IA to every class (update if needed)!
TODO: Explain, in the docstring, new terms created (e.g. cluster, vertex type, etc.)
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


factor_weights = [0.45, 0.3, 0.2]  # TODO: Check weights
generator = GraphGenerator('vertex_data.csv', 'edge_data.csv', factor_weights)
scaled_graph = generator.scaled_graph
normal_graph = generator.normal_graph

# Main program loop
state = True
menu = ['sg', 'ng', 'exit', '.']
print("Initializing analyzer...\n")

while state:
    user_input = input("Type a command: ")
    if user_input == 'exit':
        state = False
    elif user_input == 'sg':
        visualize_map()  # TODO: implement
    elif user_input == 'ng':
        visualize_square_graph()  # TODO: implement
    else:
        user_input = input("Enter a valid command: ")
