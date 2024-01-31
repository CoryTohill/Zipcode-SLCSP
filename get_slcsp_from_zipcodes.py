import csv


def read_csv(file_path):
    """
    Reads a csv file and returns a list of dictionaries where each dictionary represents a row in the csv file.
    The dictionary keys are the column names and the values are the row values.

    Args:
        file_path (str): The file path to the csv file to be read

    Returns:
        List: A list of dictionaries where each dictionary represents a row in the csv file
    """
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data


plans_file_path = 'plans.csv'
slcsps_file_path = 'slcsp.csv'
zips_file_path = 'zips.csv'


plan_data = read_csv(plans_file_path)
slcsp_data = read_csv(slcsps_file_path)
zipcode_data = read_csv(zips_file_path)
