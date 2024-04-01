import csv

"""File that runs the main program
TODO: Finish file dosctring"""


def data_collector(datafile: str, name: str, type: str) -> dict:
    """Return the data associtated with the vertex"""
    with open(datafile, 'r') as file1:
        reader = csv.reader(file1)
        data_mapping = {}
        for row in reader:
            if str(row[2]) == name and row[0] == type:
                if str(row[0]) == 'MCD':
                    data_mapping['Type'] = str(row[0])
                    data_mapping['Cluster'] = int(row[1])
                    data_mapping['Name'] = str(row[2])
                    data_mapping['Vehicular Traffic'] = int(row[3])
                    data_mapping['Pedestrian Traffic'] = int(row[4])
                    data_mapping['Bike Traffic'] = int(row[5])
                    data_mapping['Reviews'] = int(row[6])
                    data_mapping['Crime Rate'] = int(row[7])
                    data_mapping['Operating Hours'] = int(row[8])
                    data_mapping['Drive Through'] = int(row[9])
                    data_mapping['Wifi'] = int(row[10])
                elif str(row[0]) == 'OtherRestaurant':
                    data_mapping['Type'] = str(row[0])
                    data_mapping['Cluster'] = int(row[1])
                    data_mapping['Name'] = str(row[2])
                    data_mapping['Reviews'] = int(row[3])
                    data_mapping['Client Similarity'] = int(row[4])
                elif str(row[0]) == 'Landmark':
                    data_mapping['Type'] = str(row[0])
                    data_mapping['Cluster'] = int(row[1])
                    data_mapping['Name'] = str(row[2])
                    data_mapping['Significance'] = int(row[3])
                elif str(row[0]) == 'Intersection':
                    data_mapping['Type'] = str(row[0])
                    data_mapping['Cluster'] = int(row[1])
                    data_mapping['Name'] = str(row[2])
                    data_mapping['Bike Per Car Ratio'] = str(row[3])
                    data_mapping['Vehicular Traffic'] = str(row[4])
                    data_mapping['Pedestrian Traffic Traffic'] = str(row[5])
                else:
                    data_mapping['Type'] = str(row[0])
                    data_mapping['Cluster'] = int(row[1])
                    data_mapping['Name'] = str(row[2])
                    data_mapping['GoogleReviews(REVIEWxREVNUM)'] = int(row[3])
    return data_mapping


def get_franchise_locations(location1: str, location2: str) -> None:
    """
    Gets user's input (i.e. Franchise location).

    This function will take the user's input, which will consist of the locations of the franchises they wish to analyze
    and compare. The function will find the franchises from the dataset using these locations.

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
