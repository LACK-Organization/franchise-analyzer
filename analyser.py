"""
Title
"""
from main import *
import csv




"""File that runs the main program
TODO: Finish file dosctring"""



def calculate_score(location1_data: dict, location2_data: dict, graph: Graph) -> tuple[float]:
    """
    Calculates and returns score for each Franchise based on intangible and tangible data.

    Tangible data includes physical/locational factors such as proximity to public transit, landmarks nearby, ...
    TODO (To be filled)

    Intangible data includes factors like customer reviews, customer service, infrastructure, number of
    daily customers, ... TODO (To be filled)

    Preconditions:
        TODO: Fill this in
    """
    all_vertices = data_collector(datafile)


def visualize_map():
    """
    Creates a map visualization of the region we're considering, i.e., where the Franchises, Transit points and the
    Landmarks are located.
    """


def visualize_square_graph():
    """
    Creates a square graph visualization of the intangible Franchise data.
    """


def edge_data(edge_file: str) -> dict:
    """Return the data corresponding to every road in the region."""

    with open(edge_file, 'r') as roads:
        reader = csv.reader(roads)
        for row in reader:




# Main program loop

state = True
print("What are the locations of the franchises you want to analyse?\n")
location1 = input("Write the name of the first location: ").strip()
location2 = input("\nWrite the name of the second location: ").strip()
get_franchise_locations(location1, location2)

# while not state:
