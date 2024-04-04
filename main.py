"""CSC111 Project 2: LACK's Franchise Analyzer

This module contains the main block of code that runs the whole program.

Created by Leandro Hamaguchi, Aryan Nair, Carlos Solares, and Karan Singh. (LACK)
TODO: Finish file dosctring!
TODO: Add RI and IA to every class (update if needed)!
TODO: Explain, in the docstring, new terms created (e.g. cluster, vertex type, etc.)
"""
from program_data import *
from visualizer import *
from compute_data import *

INTANGIBLE_FACTOR_CATEGORIES = {
    'MCD': ['Vehicular Traffic', 'Pedestrian Traffic', 'Bike Traffic', 'Reviews', 'Operating Hours', 'Drive Through',
            'Wifi', 'Physical Limitations'],
    'OtherRestaurant': ['Reviews', 'Client Similarity'],
    'Landmark': ['Significance'],
    'IntersectionMain': ['Bike Per Car Ratio', 'Vehicular Traffic', 'Pedestrian Traffic Traffic'],
    'IntersectionSmall': [],
    'TTC': ['Google Reviews']
}
TANGIBLE_FACTOR_WEIGHTS = [0.45, 0.35, 0.2]  # TODO: Check weights

generator = GraphGenerator('vertex_data.csv', 'edge_data.csv',
                           TANGIBLE_FACTOR_WEIGHTS, INTANGIBLE_FACTOR_CATEGORIES)
scaled_graph = generator.scaled_graph
normal_graph = generator.normal_graph

calculate_score('QueenSpadina', 'AGO', [0.175, 0.125, 0.05, 0.2, 0.1, 0.3, 0.05], scaled_graph)

cluster_color_code = {
    0: 'light blue', 1: 'salmon', 2: 'green', 3: 'red', 4: 'sandybrown', 5: 'blue', 6: 'turquoise', 7: 'brown',
    8: 'orange', 9: 'yellow', 10: 'coral', 11: 'purple', 12: 'palegoldenrod', 13: 'seashell', 14: 'olive'
}

# Main program loop
state = True
menu = ['sg', 'ng', 'exit', '.']
print("Initializing analyzer...\n")

while state:
    user_input = input("Type a command from the following menu [sg, ng, compute, exit]: ").strip()
    if user_input == 'exit':
        state = False
    elif user_input == 'sg':
        visualize_map(scaled_graph.get_vertices(), scaled_graph.get_edges(), cluster_color_code)
    elif user_input == 'ng':
        visualize_map(normal_graph.get_vertices(), normal_graph.get_edges(), cluster_color_code)
    elif user_input == 'compute':
        calculate_score('QueenSpadina', 'AGO', [0.175, 0.125, 0.05, 0.2, 0.1, 0.3, 0.05], scaled_graph)
    else:
        user_input = input("Enter a valid command: ")
