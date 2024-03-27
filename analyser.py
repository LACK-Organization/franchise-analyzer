"""
File that runs the main program
TODO: Finish file dosctring
"""


def get_franchise_locations(location1: str, location2: str) -> None:
    """
    Gets user's input (i.e. Franchise location).

    This function will take the user's input, which will consist of the locations of the franchises they wish to analyze
    and compare. The function will find the franchises from the dtataset using these locations.

    Preconditions:
        - input != ''
        - all(i.isalnum() or i == '-' for i in input)
        - input is a valid franchise location
    """


def calculate_score(location1_data: dict, location2_data: dict) -> tuple[float]:
    """
    Calculates and returns score for each Franchise based on intangible and tangible data.

    Tangible data includes physical/locational factors such as proximity to public transit, landmarks nearby, ...
    TODO (To be filled)

    Intangible data includes factors like customer reviews, customer service, infrastructure, number of
    daily customers, ... TODO (To be filled)

    Preconditions:
        TODO: Fill this in
    """


def visualize_map():
    """
    Creates a map visualization of the region we're considering, i.e., where the Franchises, Transit points and the
    Landmarks are located.
    """


def visualize_square_graph():
    """
    Creates a square graph visualization of the intangible Franchise data.
    """


# Main program loop

state = True
print("What are the locations of the franchises you want to analyse?\n")
location1 = input("Write the name of the first location: ").strip()
location2 = input("\nWrite the name of the second location: ").strip()
get_franchise_locations(location1, location2)

while not state:
