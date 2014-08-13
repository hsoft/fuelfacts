# Read zipped JSON file supplied by EIA (http://www.eia.gov).
import os.path as op
import zipfile
import json
from urllib.request import urlretrieve

EIA_URL_PATTERN = 'http://api.eia.gov/bulk/{}.zip'

def load_series(api_id, serie_ids):
    zip_name = '{}.zip'.format(api_id)
    if not op.exists(zip_name):
        url = EIA_URL_PATTERN.format(api_id)
        print("Downloading EIA series file from {}. Might take a while...".format(url))
        urlretrieve(url, zip_name)
        print("Done!")
    result = []
    with zipfile.ZipFile(zip_name) as z:
        contents = z.read('PET.txt').decode('utf-8')
    for serie_id in serie_ids:
        linestart = '{"series_id":"' + serie_id
        start = contents.index(linestart)
        end = contents.index('\n', start)
        result.append(json.loads(contents[start:end]))
    return result

