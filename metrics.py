"""Retail Metrics provides three business intelligence metrics based off of 
   retail transaction data of various energy drink brands."""

import numpy as np
import pandas as pd


def create_df():
    """Creates a Panda DataFrame with transaction data."""

    # Trips to the store for various energy drink brands in CSV format.
    # Each line belongs to a purchase at a retailer for a given parent brand,
    # including total dollars for the item.
    # url = "https://s3.amazonaws.com/isc-isc/trips_gdrive.csv"

    # Using only the first 100 rows of data to save run time.
    url = "data/transactions.head.csv"

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

# retailer_affinity('Monster')
# retailer_affinity('Red Bull')
# retailer_affinity('Rockstar')
# retailer_affinity('5 Hour Energy')

################################################################################


def count_hhs(brand=None, retailer=None, start_date=None, end_date=None):
    """Returns the number of households given any of the optional inputs."""
    
    df = create_df()
    columns = []
    args = ""


    if brand:
        columns = ['Parent Brand']
        args = brand

        if retailer:
            columns = ['Parent Brand','Retailer']
            args = (brand, retailer)

            if start_date:
                columns = ['Parent Brand','Retailer','Date']
                args = (brand, retailer, date)

    elif retailer:
        columns = ['Retailer']
        args = retailer

        if brand:
            columns = ['Retailer','Parent Brand']
            args = (retailer, brand)

            if start_date:
                columns = ['Retailer','Parent Brand','Date']
                args = (retailer, brand, date)

    elif start_date:
        columns = ['Date']
        args = date



    elif end_date:
        print "well this shouldn't print"

    
    if not columns or not args:
        newdf = df
    else:   
        df = df.groupby(columns)
        newdf = df['Date','Retailer','Parent Brand','User ID'].get_group(args)


    print newdf['User ID'].nunique()
    print "\n\n"



    # There are 93 total unique user IDs.
    # Outline: 
    # Create series of "if" statements to see if each argument is given.
    # (Don't use switch/case here.)
    # Inside each if block, modify df according to that ONE parameter.
    # At the end of all the if blocks, the final df should have the data in the
    # way we want it, and so we can simply call .nunique() on the Series.
    # Next: work on the Datetime object.

count_hhs(brand='5 Hour Energy')

################################################################################


def top_buying_brand():
    """Identifies the brand with the top buying rate ($ spent / HH)."""
    
    df = create_df()

    # print df.types

    # Convert string obj to int type
    df['Item Dollars'] = df['Item Dollars'].str[1:].astype(int)

    # Sum up $ spent by each unique household ID
    df = df.groupby(['Parent Brand', 'User ID'])['Item Dollars'].sum().reset_index()

    print "\n" + "Brand with the top buying rate ($ spent / HH):" + "\n"
    print df[df['Item Dollars'] == df['Item Dollars'].max()]

# top_buying_brand()


