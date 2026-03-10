import pandas as pd

#fix from https://github.com/lezandar/flights
def clean(file):

    flights = pd.read_csv(file, low_memory=False)

    aircode1 = pd.read_csv('data/L_AIRPORT.csv')
    aircode2 = pd.read_csv('data/L_AIRPORT_ID.csv')

    # Format the airport codes
    aircode1 = aircode1.reset_index()
    aircode2 = aircode2.reset_index()

    aircodes = pd.merge(aircode1,aircode2,on='Description')
    aircode_dict = dict(zip(aircodes['Code_y'].astype(str),aircodes['Code_x']))

    # Make sure all Origin and departing airports are strings
    flights['ORIGIN_AIRPORT'] = flights['ORIGIN_AIRPORT'].values.astype(str)
    flights['DESTINATION_AIRPORT'] = flights['DESTINATION_AIRPORT'].values.astype(str)

    for i in range(len(flights)):
        if len(flights['ORIGIN_AIRPORT'][i]) != 3:
            to_replace = flights['ORIGIN_AIRPORT'][i]
            value = aircode_dict[flights['ORIGIN_AIRPORT'][i]]
            flights = flights.replace(to_replace, value)

    for i in range(len(flights)):
        if len(flights['DESTINATION_AIRPORT'][i]) != 3:
            to_replace = flights['DESTINATION_AIRPORT'][i]
            value = aircode_dict[flights['DESTINATION_AIRPORT'][i]]
            flights = flights.replace(to_replace, value)

    flights_filtered_bsm = flights[
        (flights['ORIGIN_AIRPORT'] != 'BSM') &
        (flights['DESTINATION_AIRPORT'] != 'BSM')
    ]

    flights_filtered_bsm.to_csv('data/flights_filtered_fixed.csv', index=False)

    return