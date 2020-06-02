# FEC2020

In working for a political campaign, it is sometimes advantageous to automate certain tasks relating to the FEC. Part of this is exploration of campaign data, like other candidates' cash on hand, or summarizing how other campaigns are raising money. This repository contains some ad-hoc functions for examining FEC data using their API.

The functionality is all in main.py 

## Finding a Committee ID

The FEC API is easier to use if you know the committee ID for a candidate's campaign or victory fund. The function query_for_committee allows a user to input data to put in the FEC's query function to find a committee and then select the right committee. The function then returns the committee ID.

## Getting Cash on Hand

The print_cash_on_hand function takes in a committee ID and prints the most recent cash on hand value for the committee. It also takes optional extra paramters (extra_params) to add to the filing query – say, if you want a filing only if it's from a particular quarter.