"""
Title
"""
from main import *
import csv




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
