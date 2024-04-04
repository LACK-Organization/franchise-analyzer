"""CSC111 Project 2: LACK's Franchise Analyzer

This module contains the functions responsible for computing the data.

Created by Leandro Hamaguchi, Aryan Nair, Carlos Solares, and Karan Singh. (LACK)
TODO: Finish file dosctring!
TODO: Add RI and IA to every class (update if needed)!
TODO: Explain, in the docstring, new terms created (e.g. cluster, vertex type, etc.)
"""
from program_data import _WeightedVertex, WeightedGraph


def get_franchises(franchise1: str, franchise2: str, graph: WeightedGraph) -> tuple[_WeightedVertex, _WeightedVertex]:
    """Returns the vertices corresponding to franchise 1 and franchise 2.
    """
    vertices = graph.get_vertices()
    v1 = vertices[franchise1]
    v2 = vertices[franchise2]
    return (v1, v2)


def calculate_score(franchise1: str, franchise2: str, factor_weights: list[float], graph: WeightedGraph) -> tuple[float, float]:
    """
    Calculates and returns score for each Franchise based on intangible and tangible data.

    Tangible data includes physical/locational factors such as proximity to public transit, landmarks nearby, ...
    TODO (To be filled)

    Intangible data includes factors like customer reviews, customer service, infrastructure, number of
    daily customers, ... TO DO (To be filled)

    Preconditions:
        TODO: Fill this in
    """
    f1, f2 = get_franchises(franchise1, franchise2, graph)
    final_score1 = 0
    final_score2 = 0

    for u in graph.vertices:
        if graph.vertices[u].vertex_type not in {'OtherRestaurant', 'TTC'}:
            final_score1 += 1 / f1.best_weighted_path(u, set())[0]
            final_score2 += 1 / f2.best_weighted_path(u, set())[0]

    f1_data = list(f1.vertex_data.values())
    f2_data = list(f2.vertex_data.values())

    f1_intangibles = 0
    f2_intangibles = 0
    for i in range(len(factor_weights)):
        f1_intangibles += factor_weights[i] * f1_data[i]
        f2_intangibles += factor_weights[i] * f2_data[i]

    final_score1 += f1_intangibles
    final_score2 += f2_intangibles

    restaurant_competiton_1 = 0
    restaurant_competiton_2 = 0
    ttc_proximity_1 = 0
    ttc_proximity_2 = 0
    all_vertices = graph.vertices
    for v in all_vertices:
        if all_vertices[v].vertex_type == 'OtherRestaurant':
            competing_score = 0.65 * all_vertices[v].vertex_data['Client SImilarity']\
                              + 0.35 * all_vertices[v].vertex_data['Review']
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

    final_score1 += ttc_proximity_1 - restaurant_competiton_1
    final_score2 += ttc_proximity_2 - restaurant_competiton_2
    return (final_score1, final_score2)


# def proximity_to_transit(v1: str, transit_stop: str, visited: set[_WeightedVertex]) -> float:
#     """Returns the score of the optimal path between a """
