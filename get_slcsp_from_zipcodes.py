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


# Filter the zipcode data to only include the zipcodes needed
zipcodes_needed = [slcsp['zipcode'] for slcsp in slcsp_data]
filtered_zipcode_data = [zip_row for zip_row in zipcode_data if zip_row['zipcode'] in zipcodes_needed]


# Create a dictionary where the keys are the zipcodes
# and the values are a set of tuples which contain the state and rate area number
zipcode_rate_areas = {}

for zid_data in filtered_zipcode_data:
    zipcode_rate_areas.setdefault(zid_data['zipcode'], set()).add((zid_data['state'], zid_data['rate_area']))
