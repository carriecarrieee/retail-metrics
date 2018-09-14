"""Retail Metrics provides three business intelligence metrics based off of 
   retail transaction data of various energy drink brands."""

import numpy as np
import pandas as pd


def create_df():
    """Creates a Panda DataFrame with transaction data."""

    # Trips to the store for various energy drink brands in CSV format.
    # Each line belongs to a purchase at a retailer for a given parent brand,
    # including total dollars for the item.
    url = "https://s3.amazonaws.com/isc-isc/trips_gdrive.csv"

    # Test data of first 100 rows: url = "data/transactions.head.csv"

    data = pd.read_csv(url, parse_dates=['Date'], infer_datetime_format=True)
    df = pd.DataFrame(data) # Create DataFrame from CSV file
    
    if df.empty:
        print "Error: No data found!"
    else:
        return df


################################################################################


def retailer_affinity(focus_brand):
    """Returns the strongest retailer affinity of focus brand relative to other 
       brands. We will define retailer affinity by the retailer that sells the
       highest percentage of the focus brand out of total units sold by that
       retailer."""
    
    df = create_df()

    # Add column of total drink units per retailer to perform math 
    df['Total by Ret'] = df.groupby(['Retailer'])['Item Units'].transform('sum')

    # Sum up column of total drink units per brand
    df = df.groupby(['Retailer', 'Parent Brand', 'Total by Ret']) \
        ['Item Units'].sum().reset_index()

    # Add column of drinks per brand divided by total units per retailer
    df['Percentage %'] = df['Item Units'] / df['Total by Ret'] * 100

    # Create and query multiindex based on two columns in new df
    df = df.set_index(['Retailer', 'Parent Brand']).xs(focus_brand, level='Parent Brand')

    # Print row(s) with highest percentage, showing strongest retailer affinity
    print "\n" + focus_brand + ":\n"
    print df[df['Percentage %'] == df['Percentage %'].max()]
    print "\n"

    raw_input("Press 'Enter' to see all the retailers for " + focus_brand + ".\n\n")

    print df.sort_values(by='Percentage %', ascending=False)
    print "\n\n"


################################################################################


def count_hhs(brand=None, retailer=None, start_date=None, end_date=None):
    """Returns the number of households given any of the optional inputs."""
    
    # Prepare df for date manipulation; 'Date' column is now the index
    df = create_df().set_index(['Date']).sort_index()

    columns = []
    params = []

    # Considering if each input was given
    if brand:
        columns.append('Parent Brand')
        params.append(brand)

    if retailer:
        columns.append('Retailer')
        params.append(retailer)

    if start_date:
        start_date = pd.to_datetime(start_date, infer_datetime_format=True)
        df = df.loc[start_date:]

    if end_date:
        end_date = pd.to_datetime(end_date, infer_datetime_format=True)
        df = df.loc[:end_date]


    if not columns or not params: # Case for empty lists
        newdf = df

    else:
        if len(params) < 2: # Since tuples w/ one item have a trailing comma
            args = params[0]
        else:
            args = tuple(params) # Convert to tuple to pass into get_group()


        df = df.groupby(columns) # Group by current list of parameters
        newdf = df['Retailer','Parent Brand','User ID'].get_group(args)

    # Count number of unique User IDs from the final newdf
    hhs = newdf['User ID'].nunique()

    print "\nGiven the parameter(s), the number of unique household(s) is: {}.".format(hhs)
    raw_input("\n\nPress 'Enter' to see the expanded results:\n\n")

    print newdf
    print "\n\n"


################################################################################


def top_buying_brand():
    """Identifies the brand with the top buying rate ($ spent / HH)."""
    
    df = create_df()

    # Convert string obj to int type
    df['Item Dollars'] = df['Item Dollars'].str[1:].astype(int)

    # Sum up $ spent by each unique household ID
    df = df.groupby(['Parent Brand','User ID'])['Item Dollars'] \
        .sum() \
        .reset_index() \
        .set_index(['Parent Brand'])

    print "\n" + "Brand with the top buying rate ($ spent / HH):" + "\n"
    print df[df['Item Dollars'] == df['Item Dollars'].max()]
    print "\n\n"


################################################################################