import os
import pika
import time
import PIL.Image
from PIL import Image
from PIL.ExifTags import TAGS
#from __future__ import print_function
import binascii
import scipy
import scipy.misc
import scipy.cluster
import numpy as np
import json
from PIL import Image
import math
import matplotlib.pyplot as plot
from sklearn.cluster import KMeans
from scipy.spatial import KDTree
from webcolors import (
    CSS3_HEX_TO_NAMES,
    hex_to_rgb,
    name_to_rgb,
)

result = 0
connection = 0

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def convert_rgb_to_names(rgb_tuple):

    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))

    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return f'{names[index]}'


def find_color(a, b, c, d):
    NUM_CLUSTERS = 5
    path = "/share/Images/"
    folders = os.listdir(path)
    categories = []
    data = []
    cpt = 0
    print("analysing images...")
    for folder in folders:
        categories.append(folder)
        for image in os.listdir(path + folder):
            cpt = cpt + 1
            if image.endswith((".jpg", ".png")):
                img = Image.open(path + folder + "/" + image)
                # To converte all image to RGB image and resize to 150*150
                img = img.resize((150, 150)).convert("RGB")
                img = img.convert("RGB")
                ar = np.asarray(img)
                shape = ar.shape
                ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)
                codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
                vecs, dist = scipy.cluster.vq.vq(
                    ar, codes)         # assign codes
                counts, bins = np.histogram(
                    vecs, len(codes))    # count occurrences
                index_max = np.argmax(counts)  # find most frequent
                peak = codes[index_max]
                colour = binascii.hexlify(
                    bytearray(int(c)for c in peak)).decode('ascii')
                # print('Most frequent is %s (#%s)' % (peak, colour))
                colour_name = convert_rgb_to_names(hex_to_rgb(colour))
                el = {
                    'path': image,
                    'Id': cpt,
                    'Category': folder,
                    'Color': colour_name,
                    'size': img.size
                }

                data.append(el)

    print("Saving in jsons...")
    with open('/share/json_data.json', 'w+') as outfile:
        outfile.write(json.dumps(data, indent=4))
        # outfile.write(",")
        outfile.close()
    
    send_signal(result[0], result[1])



def init_connection(QUEUE):
    global connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE)
    return channel, connection


def send_signal(channel, connection):

    channel.basic_publish(exchange='', routing_key='acquisition_completed',
                          body='<--acquisition completed | start recommendation-->')

    print(" [x] Sent : <--acquisition completed | start recommendation-->")
    connection.close()


def listen(channel, connection, QUEUE):
    channel.basic_consume(queue=QUEUE,
                          auto_ack=True,
                          on_message_callback=find_color)

    channel.queue_declare(queue=QUEUE)
    print("Waiting for a signal ...")
    channel.start_consuming()


def main():
    print("Waiting for rabbitmq server start ...")
    time.sleep(7)
    global result
    print("Init new connection to received message...")
    result = init_connection('download_completed')
    listen(result[0], result[1],'download_completed')
    print("Init new connection for sending message...")
    result = init_connection('acquisition_completed')
    print("connection ok")
    send_signal(result[0], result[1])

    time.sleep(1000)

if __name__ == '__main__':
    main()
