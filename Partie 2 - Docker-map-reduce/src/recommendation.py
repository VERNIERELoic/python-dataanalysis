from sklearn import tree
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import json


def prediction(filename):
    data = []
    with open(filename) as f:
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


prediction('json_data.json')
