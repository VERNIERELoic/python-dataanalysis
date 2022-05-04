import numpy as np
from matplotlib import pyplot as plt
from webcolors import (
    CSS3_HEX_TO_NAMES,
    hex_to_rgb,
    name_to_rgb,
)

def analysedata(filename):
    colors = []
    colors_quantity = []

    with open(filename) as f:
        datajs = json.load(f)
        for row in datajs:
            colors.append(row.get('Color'))

    for line in colors:
        nbr_colors = colors.count(line)
        colors_quantity.append(nbr_colors)  # , line
    
    plt.title("Data analyse colors")
    names = []
    for i in colors:
        names.append(name_to_rgb(i))

    plt.bar(colors, colors_quantity, color=colors, align='center')
    plt.ylabel('Quantity')
    plt.xlabel('Color')


analysedata('json_data.json')