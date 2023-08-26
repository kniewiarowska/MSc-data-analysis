import pandas as pd
import time
import datetime

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
    last_time_stamp = fru['timestamp'].values[0]
    value = last_time_stamp
    for row in fru.itertuples():
        if row.timestamp < date:
            last_time_stamp = row.timestamp
        if row.timestamp > last_time_stamp:
            value = last_time_stamp

    feeling_row = fru.loc[fru['timestamp'] == value]
    return feeling_row['feeling_rate'].values[0]


def change_to_timestamp(date):
    date2 = pd.to_datetime(date, format='%Y-%m-%d %H:%M:%S')
    element = datetime.datetime.strptime(str(date2), "%Y-%m-%d %H:%M:%S")
    tuple = element.timetuple()
    return time.mktime(tuple)


def prepare_data_for_user(user_name):
    df = mi_band_data.loc[mi_band_data['user_id'] == user_name]
    fru = user_feeling_rate(user_name)
    for item in df.itertuples():
        data = [item.steps, item.heart_rate, item.raw_intensity, find_feeling_rate(fru, item.timestamp), get_time_of_day(item.timestamp)]
        final_data.append(data)


def get_time_of_day(timestamp):

    dt = datetime.datetime.fromtimestamp(timestamp)
    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    date_and_time = str(formatted_time).split(' ')
    hh_mm_ss = date_and_time[1].split(':')
    hour = hh_mm_ss[0]
    return (int(hour) % 24 + 4) // 4
    # time_of_day = (int(hour) % 24 + 4) // 4
    # time_of_day_dict = {1: 'Late Night', 2: 'Early Morning', 3: 'Morning', 4: 'Noon', 5: 'Evening', 6: 'Night'}
    # return time_of_day_dict.get(time_of_day)


# Read data from mi_band
mi_band_data = pd.read_csv("data/db_mi_band.csv")
users = mi_band_data['user_id'].unique()

final_data = []

for user in users:
    prepare_data_for_user(user)

final_df = pd.DataFrame(final_data, columns=['steps', 'heart_rate', 'raw_intensity', 'feeling_rate', 'time_of_day'])
final_df.to_csv('data/grouped_data.csv')