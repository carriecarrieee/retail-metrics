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

def retailer_total_units():
    """Returns the total units sold of an energy drink at a given retailer."""

    df = create_df()
    #store = df['Item Units'][df['Retailer'] == store]
    #store_units = store.sum()
    #drink_units_by_store = store[df['Parent Brand']].sum()

    # print store_units, drink_units_by_store
    #items = df.groupby(['Retailer'])['Item Units'].sum()
    #grouped = df.groupby(['Retailer', 'Parent Brand'])['Item Units']
    #df_drinks = grouped.sum()

    df['Total'] = df.groupby(['Retailer'])['Item Units'].transform('sum')

    df = pd.DataFrame({'Drinks': df.groupby(['Retailer', 'Parent Brand', \
        'Total'])['Item Units'].sum()}).reset_index()
    df['Percentage %'] = df['Drinks'] / df['Total'] * 100
    df = df.set_index(['Retailer', 'Parent Brand'])

    print df
    by_brand = df.xs('Red Bull', level='Parent Brand')

    print by_brand
    print by_brand['Percentage %'].idxmax()
    

retailer_total_units()





def retailer_affinity(focus_brand):
    """Returns the strongest retailer affinity of focus brand relative to other 
       brands. We will define retailer affinity by the retailer that sells the
       highest percentage of the focus brand out of total units sold by that
       retailer."""
    
    pass




################################################################################
def count_hhs(brand=None, retailer=None, start_date=None, end_date=None):
    """Returns the number of households given any of the optional inputs."""
    
    pass

################################################################################
def top_buying_brand():
    """Identifies the brand with the top buying rate ($ spent / HH)."""
    
    pass


