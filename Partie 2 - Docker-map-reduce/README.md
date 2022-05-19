# Docker stack - Python data analysis

## Containers

### tdm_download
Running download.py, the code is in charge to connect to the Kaggle API and download a dataset

### tdm_acquisition
Running acquisition.py, the code will extract data from the images of the dataset previously downloaded and save it in json file

### tdm_analysis
Running analysis.py, in charge to create graphs about the extracted data

### tdm_recommendation
Running recommendation.py, Building a list of the favorite images in the dataset to simulate user preferences and return suggestions

### rabbitmg
Container that run a rabbitmg server to use python message broker between all the containers

## Run the stack 

```bash
cd python-dataanalysis/
#Test build for debug :
docker-compose up --build
#Standar:
docker-compose up -d --force-recreate
```