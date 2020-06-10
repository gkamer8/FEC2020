# FEC2020

In working for a political campaign, it is sometimes advantageous to automate  tasks related to the FEC. These tasks may include exploring campaign data, like other candidates' cash on hand, or summarizing how other campaigns are raising money. This repository contains some ad-hoc functions for examining campaign finance data using the FEC's API.

The functionality is all in fec2020.py 

## Finding a Committee ID

The FEC API is easier to use if you know the committee ID for a candidate's campaign or victory fund. The function query_for_committee allows a user to input data to put in the FEC's query function to find a committee and then select the right committee. The function then returns the committee ID.

## Getting Cash on Hand

The print_cash_on_hand function takes in a committee ID and prints the most recent cash on hand value for the committee. It also takes optional extra paramters (extra_params) to add to the filing query – say, if you want a filing only if it's from a particular quarter.

## Reviewing Contributions and Disbursements

The print_filing_summary function allows for viewing a summary of financial documents like quarterlies and pre-primaries. They give a link to the documents and print out contribution, disbursement, and cash on hand figures. Using the optional paramter as a store for a filename, you can write the total contributions and disbursements of the viewed file(s) straight to a CSV, adding to the previous lines.