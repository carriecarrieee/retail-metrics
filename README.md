# Retail Metrics
Retail Metrics provides three business intelligence metrics based off of retail transaction data of various energy drink brands.

### Data
The data includes rows of receipts where every receipt is processed and data is transcribed. Transcription data points include the store, transaction total, tax total, and each item purchased. These trips to the store for various energy drink brands were accessed through endpoints in CSV format (https://s3.amazonaws.com/isc-isc/trips_gdrive.cs). Each line belongs to a purchase at a retailer for a given parent brand, including total dollars for the item.

### Technology
This program was created in Python 2.7. It is optional to set up and activate a python virtual environment:
```python
virtualenv env
source env/bin/activate
```

Dependencies, listed in `requirements.txt`, include the numpy and pandas libraries. You can install this with:
```python
pip install -r requirements.txt
```

To run the program, run the following command:
```python
python metrics.py
```
