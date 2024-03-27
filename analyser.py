"""
File that runs the main program
TODO: Finish file dosctring
"""


def get_franchise_locations(location1: str, location2: str) -> None:
    """
    Gets user's input (i.e. Franchise name).
    """


def calculate_score(data: dict) -> float:
    """
    Calculates and returns score for each Franchise based on intangible and tangible data.
    """


def visualize_map():
    """
    Creates a map visualization of the region where the Franchises and the Landmarks are located.
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
