"""CSC111 Project 2: LACK's Franchise Analyzer

This module contains the main block of code that runs the whole program.

Created by Leandro Hamaguchi, Aryan Nair, Carlos Solares, and Karan Singh. (LACK)
TODO: Finish file dosctring!
TODO: Add RI and IA to every class (update if needed)!
TODO: Explain, in the docstring, new terms created (e.g. cluster, vertex type, etc.)
"""
from program_data import *


factor_weights = [0.45, 0.3, 0.2]  # TODO: Check weights
generator = GraphGenerator('vertex_data.csv', 'edge_data.csv', factor_weights)
scaled_graph = generator.scaled_graph
normal_graph = generator.normal_graph
visualize_map(scaled_graph.get_vertices(), scaled_graph.get_edges())

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
