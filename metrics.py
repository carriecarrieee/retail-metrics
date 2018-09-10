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

    data = pd.read_csv(url)
    df = pd.DataFrame(data) # Create DataFrame from CSV file
    
    if df.empty:
        print "No data found!"
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
    df['Total'] = df.groupby(['Retailer'])['Item Units'].transform('sum')

    # Sums up column of total drink units per brand and saves it as new df
    df = pd.DataFrame({'Drinks': df.groupby(['Retailer', 'Parent Brand', \
        'Total'])['Item Units'].sum()}).reset_index()

    # Add column of drinks per brand divided by total units per retailer
    df['Percentage %'] = df['Drinks'] / df['Total'] * 100

    # Create new df with a multiindex based on two columns
    df = df.set_index(['Retailer', 'Parent Brand'])

    # Query df to return cross-section of rows to show metrics by Retailer only
    by_brand = df.xs(focus_brand, level='Parent Brand')

    print by_brand.sortlevel(inplace=True)
    print by_brand['Percentage %'].idxmax()


retailer_affinity('Monster')

################################################################################
def count_hhs(brand=None, retailer=None, start_date=None, end_date=None):
    """Returns the number of households given any of the optional inputs."""
    
    pass

################################################################################
def top_buying_brand():
    """Identifies the brand with the top buying rate ($ spent / HH)."""
    
    pass


