"""
Title
"""
from main import *
import csv




"""File that runs the main program
TODO: Finish file dosctring"""



def calculate_score(location1: str, data: DataEngine, datafile: str) -> tuple[float, float]:
    """
    Calculates and returns score for each Franchise based on intangible and tangible data.

    Tangible data includes physical/locational factors such as proximity to public transit, landmarks nearby, ...
    TODO (To be filled)

    Intangible data includes factors like customer reviews, customer service, infrastructure, number of
    daily customers, ... TO DO (To be filled)

    Preconditions:
        TODO: Fill this in
    """

    mcd_1 = ''
    mcd_2 = ''
    graph = data.graph_map
    for v in graph.vertices:
        if isinstance(graph.vertices[v], int):
            for vertex in graph.vertices[v]:
                vertex_vertex = graph.vertices[v][vertex]
                if vertex_vertex.vertex_type == 'MCD' and vertex_vertex.item == 'QueenSpadina':
                    mcd_1 = vertex_vertex
                elif vertex_vertex.vertex_type == 'MCD' and vertex_vertex.item == 'AGO':
                    mcd_2 = vertex_vertex
    final_score1 = 0
    final_score2 = 0
    for point in graph.vertices:
        final_score1 += 1 / graph.best_weighted_score(point, mcd_1.item, {mcd_2})
        final_score2 += 1 / graph.best_weighted_score(point, mcd_2.item, {mcd_1})
    mcd_1_data = mcd_1.vertex_data
    mcd_2_data = mcd_2.vertex_data
    mcd_1_score = 0.175 * mcd_1_data['Vehicular Traffic'] + 0.125 * mcd_1_data['Pedestrian Traffic']\
                  + 0.05 * mcd_1_data['Bike Traffic'] + 0.2 * mcd_1_data['Reviews']\
                  + 0.1 * mcd_1_data['Operating Hours'] + 0.3 * mcd_1_data['Drive Through'] + 0.05 * mcd_1_data['Wifi']
    mcd_2_score = 0.175 * mcd_2_data['Vehicular Traffic'] + 0.125 * mcd_2_data['Pedestrian Traffic']\
                  + 0.05 * mcd_2_data['Bike Traffic'] + 0.2 * mcd_2_data['Reviews']\
                  + 0.1 * mcd_2_data['Operating Hours'] + 0.3 * mcd_2_data['Drive Through'] + 0.05 * mcd_2_data['Wifi']
    final_score1 += mcd_1_score
    final_score2 += mcd_2_score
    return (final_score1, final_score2)


        point1_1, point2_1 = 0, 1
        point1_2, point2_2 = 0, 1
        # while point1_1 < len(path1) and point2_1 <= len(path1):
        #     edge_score_1 += (1 - data.get_weight(path1[point1_1], path1[point2_1])) * get_distance(path1[point1_1],
        #                                                                                            path1[point2_1])
        #     point1_1 += 1
        #     point2_1 += 1
        # while point1_2 < len(path2) and point2_2 <= len(path2):
        #     edge_score_2 += (1 - data.get_weight(path2[point1_2], path2[point2_2])) * get_distance(path2[point1_2],
        #                                                                                            path2[point2_2])
        #
        #     point1_2 += 1
        #     point2_2 += 1
        # final_score1 += 1 / edge_score_1
        # final_score2 += 1 / edge_score_2













def visualize_map():
    """
    Creates a map visualization of the region we're considering, i.e., where the Franchises, Transit points and the
    Landmarks are located.
    """


def visualize_square_graph():
    """
    Creates a square graph visualization of the intangible Franchise data.
    """


def edge_data(vertex1: str | int, vertex2: str | int, edge_file: str) -> dict:
    """Return the data corresponding to the edge between vertex1 and vertex2."""

    with open(edge_file, 'r') as roads:
        reader = csv.reader(roads)
        mapping = {}
        for row in reader:
            if row[0] == vertex1 and row[1] == vertex2:
                mapping['vertex1'] = row[0]
                mapping['vertex2'] = row[1]
                mapping['distance'] = row[2]
                mapping['safety'] = row[3]
                mapping['road hierarchy'] = row[4]
                mapping['speed limit'] = row[5]
    return mapping





# Main program loop

state = True
print("What are the locations of the franchises you want to analyse?\n")
location1 = input("Write the name of the first location: ").strip()
location2 = input("\nWrite the name of the second location: ").strip()
get_franchise_locations(location1, location2)

# while not state:
