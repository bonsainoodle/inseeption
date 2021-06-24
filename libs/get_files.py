import sys
import io
import time
import zipfile
import requests
import pandas as pd
from tqdm import tqdm


def get_file_to_df(url):
    fname = url.split("/")[-1]
    
    print("\nDownloading %s" % fname)
    
    try:
        resp = requests.get(url, stream=True)
    except Exception as e:
        print("Error: %s" % e)
        print("Retrying in 2 seconds...")
        time.sleep(2)
        get_file_to_df(url)
        
    # total = int(resp.headers.get('content-length', 0))
    total = len(resp.content)
    
    output = b""
    io.BytesIO().seek(0)
    
    with tqdm(
        desc=fname,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            output += data
            bar.update(1024)
    mlz = zipfile.ZipFile(io.BytesIO(output)) # Get zip object

    # Convert first element of zip object to pd.DataFrame
    df = pd.read_csv(mlz.open(mlz.namelist()[0]), sep=";", low_memory=False)
    return df
