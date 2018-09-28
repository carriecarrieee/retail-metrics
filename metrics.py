"""Retail Metrics provides three business intelligence metrics based off of 
   retail transaction data of various energy drink brands.
"""

import numpy as np
import pandas as pd


class Metrics:

    def __init__(self):
        self.df = None


    ############################################################################


    def get_df(self):
        """Creates a Panda DataFrame with transaction data."""
        
        # This tests to see if df was already created; if not, the program will
        # download and parse the data, and create a df. If a df already exists,
        # the else block simply returns the df.
        if not self.df:
            
            # Test data of first 100 rows: 
            # url = "data/transactions.head.csv"

            # Trips to the store for various energy drink brands in CSV format.
            # Each line belongs to a purchase at a retailer for a given parent 
            # brand, including total dollars for the item.
            url = "https://s3.amazonaws.com/isc-isc/trips_gdrive.csv"

            try:
                self.data = pd.read_csv(url, parse_dates=['Date'], \
                                             infer_datetime_format=True)

                # Create DataFrame from CSV file
                self.df = pd.DataFrame(self.data)
                return self.df

            except:
                print "Error: No data found!"

        else:
            return self.df


    ############################################################################


    def retailer_affinity(self, focus_brand):
        """Returns the strongest retailer affinity of focus brand relative to other 
           brands. We will define retailer affinity by the retailer that sells the
           highest percentage of the focus brand out of total units sold by that
           retailer.

           Test:

           >>> myMetrics = Metrics()
           >>> myMetrics.retailer_affinity('Monster')
           'CVS'

           >>> myMetrics.retailer_affinity('Red Bull')
           'Publix'

           >>> myMetrics.retailer_affinity('Rockstar')
           'Walgreens'

           >>> myMetrics.retailer_affinity('5 Hour Energy')
           'CVS'

        """
        
        df = Metrics().get_df()

        # Add column of total drink units per retailer to perform math 
        df['Total by Ret'] = df.groupby(['Retailer'])['Item Units'].transform('sum')

        # Sum up column of total drink units per brand
        df = df.groupby(['Retailer', 'Parent Brand', 'Total by Ret']) \
            ['Item Units'].sum().reset_index()

        # Add column of drinks per brand divided by total units per retailer
        df['Percentage %'] = df['Item Units'] / df['Total by Ret'] * 100

        # Create and query multiindex based on two columns in new df, then sort
        df = df.set_index(['Retailer', 'Parent Brand']) \
               .xs(focus_brand, level='Parent Brand')

        # Return the retailer with the highest percentage.
        return df[df['Percentage %'] == df['Percentage %'].max()].index[0]


    ############################################################################


    def count_hhs(self, brand=None, retailer=None, start_date=None, end_date=None):
        """Returns the number of households given any of the optional inputs.

           Test:

            >>> myMetrics = Metrics()
            >>> myMetrics.count_hhs(start_date='2014-01-01', end_date='2014-02-01')
            2488
            
            >>> myMetrics.count_hhs(retailer='CVS')
            715

            >>> myMetrics.count_hhs(start_date='2014-01-01', brand='Rockstar')
            2312

            >>> myMetrics.count_hhs(end_date='2014-02-01', brand='Monster', retailer='Walmart')
            506

            >>> myMetrics.count_hhs(start_date='2014-01-01', end_date='2014-02-01', brand='5 Hour Energy', retailer='Publix')
            10

        """
        
        # Prepare df for date manipulation; 'Date' column is now the index
        df = Metrics().get_df().set_index(['Date']).sort_index()

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

        
        # Multiple keys to .get_group() must be passed through as a tuple.
        # Since tuples with one item include a trailing comma i.e. (key,)
        # this code ensures that a tuple of one item will simply show (key)
        else:
            if len(params) < 2:
                args = params[0]
            else:
                args = tuple(params) # Convert to tuple to pass into get_group()


            df = df.groupby(columns) # Group by current list of parameters
            newdf = df['Retailer','Parent Brand','User ID'].get_group(args)

        # Count number of unique User IDs from the final newdf
        return newdf['User ID'].nunique()


    ############################################################################


    def top_buying_brand(self):
        """Identifies the brand with the top buying rate ($ spent / HH).

           Test:

           >>> myMetrics = Metrics()
           >>> myMetrics.top_buying_brand()
           'Rockstar'

        """
        
        df = Metrics().get_df()

        # Convert string obj to int type
        df['Item Dollars'] = df['Item Dollars'].str[1:].astype(int)

        # Sum up $ spent by each unique household ID
        df = df.groupby(['Parent Brand','User ID'])['Item Dollars'] \
            .sum() \
            .reset_index() \
            .set_index(['Parent Brand'])

        # Brand with the top buying rate ($ spent / HH):"
        return df[df['Item Dollars'] == df['Item Dollars'].max()].index[0]


    ############################################################################


    def main(self):
        """Takes user input and calls the appropriate function."""

        input = raw_input("\nWhich metric would you like to see?\n\n \
            a) Retailer Affinity \n \
            b) Number of Households \n \
            c) Top Buying Brand\n")

        if input == 'a':
            brand = raw_input("\nEnter an energy drink brand: \n \
                5 Hour Energy \n \
                Monster \n \
                Red Bull \n \
                Rockstar\n")

            return Metrics().retailer_affinity(brand)


        elif input == 'b':
            ans1 = raw_input("\nSelect energy drink brand? y/n: \n")
            if ans1 == 'Y':
                brand = raw_input("Enter an energy drink brand: \n \
                    5 Hour Energy \n \
                    Monster \n \
                    Red Bull \n \
                    Rockstar\n")
            else:
                brand = None

            ans2 = raw_input("\nSelect a retailer? y/n: \n")
            if ans2 == 'y':
                retailer = raw_input("Enter a retailer: \n \
                    Costco \n \
                    CVS \n \
                    Kroger \n \
                    Publix \n \
                    Target \n \
                    Walgreens \n \
                    Walmart \n")
            else:
                retailer = None

            ans3 = raw_input("\nWould you like to enter a start date? y/n: \n")
            if ans3 == 'y':
                start_date = raw_input("Enter a start date (YYYY-MM-DD): \n")
            else:
                start_date = None

            ans4 = raw_input("\nWould you like to enter an end date? y/n: \n")
            if ans4 == 'y':
                end_date = raw_input("Enter an end date (YYYY-MM-DD): \n")
            else:
                end_date = None

            return Metrics().count_hhs( \
                            brand=brand, \
                            retailer=retailer, \
                            start_date=start_date, \
                            end_date=end_date)

        
        elif input == 'c':
            return Metrics().top_buying_brand()

        else:
            raise Exception("Invalid input. Please enter only A, B, or C.\n")


################################################################################


if __name__ == "__main__":
    import doctest

    result = doctest.testmod()
    if result.failed == 0:
        print "ALL TESTS PASSED"
