"""CSC111 Project 2: CALK's Franchise Analyzer

This module contains the functions responsible for computing the data.

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
from program_data import _WeightedVertex, WeightedGraph


def get_franchises(franchise1: str, franchise2: str, graph: WeightedGraph) -> tuple[_WeightedVertex, _WeightedVertex]:
    """Returns the vertices corresponding to franchise 1 and franchise 2.
    """
    vertices = graph.get_vertices()
    v1 = vertices[franchise1]
    v2 = vertices[franchise2]
    return (v1, v2)


def calculate_score(franchise1: str, franchise2: str, factor_weights: dict[str, float], graph: WeightedGraph) -> \
        tuple[float, float]:
    """
    Calculates and returns score for each Franchise based on intangible and tangible data.

    Intangible factors are the factors of each of the McDonald's, and the tangible factors are weighted using edge
    weights.

    Preconditions:
        - graph.vertices != {}
        - franchise1 and franchise2 are valid franchises in the input graph.
        - len(factor_weights) must be equal to at least the length of the vertex_data attribute of the 2 franchises.
    """
    f1, f2 = get_franchises(franchise1, franchise2, graph)
    final_score1 = 0
    final_score2 = 0
    all_vertices = graph.get_vertices()

    for item in all_vertices:
        if all_vertices[item].vertex_type not in {'OtherRestaurant', 'TTC'}:
            final_score1 += 1 / f1.best_weighted_path(item, set())[0]
            final_score2 += 1 / f2.best_weighted_path(item, set())[0]

    f1_data = f1.vertex_data
    f2_data = f2.vertex_data

    f1_intangibles = 0
    f2_intangibles = 0
    for key in factor_weights:
        f1_intangibles += factor_weights[key] * f1_data[key]
        f2_intangibles += factor_weights[key] * f2_data[key]

    final_score1 += f1_intangibles
    final_score2 += f2_intangibles

    restaurant_competiton_1 = 0
    restaurant_competiton_2 = 0
    ttc_proximity_1 = 0
    ttc_proximity_2 = 0
    landmark_influence_1 = 0
    landmark_influence_2 = 0
    for v in all_vertices:
        if all_vertices[v].vertex_type == 'OtherRestaurant':
            competing_score =\
                0.65 * all_vertices[v].vertex_data['ClientSimilarity'] + 0.35 * all_vertices[v].vertex_data['Reviews']
            restaurant_range_1 = f1.best_weighted_path(v, {f2})[0]
            restaurant_range_2 = f2.best_weighted_path(v, {f1})[0]
            restaurant_competiton_1 += competing_score + restaurant_range_1
            restaurant_competiton_2 += competing_score + restaurant_range_2
        elif all_vertices[v].vertex_type == 'TTC':
            transit_score = all_vertices[v].vertex_data['Ridership'] / 731880  # 731880 is the largest average number of
            # daily TTC riders at a Subway Station (Bloor-Yonge).
            ttc_range_1 = f1.best_weighted_path(v, {f2})[0]
            ttc_range_2 = f2.best_weighted_path(v, {f1})[0]
            ttc_proximity_1 += transit_score + ttc_range_1
            ttc_proximity_2 += transit_score + ttc_range_2
        elif all_vertices[v].vertex_type == 'Landmark':
            landmark_score_f1 = \
                all_vertices[v].vertex_data['Significance'] * all_vertices[v].vertex_data['DistanceAGOMCD']
            landmark_score_f2 = \
                all_vertices[v].vertex_data['Significance'] * all_vertices[v].vertex_data['DistanceQSMCD']
            landmark_influence_1 += f1.best_weighted_path(v, {f2})[0] + landmark_score_f1
            landmark_influence_2 += f2.best_weighted_path(v, {f1})[0] + landmark_score_f2

    final_score1 += ttc_proximity_1 - restaurant_competiton_1 + landmark_influence_1
    final_score2 += ttc_proximity_2 - restaurant_competiton_2 + landmark_influence_2
    return round(final_score1 / 100, 2), round(final_score2 / 100, 2)


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['csv', 'plotly.graph_objects', 'program_data'],
        'disable': ['R0914 '],
        'allowed-io': ['_check_len_data_row', 'load_edge_data', 'load_vertex_data'],
        'max-line-length': 120
    })
