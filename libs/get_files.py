import io
import zipfile
import requests
import pandas as pd


def get_file_to_df(url):
    r = requests.get(url)  # GET request
    mlz = zipfile.ZipFile(io.BytesIO(r.content))  # Get zip object

    # Convert first element of zip object to pd.DataFrame
    df = pd.read_csv(mlz.open(mlz.namelist()[0]), sep=";", low_memory=False)
    return df
