# import opendatasets as od
import os
import time
import pika
from kaggle.api.kaggle_api_extended import KaggleApi


def download():
    dataset = 'ayklovettc/images-with-exif'
    path = '/share'

    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset, path,  unzip=True)
    time.sleep(5)



def init_connection():
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))

    channel = connection.channel()
    channel.queue_declare(queue='download_completed')
    return channel, connection

def start(channel, connection):

    channel.basic_publish(exchange='', routing_key='download_completed',
                          body='<--download completed | start acquisition-->')

    print(" [x] Sent : <--download completed | start acquisition-->")
    connection.close()


def main():
    print("Waiting for rabbitmq server start ...")
    time.sleep(7)
    result = init_connection()
    download()
    print("Waiting for download completed...")
    while not os.path.exists("/share/Images/star"):
        time.sleep(1)
        print("waiting in loop...")
    print("download completed !")
    start(result[0], result[1])
    time.sleep(10000)


if __name__ == "__main__":
    main()
