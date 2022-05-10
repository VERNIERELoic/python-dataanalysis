import opendatasets as od
import os
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


def find_color(NUM_CLUSTERS):

    path = "Images/"
    folders = os.listdir("Images")
    categories = []
    data = []
    cpt = 0

    for folder in folders:
        categories.append(folder)
        for image in os.listdir(path + folder):
            cpt = cpt + 1
            if image.endswith((".jpg",".png")):
                img = Image.open(path + folder + "/" + image)
                #img = img.resize((150, 150)).convert("RGB") #To converte all image to RGB image and resize to 150*150
                img = img.convert("RGB")
                ar = np.asarray(img)
                shape = ar.shape
                ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)
                codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
                vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
                counts, bins = np.histogram(vecs, len(codes))    # count occurrences
                index_max = np.argmax(counts) # find most frequent
                peak = codes[index_max]
                colour = binascii.hexlify(bytearray(int(c)for c in peak)).decode('ascii')
                #print('Most frequent is %s (#%s)' % (peak, colour))
                colour_name = convert_rgb_to_names(hex_to_rgb(colour))
                el = {
                  'path' : image,
                  'Id': cpt,
                  'Category': folder, 
                  'Color': colour_name,
                  'size' : img.size
                }

                data.append(el)
    
    with open('json_data.json', 'w+') as outfile:
        outfile.write(json.dumps(data, indent=4))
        #outfile.write(",")
        outfile.close()

find_color(5)