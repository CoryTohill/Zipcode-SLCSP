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

for zip_data in filtered_zipcode_data:
    # Using a set instead of a list here to deduplicate any rate areas that are the same
    zipcode_rate_areas.setdefault(zip_data['zipcode'], set()).add((zip_data['state'], zip_data['rate_area']))


# Filter the plan data to only include the plans needed based on the rate areas
rate_areas_needed = [(zip_row['state'], zip_row['rate_area']) for zip_row in filtered_zipcode_data]
filtered_plan_data = [plan for plan in plan_data if plan['metal_level'] == 'Silver' and (plan['state'], plan['rate_area']) in rate_areas_needed]


# Create a dictionary where the keys are the zipcodes
# and the values are the SLCSP if that exists
zipcode_rates = {}

for zipcode, rate_areas in zipcode_rate_areas.items():
    # If there are multiple rate areas for a zipcode, the SLCSP is not available
    if len(rate_areas) > 1:
        zipcode_rates[zipcode] = None
    else:
        state, rate_area = rate_areas.pop()
        plans = [plan for plan in filtered_plan_data if plan['state'] == state and plan['rate_area'] == rate_area]
        # Using a set to deduplicate any rates that are the same
        rates = set(float(plan['rate']) for plan in plans)
        rates = list(rates)
        rates.sort()
        # If there are less than 2 rates, the SLCSP is not available
        if len(rates) < 2:
            zipcode_rates[zipcode] = None
        else:
            zipcode_rates[zipcode] = rates[1]


# Print the results in the order determined in the zips.csv file with 2 digits after the decimal point
print('zipcode,rate')
for zipcode in zipcodes_needed:
    slcsp = f'{zipcode_rates[zipcode]:.2f}' if zipcode_rates[zipcode] else ''
    print(f'{zipcode},{slcsp}')
