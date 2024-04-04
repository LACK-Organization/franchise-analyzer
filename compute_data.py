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
        final_score1 += 1 / f1.best_weighted_path(u, set())[0]
        final_score2 += 1 / f2.best_weighted_path(u, set())[0]

    f1_data = list(f1.vertex_data.values())
    f2_data = list(f2.vertex_data.values())

    f1_intangibles = 0
    f2_intangibles = 0
    for i in range(len(factor_weights)):
        f1_intangibles += factor_weights[i] * f1_data[i]
        f2_intangibles += factor_weights[i] * f2_data[i]

    final_score1 += f1_score
    final_score2 += f2_score
    return (final_score1, final_score2)
