from sklearn import tree
import time
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import json
import pika


def prediction(a,b,c,d):
    data = []
    path = "/share/json_data.json"
    with open(path) as f:
        datajs = json.load(f)
        for index in range(0, 26, 2):
            value = datajs[index]
            val = [value["Category"], value["Color"]]  # ,value["size"]
            data.append(val)

        print(data)

    result = [
        'Favorite',
        'NotFavorite',
        'Favorite',
        'Favorite',
        'Favorite',
        'Favorite',
        'Favorite',
        'NotFavorite',
        'NotFavorite',
        'Favorite',
        'Favorite',
        'NotFavorite',
        'NotFavorite'
    ]

    # creating dataframes
    dataframe = pd.DataFrame(data, columns=['category', 'color'])
    resultframe = pd.DataFrame(result, columns=['favorite'])

    # generating numerical labels
    le1 = LabelEncoder()
    dataframe['category'] = le1.fit_transform(dataframe['category'])

    le2 = LabelEncoder()
    dataframe['color'] = le2.fit_transform(dataframe['color'])

    le3 = LabelEncoder()
    resultframe['favorite'] = le3.fit_transform(resultframe['favorite'])

    # Use of decision tree classifiers
    dtc = tree.DecisionTreeClassifier()
    dtc = dtc.fit(dataframe, resultframe)

    # prediction
    prediction = dtc.predict(
        [[le1.transform(['airplane'])[0], le2.transform(['black'])[0]]])

    print(le3.inverse_transform(prediction))
    print(dtc.feature_importances_)
    print("prediction finihed ...")




def init_connection(QUEUE):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE)
    return channel, connection

    print(" [x] Sent : <--analysis_completed -->")
    connection.close()


def listen(channel, connection, QUEUE):
    channel.basic_consume(queue=QUEUE,
                          auto_ack=True,
                          on_message_callback=prediction)

    channel.queue_declare(queue=QUEUE)
    print("Waiting for a signal ...")
    channel.start_consuming()


def main():
    print("Waiting for rabbitmq server start ...")
    time.sleep(7)
    global result
    print("Init new connection to received message...")
    result = init_connection('acquisition_completed')
    listen(result[0], result[1],'acquisition_completed')


if __name__ == '__main__':
    main()
