"""CSC111 Project 2: CALK's Franchise Analyzer

This module contains the functions responsible for the data visualization.

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
import csv
import plotly.graph_objects as go
from program_data import _WeightedVertex


def visualize_map(vertex_data: dict[str, _WeightedVertex], edge_data: set[tuple[str, str]],
                  cluster_color_code: dict[int, str]) -> None:
    """
    Creates a map visualization of the region we're considering, i.e., where the Franchises, Transit points and the
    Landmarks are located.
    """
    vertex_to_params = {}
    for item in vertex_data:
        vertex_to_params[item] = {'coordinates': vertex_data[item].coordinates,
                                  'cluster': vertex_data[item].cluster}

    connections = edge_data

    fig = go.Figure()

    for conn in connections:
        start_vertex, end_vertex = conn
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=[vertex_to_params[start_vertex]['coordinates'][0], vertex_to_params[end_vertex]['coordinates'][0]],
            lat=[vertex_to_params[start_vertex]['coordinates'][1], vertex_to_params[end_vertex]['coordinates'][1]],
            line=dict(width=2, color='black'),
        ))

    for vertex_item, details in vertex_to_params.items():
        c = cluster_color_code[details['cluster']]
        fig.add_trace(go.Scattermapbox(
            mode="markers+text",
            lon=[details['coordinates'][0]],
            lat=[details['coordinates'][1]],
            marker={'size': 10, 'color': c},
            name=vertex_item,
            text=vertex_item,
            textposition="top center"
        ))

    fig.update_layout(
        mapbox={
            'style': "open-street-map",
            'zoom': 15,
            'center': {'lon': -79.392887, 'lat': 43.651471}
        },
        showlegend=True,
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0}
    )

    fig.show()


def visualize_tree_map(treemap_data: str, vertex_data: str, name: str, label_to_weight: dict[str, float]) -> None:
    """
       Creates a TreeMap visualization of all the factors that contribute to the success of the specified
       McDonald's location.
       """
    with open(treemap_data, 'r') as file1:
        reader1 = csv.reader(file1)
        lst = []
        for row in reader1:
            for item in row:
                lst.append(float(item))

    with open(vertex_data, 'r') as file2:
        reader2 = csv.reader(file2)
        mcdonalds_data = []
        for row in reader2:
            if str(row[0]) == 'MCD' and str(row[2]) == name:
                mcdonalds_data = [float(row[3]), float(row[4]), float(row[5]),
                                  float(row[6]), float(row[7]), float(row[8]), float(row[9]), float(row[10])]

    labels = list(label_to_weight)
    items = list(label_to_weight.items())
    tuple_of_ratios = [(mcdonalds_data[j] / lst[j] * items[j][1], items[j][0]) for j in range(len(items))]

    scores = []
    for score in tuple_of_ratios:
        scores.append(score)

    scores.sort()

    ordered_variables = []
    for score in scores:
        ordered_variables.append(score[1])

    parents = [1, 1, 1, 1, 1, 1, 1, 1]
    for i in range(len(ordered_variables) - 1):
        if i == len(ordered_variables) - 1:
            k = labels.index(ordered_variables[i + 1])
            parents[k] = 1

        else:
            k = labels.index(ordered_variables[i])
            parents[k] = ordered_variables[i + 1]

    index_of_biggest = parents.index(1)
    parents[index_of_biggest] = ""

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        marker_colors=["pink", "royalblue", "lightgray", "purple", "cyan", "lightgray", "lightblue", "orange"]
    ))

    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['csv', 'plotly.graph_objects', 'program_data'],
        'disable': ['R0914', 'R1735'],
        'allowed-io': ['visualize_tree_map', 'load_tree_map'],
        'max-line-length': 120
    })
