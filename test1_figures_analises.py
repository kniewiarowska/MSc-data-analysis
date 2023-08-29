import pandas as pd
import matplotlib.pyplot as plt
import time


def change_to_dict(d, dict):
    for i in range(0, len(d)):
        date = d[i].values[0][4]
        dict.update({date: d[i]})


def print_figures_for_day(day):

    fig_df = dict.get(day)
    x = fig_df['time'].values
    steps = fig_df['steps'].values
    heart_rate = fig_df['heart_rate'].values
    raw_intensity = fig_df['raw_intensity'].values

    plt.figure()
    plt.plot(x, steps, 'bx-')
    plt.title(day)
    plt.xlabel('time')
    plt.xticks(rotation=90)
    plt.ylabel('steps')

    plt.figure()
    plt.plot(x, heart_rate, 'bx-')
    plt.title(day)
    plt.xticks(rotation=90)
    plt.ylabel('heart_rate')

    plt.figure()
    plt.plot(x, raw_intensity, 'bx-')
    plt.title(day)
    plt.xlabel('time')
    plt.xticks(rotation=90)
    plt.ylabel('raw_intensity')
    plt.show()


def get_figures_for_period(start, end):
    df2 = df2[((df2['date'] > end) & (df2['date'] > start))]

    x = fig_df['time'].values
    steps = fig_df['steps'].values
    heart_rate = fig_df['heart_rate'].values
    raw_intensity = fig_df['raw_intensity'].values

    plt.figure()
    plt.plot(x, steps, 'bx-')
    plt.title(day)
    plt.xlabel('time')
    plt.xticks(rotation=90)
    plt.ylabel('steps')

    plt.figure()
    plt.plot(x, heart_rate, 'bx-')
    plt.title(day)
    plt.xticks(rotation=90)
    plt.ylabel('heart_rate')

    plt.figure()
    plt.plot(x, raw_intensity, 'bx-')
    plt.title(day)
    plt.xlabel('time')
    plt.xticks(rotation=90)
    plt.ylabel('raw_intensity')
    plt.show()


df = pd.read_csv("data/one_hour_data_test1.csv")
df2 = pd.read_csv("data/one_hour_datetime_test1.csv")
dfs = [y for x, y in df.groupby('day', as_index=False)]
dict = {}

change_to_dict(dfs, dict)

#print_figures_for_day('2023-05-07')
get_figures_for_period('2023-05-07', '2023-07-01')

