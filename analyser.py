"""
Title
"""
from main import *
import csv




"""File that runs the main program
TODO: Finish file dosctring"""



def calculate_score(location1: str, graph: Graph, datafile: str) -> float:
    """
    Calculates and returns score for each Franchise based on intangible and tangible data.

    Tangible data includes physical/locational factors such as proximity to public transit, landmarks nearby, ...
    TODO (To be filled)

    Intangible data includes factors like customer reviews, customer service, infrastructure, number of
    daily customers, ... TODO (To be filled)

    Preconditions:
        TODO: Fill this in
    """
    vertex_data = data_collector(location1, datafile, 'MCD')
    score = 0





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
    """Return the data corresponding to every road in the region."""

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
