"""CSC111 Project 2: CALK's Franchise Analyzer

This module contains the main block of code that runs the whole program.

Created by Leandro Hamaguchi, Aryan Nair, Carlos Solares, and Karan Singh. (CALK)

Copyright and Usage Information
===============================

This program is created solely for the personal and private use of CALK's members (Leandro Hamaguchi, Aryan Nair,
Carlos Solares, and Karan Singh). All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited. For more information on copyright send a message to one of the following emails:
 - l.brasil@mail.utoronto.ca
 - aryan.nair@mail.utoronto.ca
 - carlos.solares@mail.utoronto.ca
 - karan.singh@mail.utoronto.ca

This file is Copyright (c) CALK Team
TODO: Finish file dosctring!
TODO: Add RI and IA to every class (update if needed)!
TODO: Explain, in the docstring, new terms created (e.g. cluster, vertex type, etc.)
"""
from program_data import *
from visualizer import *
from compute_data import *

INTANGIBLE_FACTOR_CATEGORIES = {
    'MCD': ['VehicularTraffic', 'PedestrianTraffic', 'BikeTraffic', 'Reviews', 'OperatingHours', 'DriveThru',
            'Wifi', 'PhysicalLimitations'],
    'OtherRestaurant': ['Reviews', 'ClientSimilarity'],
    'Landmark': ['Significance'],
    'IntersectionMain': ['BikePerCarRatio', 'VehicularTraffic', 'PedestrianTraffic'],
    'IntersectionSmall': [],
    'TTC': ['Ridership']
}
INTANGIBLE_MCD_FACTOR_WEIGHTS = {
    'VehicularTraffic': 0.16, 'PedestrianTraffic': 0.12, 'BikeTraffic': 0.05, 'Reviews': 0.15,
    'OperatingHours': 0.1, 'DriveThru': 0.2, 'Wifi': 0.05, 'PhysicalLimitations': 0.17
}
TANGIBLE_FACTOR_WEIGHTS = [0.45, 0.35, 0.2]
cluster_color_code = {
    0: 'light blue', 1: 'salmon', 2: 'green', 3: 'red', 4: 'sandybrown', 5: 'blue', 6: 'turquoise', 7: 'brown',
    8: 'orange', 9: 'yellow', 10: 'coral', 11: 'purple', 12: 'palegoldenrod', 13: 'seashell', 14: 'olive'
}
mcd1, mcd2 = 'MCDQueenSpadina', 'MCDAGO'

generator = GraphGenerator('vertex_data.csv', 'edge_data.csv',
                           TANGIBLE_FACTOR_WEIGHTS, INTANGIBLE_FACTOR_CATEGORIES)
scaled_graph = generator.scaled_graph
normal_graph = generator.normal_graph

# Main program loop
state = True
menu = ['map', 'treemap1', 'treemap2', 'compute', 'exit']
print("Initializing analyzer...\n")

while state:
    user_input = input(f"Type a command from the following menu {menu}: ").strip()
    if user_input == 'exit':
        state = False
    elif user_input == 'map':
        visualize_map(scaled_graph.get_vertices(), scaled_graph.get_edges(), cluster_color_code)
    elif user_input == 'treemap1':
        visualize_tree_map('treemap_data.csv', 'vertex_data.csv', mcd1,
                           INTANGIBLE_MCD_FACTOR_WEIGHTS)
    elif user_input == 'treemap2':
        visualize_tree_map('treemap_data.csv', 'vertex_data.csv', mcd2,
                           INTANGIBLE_MCD_FACTOR_WEIGHTS)
    elif user_input == 'compute':
        mcd1_score, mcd2_score = calculate_score(mcd1, mcd2, INTANGIBLE_MCD_FACTOR_WEIGHTS, scaled_graph)
        print(f'Queen-Spadina McDonald\'s score: {mcd1_score}\n'
              f'AGO McDonald\'s score: {mcd2_score}\n')
    else:
        user_input = input("Enter a valid command: ")
