import numpy as np
import time
import pika
import json
from matplotlib import pyplot as plt
from webcolors import (
    CSS3_HEX_TO_NAMES,
    hex_to_rgb,
    name_to_rgb,
)


def analysedata(a, b, c, d):
    colors = []
    colors_quantity = []
    filename = "json_data.json"
    path = "/share/"+filename

    with open(path) as f:
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


def init_connection(QUEUE):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE)
    return channel, connection


def send_signal(channel, connection):

    channel.basic_publish(exchange='', routing_key='analysis_completed',
                          body='<--analysis_completed | start recommendation-->')

    print(" [x] Sent : <--analysis_completed | start recommendation-->")
    connection.close()


def listen(channel, connection, QUEUE):
    channel.basic_consume(queue=QUEUE,
                          auto_ack=True,
                          on_message_callback=analysedata)

    channel.queue_declare(queue=QUEUE)
    print("Waiting for a signal ...")
    channel.start_consuming()


def main():
    print("Waiting for rabbitmq server start ...")
    time.sleep(7)
    global result
    print("Init new connection ...")
    result = init_connection('acquisition_completed')
    listen(result[0], result[1],'acquisition_completed')
    print("Init new connection ...")
    result = init_connection('analysis_completed')
    send_signal(result[0], result[1])


if __name__ == '__main__':
    main()
