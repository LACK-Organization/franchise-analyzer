"""CSC111 Project 2: LACK's Franchise Analyzer

This module contains the functions responsible for the data visualization.

Created by Leandro Hamaguchi, Aryan Nair, Carlos Solares, and Karan Singh. (LACK)
TODO: Finish file dosctring!
TODO: Add RI and IA to every class (update if needed)!
TODO: Explain, in the docstring, new terms created (e.g. cluster, vertex type, etc.)
"""
import plotly.graph_objects as go
import csv


def visualize_map(final_data: dict, edge_data: set):
    """
    Creates a map visualization of the region we're considering, i.e., where the Franchises, Transit points and the
    Landmarks are located.
    """
    vertices = {}
    for vertex in final_data:
        vertices[vertex.item] = {'coordinates': final_data[vertex].vertex_data['coordinates'],
                                 'cluster': final_data[vertex].vertex_data['cluster']}
    # Connections (lines) between vertices
    connections = edge_data

    fig = go.Figure()

    # Add lines for each connection
    for conn in connections:
        start_vertex, end_vertex = conn
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=[vertices[start_vertex]['coordinates'][0], vertices[end_vertex]['coordinates'][0]],
            lat=[vertices[start_vertex]['coordinates'][1], vertices[end_vertex]['coordinates'][1]],
            line=dict(width=2, color='black'),  # Customize line color here
        ))

    # Add markers for the vertices
    for vertex, details in vertices.items():
        if details['cluster'] == 0:
            c = 'light blue'
        elif details['cluster'] == 1:
            c = 'salmon'
        elif details['cluster'] == 2:
            c = 'green'
        elif details['cluster'] == 3:
            c = 'red'
        elif details['cluster'] == 4:
            c = 'sandybrown'
        elif details['cluster'] == 5:
            c = 'blue'
        elif details['cluster'] == 6:
            c = 'turquoise'
        elif details['cluster'] == 7:
            c = 'brown'
        elif details['cluster'] == 8:
            c = 'orange'
        elif details['cluster'] == 9:
            c = 'yellow'
        elif details['cluster'] == 10:
            c = 'coral'
        elif details['cluster'] == 11:
            c = 'purple'
        elif details['cluster'] == 12:
            c = 'palegoldenrod'
        elif details['cluster'] == 13:
            c = 'seashell'
        elif details['cluster'] == 14:
            c = 'olive'
        fig.add_trace(go.Scattermapbox(
            mode="markers+text",
            lon=[details['coordinates'][0]],
            lat=[details['coordinates'][1]],
            marker={'size': 10, 'color': c},
            name=vertex,
            text=vertex,
            textposition="top center"
        ))

    fig.update_layout(
        mapbox={
            'style': "open-street-map",
            'zoom': 5,  # Adjust the zoom level as needed
            'center': {'lon': 35, 'lat': 25}  # Center of the map for better visualization
        },
        showlegend=True,
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0}
    )

    fig.show()


def visualize_square_graph():
    """
    Creates a square graph visualization of the intangible Franchise data.
    """

def visualize_tree_map(treemap_data: str, vertex_data: str, name: str):
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
                                        float(row[6]), float(row[7]), float(row[8]), float(row[9])]

    labels = ["Vehicular Traffic", "Pedestrain Traffic", "Bike Traffic", "Reviews", "Hours Open",
              "Drive-Thru", "Wifi"]

    tuple_of_ratios = [(mcdonalds_data[0]/lst[0] * 0.175, "Vehicular Traffic"),
                       (mcdonalds_data[1]/lst[1] * 0.125, "Pedestrain Traffic"),
                       (mcdonalds_data[2]/lst[2] * 0.05, "Bike Traffic"),
                       (mcdonalds_data[3]/lst[3] * 0.2, "Reviews"),
                       (mcdonalds_data[4]/lst[4] * 0.10, "Hours Open"),
                       (mcdonalds_data[5]/lst[5] * 0.30, "Drive-Thru"),
                       (mcdonalds_data[6]/lst[6] * 0.05, "Wifi")]
    print(tuple_of_ratios)

    scores = []
    for score in tuple_of_ratios:
        scores.append(score)

    scores.sort()
    print(scores)

    ordered_variables = []
    for score in scores:
        ordered_variables.append(score[1])
    print(ordered_variables)

    parents = [1, 1, 1, 1, 1, 1, 1]
    for i in range(len(ordered_variables) - 1):
        if i == len(ordered_variables) - 1:
            k = labels.index(ordered_variables[i + 1])
            parents[k] = 1

        else:
            k = labels.index(ordered_variables[i])
            parents[k] = ordered_variables[i + 1]

    l = parents.index(1)
    parents[l] = ""


    print(parents)

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        marker_colors=["pink", "royalblue", "lightgray", "purple",
        "cyan", "lightgray", "lightblue"]
    ))

    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()
