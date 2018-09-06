"""Retail Metrics provides three business intelligence metrics based off of 
   retail transaction data."""

import requests

import numpy as np

import pandas as pd


def get_data():
    """Requests and accesses data from an API endpoint, and returns a python
       list of dictionaries."""

    # Trips to the store for various energy drink brands in JSON format.
    # Each line belongs to a purchase at a retailer for a given parent brand,
    # including total dollars for the item.
    url = "https://s3.amazonaws.com/isc-isc/trips_gdrive.json"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json() # Converts json to a list of dictionaries
        print "get_data() successful!"
        return data
    else:
        print "{} {}".format("Request failed; response code:", response.status_code)



def retailer_affinity(focus_brand):
    """Returns the strongest retailer affinity of focus brand relative to other brands."""
    pass


def count_hhs(brand=None, retailer=None, start_date=None, end_date=None):
    """Returns the number of households given any of the optional inputs."""
    pass


def top_buying_brand():
    """Identifies the brand with the top buying rate ($ spent / HH)."""
    pass


