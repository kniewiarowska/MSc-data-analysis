import numpy as np
import pandas as pd
import time
import datetime


def split_by_day(user_df):
    # split by date
    return {z: t for z, t in user_df.groupby(user_df['timestamp'].dt.date)}


def calculate_heart_rate(item):
    # remove wrong values
    heart_rate_data = item[((item['heart_rate'] > 39) & (item['heart_rate'] < 200))]  # remove wrong values

    # calculate average heart rate
    numer_of_heart_rate = (heart_rate_data.count()[0])
    if numer_of_heart_rate != 0:
        return heart_rate_data['heart_rate'].sum() / (heart_rate_data.count()[0])
    else:
        return heart_rate_mean


def calculate_raw_intensity(item):
    if item.count()[0] != 0:
        return item['raw_intensity'].sum() / (item.count()[0])
    else:
        return raw_intensity_mean


def calculate_heart_rate_mean(item):
    # remove wrong values
    heart_rate_data = item[((item['heart_rate'] > 39) & (item['heart_rate'] < 200))]
    return heart_rate_data['heart_rate'].mean()


def calculate_raw_intensity_mean(item):
    return item['raw_intensity'].mean()


def prepare_statistic_from_one_day(item, key, feeling_rates_for_user):
    # sum steps
    steps = item['steps'].sum()

    # calculate average heart rate
    heart_rate_avg = calculate_heart_rate(item)

    # calculate average raw intensity
    raw_intensity_avg = calculate_raw_intensity(item)

    first_date = key

    feeling_rate = find_feeling_rate(feeling_rates_for_user, first_date)

    data = [steps, round(heart_rate_avg, 2), round(raw_intensity_avg, 2),
            feeling_rate]
    final_data.append(data)


def user_feeling_rate(user_id):
    feeling_rates = pd.read_csv("data/db_feeling_result.csv")
    fru = feeling_rates.loc[feeling_rates['user_id'] == user_id]
    return fru


# def get_time_of_day(datetime):
#     date_and_time = str(datetime).split('T')
#     hh_mm_ss = date_and_time[1].split(':')
#     hour = hh_mm_ss[0]
#     print(hour)
#     return (int(hour) % 24 + 4) // 4


def find_feeling_rate(fru, date):
    results = []
    for idx, row in fru.iterrows():
        value = str(row['timestamp'])
        day = value.split(' ')[0]

        if str(day) == str(date):
            results.append(row['feeling_rate'])

    if len(results) != 0:
        res = (sum(results)/len(results))
        if res > 4:
            return 3
        if res > 3:
            return 2
        return 1

    return 0


def change_to_timestamp(date):
    date2 = pd.to_datetime(date, format='%Y-%m-%d %H:%M:%S')
    element = datetime.datetime.strptime(str(date2), "%Y-%m-%d %H:%M:%S")
    tuple = element.timetuple()
    return time.mktime(tuple)


def prepare_data_for_user(user_name):
    df = mi_band_data.loc[mi_band_data['user_id'] == user_name]
    datetime_column = pd.to_datetime(df['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Europe/Warsaw')
    df['timestamp'] = datetime_column
    data_grouped_by_day = split_by_day(df)

    for key, value in data_grouped_by_day.items():
        prepare_statistic_from_one_day(value, key, user_feeling_rate(user))


# Read data from mi_band
mi_band_data = pd.read_csv("data/cleaned_data.csv")
users = mi_band_data['user_id'].unique()

final_data = []
heart_rate_mean = calculate_heart_rate_mean(mi_band_data)
raw_intensity_mean = calculate_raw_intensity_mean(mi_band_data)

for user in users:
    prepare_data_for_user(user)


df = pd.DataFrame(final_data, columns=['steps', 'heart_rate', 'raw_intensity', 'feeling_rate'])
final_df = df.loc[df['feeling_rate'] != 0]
final_df.to_csv('data/daily_data_3_values.csv')
