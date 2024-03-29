# Docker stack - Python data analysis

## 

## Containers

### tdm_download
- Running download.py, the code is in charge to connect to the Kaggle API and download a dataset

### tdm_acquisition
- Running acquisition.py, the code will extract data from the images of the dataset previously downloaded and save it in json file

### tdm_analysis
- Running analysis.py, in charge to create graphs about the extracted data

### tdm_recommendation
- Running recommendation.py, Building a list of the favorite images in the dataset to simulate user preferences and return suggestions

### tdm_rabbitmg
- Container that run a rabbitmg server to use python message broker between all the containers

### tdm_notebooklab
- Container that run a jupyter notebook lab to see the graph generated by analysis step

## Volumes

- shared-data:/share

To share the images and the json generated by the analysis code, I decided de to create a volume named **images-data** binded on **/share** on all the containers

## Network

- I created a new network named net_common for the communication between all the containers


## Run the stack 

```bash
# Clone the project
git clone https://github.com/VERNIERELoic/python-dataanalysis.git
# Move into project folder
cd python-dataanalysis/Partie\ 2\ -\ Docker-map-reduce/
# Create net_common network
docker network create net_common
# debug run :
docker-compose up --build
# Prod run : 
docker-compose up -d --force-recreate
```