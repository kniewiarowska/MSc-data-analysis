import numpy as np
import pandas as pd
import time
import datetime


def split_by_day(user_df):
    # split by date
    return {z: t for z, t in user_df.groupby('date')}


def calculate_heart_rate(item):
    # remove wrong values
    heart_rate_data = item[((item['heart_rate'] > 39) & (item['heart_rate'] < 200))]  # remove wrong values

    # calculate average heart rate
    numer_of_heart_rate = (heart_rate_data.count()[0])
    if numer_of_heart_rate != 0:
        return heart_rate_data['heart_rate'].sum() / (heart_rate_data.count()[0])
    else:
        return heart_rate_mean


def calculate_heart_rate_mean(item):
    # remove wrong values
    heart_rate_data = item[((item['heart_rate'] > 39) & (item['heart_rate'] < 200))]
    return heart_rate_data['heart_rate'].mean()


def prepare_statistic_from_one_day(item):
    # sum steps
    steps = item['steps'].sum()

    # calculate average heart rate
    heart_rate_avg = calculate_heart_rate(item)

    data = [steps, round(heart_rate_avg, 2)]

    final_data.append(data)


# Read data from mi_band
mi_band_data1 = pd.read_csv("data/cleaned_data_unlebeled.csv")
mi_band_data2 = pd.read_csv("data/cleaned_data_unlebeled2.csv")
mi_band_data3 = pd.read_csv("data/cleaned_data_unlebeled3.csv")
array = [mi_band_data1, mi_band_data2, mi_band_data3]

final_data = []

for i in range(0, 2):
    heart_rate_mean = calculate_heart_rate_mean(array[i])

    days = split_by_day(array[i])
    for key in days:
        prepare_statistic_from_one_day(days.get(key))


df = pd.DataFrame(final_data, columns=['steps', 'heart_rate'])
df.to_csv('data/daily_data_unlabeled.csv')
