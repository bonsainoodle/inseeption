import sys
import io
import time
import zipfile
import requests
import pandas as pd
from tqdm import tqdm


def get_file_to_df(url):
    """
    Gets the csv file of a zip object through a request

            Parameters:
                    url (string): Direct url of the zipfile that contains the csv

            Returns:
                    df (pd.DataFrame): DataFrame object of the csv file
    """
    
    fname = url.split("/")[-1]
    
    print("Downloading %s" % fname)
    
    try:
        resp = requests.get(url, stream=True) # Stream must be set to True since we are continuously getting the data 
    except Exception as e:
        print("Error: %s" % e)
        print("Retrying in 5 seconds...")
        time.sleep(5)
        get_file_to_df(url)

    total = len(resp.content)
    
    # Init the bytes object 
    output = b""
    io.BytesIO().seek(0)
    
    # Create the progress bar
    with tqdm(
        desc=fname,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            output += data # Allows to store zipfile in buffer
            bar.update(1024)
    mlz = zipfile.ZipFile(io.BytesIO(output)) # Get zip object
    
    df = pd.read_csv(mlz.open(mlz.namelist()[0]), sep=";", low_memory=False) # Convert first element of zip object to pd.DataFrame
    print("\n")
    return df
