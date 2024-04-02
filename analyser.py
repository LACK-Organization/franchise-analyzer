"""
Title
"""
from main import *
import csv
import plotly.graph_objects as go






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


def calculate_customer_choice(self, vertex: str, franchise1: str, franchise2: str, visited: set[Vertex]):
    """
    Calculate which McDonald's a customer would be more likely to go to, given the vertex of the
    customer's location. Uses the weighed edges to calculate the path with the highest score.

    Preconditions:
     -
    """
    score_franchise1 = best_score_to_franchise(vertex, franchise1, graph, visite)
    score_franchise2 = best_score_to_franchise(vertex, franchise2, graph)

def best_score_to_franchise(vertex1: str, vertex2: str, graph: Graph, visited: set[Vertex]):
    """Calculate the best score between any two points on the graph based on the weighted edges.
    """



def visualize_map():
    """
    Creates a map visualization of the region we're considering, i.e., where the Franchises, Transit points and the
    Landmarks are located.
    """
    lon = [30, 30, 40, 30]
    lat = [20, 30, 20, 40]
    text = ['Vertex 1', 'Vertex 2', 'Vertex 3', 'Vertex 4']

    connections = [
        {'start': 0, 'end': 1},
        {'start': 0, 'end': 2},
        {'start': 2, 'end': 1},
        {'start': 2, 'end': 3}
    ]

    fig = go.Figure()

    for conn in connections:
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=[lon[conn['start']], lon[conn['end']]],
            lat=[lat[conn['start']], lat[conn['end']]],
            marker={'size': 10},
        ))

    fig.add_trace(go.Scattermapbox(
        mode="markers+text",
        lon=lon,
        lat=lat,
        marker={'size': 10},
        text=text,
        textposition="top center"
    ))

    fig.update_layout(
        mapbox={
            'style': "open-street-map",
            'zoom': 5,
            'center': {'lon': -79.393425, 'lat': 43.651707}  # Center of the map
        },
        showlegend=False,
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0}
    )

    fig.show()


def visualize_square_graph():
    """
    Creates a square graph visualization of the intangible Franchise data.
    """


def edge_data(edge_file: str) -> list[dict]:
    """Return the data corresponding to every road in the region."""

    with open(edge_file, 'r') as roads:
        reader = csv.reader(roads)
        lst = []
        mapping = {}
        for row in reader:
            mapping['vertex1'] = row[0]
            mapping['vertex2'] = row[1]
            mapping['distance'] = row[2]
            mapping['safety'] = row[3]
            mapping['road hierarchy'] = row[4]
            mapping['speed limit'] = row[5]
            lst.append(mapping)
    return lst





# Main program loop

state = True
print("What are the locations of the franchises you want to analyse?\n")
location1 = input("Write the name of the first location: ").strip()
location2 = input("\nWrite the name of the second location: ").strip()
get_franchise_locations(location1, location2)

# while not state:
