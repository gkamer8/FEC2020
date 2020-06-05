import requests
import json

# OPEN FEC API DOCS: https://api.open.fec.gov/developers/

base_url = "https://api.open.fec.gov/v1/"

# My API key 
api_key = "rcqremU3GbE0epC0132ZWY7ZXgfOCL7pD36Uspgh"

# Helper function for adding parameters to an API request
def make_params(my_dict):
    p_string = "?api_key=" + api_key
    for p in my_dict:
        p_string += "&" + p + "=" + my_dict[p]
    return p_string


# Returns JSON data (dictionary) of reports, given a committee and other specs
# Note: returns None if no reports found
def get_committee_reports(committee_id, extra_params=None):

    if extra_params is None:
        extra_params = dict()
    params = make_params(extra_params)
    url = base_url + "committee/" + committee_id + "/reports"
    page_string = requests.get(url + params).content.decode("utf-8")

    try:
        data = json.loads(page_string)['results']
    except IndexError:
        return None

    return data


# Prints the most recent cash on hand given a committee ID
# Takes optional other parameters specifying which filing to grab from
def print_cash_on_hand(committee_id, extra_params=None):

    data = get_committee_reports(committee_id, extra_params=extra_params)

    if data is None:
        print("No filings found.")
    else:
        cash_on_hand = data[0]['cash_on_hand_end_period']  # Goes for the first filing - hope it's right!
        cash_on_hand = round(cash_on_hand)  # Rounds to nearest dollar

        print('Cash: $' + '{:,}'.format(cash_on_hand))


# Interactive searching for a committee, returns committee ID
def query_for_committee():

    url = base_url + "names/committees/"

    q = input("Query for committee: ")
    response = requests.get(url + make_params({'q': q})).content.decode("utf-8")
    response_data = json.loads(response)['results']

    for i in range(len(response_data)):
        if response_data[i]['is_active']:  # Only shows active committees
            print(str(i) + ": " + response_data[i]['name'])

    choice = input("\nChoose committee ('q' for do-over): ")

    if choice == 'q':
        return query_for_committee()
    else:
        return response_data[int(choice)]['id']


# This part can be ignored – I typically run this file directly when working
if __name__ == "__main__":

    while True:

        print_cash_on_hand(query_for_committee(), extra_params={})

        stop = input("Stop? (y for exit): ")

        if stop == 'y':
            break



