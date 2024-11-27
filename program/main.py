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
 - kar.singh@mail.utoronto.ca

This file is Copyright (c) CALK Team
"""
from program_data import *
from visualizer import *
from compute_data import *

INTANGIBLE_FACTOR_CATEGORIES = {
    'MCD': ['VehicularTraffic', 'PedestrianTraffic', 'BikeTraffic', 'Reviews', 'OperatingHours', 'DriveThru',
            'Wifi', 'PhysicalLimitations'],
    'OtherRestaurant': ['Reviews', 'ClientSimilarity'],
    'Landmark': ['Significance', 'DistanceAGOMCD', 'DistanceQSMCD'],
    'IntersectionMain': ['BikePerCarRatio', 'VehicularTraffic', 'PedestrianTraffic'],
    'IntersectionSmall': [],
    'TTC': ['Ridership']
}
INTANGIBLE_MCD_FACTOR_WEIGHTS = {
    'VehicularTraffic': 0.16, 'PedestrianTraffic': 0.12, 'BikeTraffic': 0.05, 'Reviews': 0.15,
    'OperatingHours': 0.1, 'DriveThru': 0.2, 'Wifi': 0.05, 'PhysicalLimitations': 0.17
}
TANGIBLE_FACTOR_WEIGHTS = [0.45, 0.35, 0.2]
CLUSTER_COLOR_CODE = {
    0: 'light blue', 1: 'salmon', 2: 'green', 3: 'red', 4: 'sandybrown', 5: 'blue', 6: 'turquoise', 7: 'brown',
    8: 'orange', 9: 'yellow', 10: 'coral', 11: 'purple', 12: 'palegoldenrod', 13: 'seashell', 14: 'olive'
}
mcd1, mcd2 = 'MCDQueenSpadina', 'MCDAGO'

GENERATOR = GraphGenerator('../data/vertex_data.csv', '../data/edge_data.csv',
                           TANGIBLE_FACTOR_WEIGHTS, INTANGIBLE_FACTOR_CATEGORIES)
SCALED_GRAPH = GENERATOR.scaled_graph
NORMAL_GRAPH = GENERATOR.normal_graph

# Main program loop
STATE = True
MENU = ['map', 'treemap1', 'treemap2', 'compute', 'exit']
print("Initializing analyzer...\n")

while STATE:
    USER_INPUT = input(f"Type a command from the following menu {MENU}: ").strip()
    if USER_INPUT == 'exit':
        STATE = False
    elif USER_INPUT == 'map':
        visualize_map(SCALED_GRAPH.get_vertices(), SCALED_GRAPH.get_edges(), CLUSTER_COLOR_CODE)
    elif USER_INPUT == 'treemap1':
        visualize_tree_map('treemap_data.csv', 'vertex_data.csv', mcd1,
                           INTANGIBLE_MCD_FACTOR_WEIGHTS)
    elif USER_INPUT == 'treemap2':
        visualize_tree_map('treemap_data.csv', 'vertex_data.csv', mcd2,
                           INTANGIBLE_MCD_FACTOR_WEIGHTS)
    elif USER_INPUT == 'compute':
        MCD1_SCORE, MCD2_SCORE = calculate_score(mcd1, mcd2, INTANGIBLE_MCD_FACTOR_WEIGHTS, SCALED_GRAPH)
        print(f'Queen-Spadina McDonald\'s score: {MCD1_SCORE}\n'
              f'AGO McDonald\'s score: {MCD2_SCORE}\n')
    else:
        USER_INPUT = input("Enter a valid command: ")


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['program_data', 'visualizer', 'compute_data'],
        'disable': ['E9998', 'E9997', 'E9992', 'W0401 '],
        'allowed-io': ['_check_len_data_row', 'load_edge_data', 'load_vertex_data'],
        'max-line-length': 120
    })
