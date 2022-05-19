# import opendatasets as od
import os
# os.environ['KAGGLE_USERNAME'] = 'verniereloic'
# os.environ['KAGGLE_KEY'] = '03e78f24e94d43d80b595934fc372ecf'
from kaggle.api.kaggle_api_extended import KaggleApi

dataset = 'ayklovettc/images-with-exif'
path = './'

api = KaggleApi()
api.authenticate()

api.dataset_download_files(dataset, path,  unzip=True)

# username = "verniereloic"
# key = "03e78f24e94d43d80b595934fc372ecf"

# od.download("https://www.kaggle.com/ayklovettc/images-with-exif")
