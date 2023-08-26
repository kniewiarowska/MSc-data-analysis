import numpy as np
import pandas as pd
import time
import datetime


def split_data_by_hour_and_day(user_df):
    # split by date
    hh = {z: t for z, t in user_df.groupby(user_df['timestamp'].dt.date)}

    # split by hour in day
    dfs_hours_in_day = []
    for day in hh.items():
        user_df = day[1]
        data = {x: y for x, y in user_df.groupby(user_df['timestamp'].dt.hour)}

        for hour in data.items():
            dfs_hours_in_day.append(hour[1])

    return dfs_hours_in_day


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


def prepare_statistic_from_one_hour(item, feeling_rates_for_user):
    # sum steps
    steps = item['steps'].sum()

    # calculate average heart rate
    heart_rate_avg = calculate_heart_rate(item)

    # calculate average raw intensity
    raw_intensity_avg = calculate_raw_intensity(item)

    first_date = item['timestamp'].values[0]

    feeling_rate = find_feeling_rate(feeling_rates_for_user, first_date)

    time_of_day = get_time_of_day(first_date)

    data = [steps, round(heart_rate_avg, 2), round(raw_intensity_avg, 2),
            feeling_rate, time_of_day]
    final_data.append(data)


def get_time_of_day(datetime):
    date_and_time = str(datetime).split('T')
    hh_mm_ss = date_and_time[1].split(':')
    hour = hh_mm_ss[0]
    print(hour)
    return (int(hour) % 24 + 4) // 4
    # time_of_day_dict = {1: 'Late Night', 2: 'Early Morning', 3: 'Morning', 4: 'Noon', 5: 'Evening', 6: 'Night'}
    # return time_of_day_dict.get(time_of_day)


def user_feeling_rate(user_id):
    feeling_rates = pd.read_csv("data/db_feeling_result.csv")
    fru = feeling_rates.loc[feeling_rates['user_id'] == user_id]
    timestamps = []
    for row in fru.itertuples():
        timestamp = change_to_timestamp(row.timestamp)
        timestamps.append(timestamp)
    fru['timestamp'] = timestamps

    return fru


def find_feeling_rate(fru, date):
    date2 = change_to_timestamp(date)
    last_time_stamp = fru['timestamp'].values[0]
    value = last_time_stamp
    for row in fru.itertuples():
        if row.timestamp < date2:
            last_time_stamp = row.timestamp
        if row.timestamp > last_time_stamp:
            value = last_time_stamp

    feeling_row = fru.loc[fru['timestamp'] == value]
    feeling_value = feeling_row['feeling_rate'].values[0]

    if feeling_value == 5:
        return 3
    if feeling_value == 4:
        return 2
    return 1


def change_to_timestamp(date):
    date2 = pd.to_datetime(date, format='%Y-%m-%d %H:%M:%S')
    element = datetime.datetime.strptime(str(date2), "%Y-%m-%d %H:%M:%S")
    tuple = element.timetuple()
    return time.mktime(tuple)


def prepare_data_for_user(user_name):
    df = mi_band_data.loc[mi_band_data['user_id'] == user_name]
    datetime_column = pd.to_datetime(df['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Europe/Warsaw')
    df['timestamp'] = datetime_column
    data_grouped_by_hour = split_data_by_hour_and_day(df)

    for item in data_grouped_by_hour:
        prepare_statistic_from_one_hour(item, user_feeling_rate(user))


# Read data from mi_band
mi_band_data = pd.read_csv("data/cleaned_data.csv")
users = mi_band_data['user_id'].unique()

final_data = []
heart_rate_mean = calculate_heart_rate_mean(mi_band_data)
raw_intensity_mean = calculate_raw_intensity_mean(mi_band_data)

for user in users:
    prepare_data_for_user(user)

final_df = pd.DataFrame(final_data, columns=['steps', 'heart_rate', 'raw_intensity', 'feeling_rate',
                                             'time_of_day'])
print(final_df)
final_df.to_csv('data/one_hour_data.csv')
