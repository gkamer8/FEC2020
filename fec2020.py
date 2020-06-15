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
    url = base_url + "committee/" + committee_id + "/reports" + params
    page_string = requests.get(url).content.decode("utf-8")

    data = json.loads(page_string)['results']

    if len(data) == 0:
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


# Like print cash on hand but prints a larger summary of the filing
# Handles multiple filings and combines contributions and disbursements at end
# Optional write paramters stores a filename to give the option of writing the total contributions/disbursements to
def print_filing_summary(committee_id, extra_params=None, write_option=None):
    data = get_committee_reports(committee_id, extra_params=extra_params)

    if data is None:
        print("No filings found.")
    else:
        total_cont = 0
        total_disb = 0

        for first in data:
            print("\n")
            try:
                cash_on_hand = round(first['cash_on_hand_end_period'])
                contributions = round(first['total_contributions_period'])
                spending = round(first['total_disbursements_period'])

                total_cont += int(contributions)
                total_disb += int(spending)

                # For checking that it's the right thing
                desc = first['document_description']
                year = first['report_year']
                html_url = first['html_url']

                print("Doc: " + desc)
                print("Year: " + str(year))
                print("URL: " + html_url + "\n")
                print('Contributions: $' + '{:,}'.format(contributions))
                print('Disbursements: $' + '{:,}'.format(spending))
                print('Cash on hand: $' + '{:,}'.format(cash_on_hand))
            except KeyError:
                desc = first['document_description']
                year = first['report_year']
                html_url = first['html_url']
                print("<Does not have contributions or disbursements")
        
        print("\nTotals")
        print('Contributions: $' + '{:,}'.format(total_cont))
        print('Disbursements: $' + '{:,}'.format(total_disb))

        if write_option is not None:
            write = input("Write? (w/n): ")
            if write == 'w':
                try: 
                    fhand = open(write_option, "r")
                    old = fhand.read()
                    fhand.close()
                except FileNotFoundError:
                    old = ""
                    pass

                fhand = open(write_option, "w")
                # Uses committee name from first filing, whatever that is
                new_write = str(data[0]['committee_name']).replace(",", "") + "," + str(total_cont) + "," + str(total_disb) + "\n"
                fhand.write(old + new_write)
                fhand.close()



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

        params = {
            'year': '2020',
            'is_amended': 'False',
        }

        print_filing_summary(query_for_committee(), extra_params=params, write_option="guns2.csv")

        stop = input("Stop? (y for exit): ")

        if stop == 'y':
            break
    



