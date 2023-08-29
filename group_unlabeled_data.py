import pandas as pd
# Read data from mi_band

df = pd.read_csv("data/unlabeled/3/HEARTRATE_AUTO.csv")
df2 = pd.read_csv("data/unlabeled/3/ACTIVITY_MINUTE.csv")

dfs = [y for x, y in df.groupby('date', as_index=False)]
dfs2 = [y for x, y in df2.groupby('date', as_index=False)]

results = []
dfs_dict = {}
dfs2_dict = {}


def change_to_dict(d, dict):
    for i in range(0, len(d)):
        date = d[i].values[0][0]
        dict.update({date: d[i]})


def prepare_dataframe(dfs_dict, dfs2_dict):

    for key in dfs_dict:
        value2 = dfs2_dict.get(key)
        if value2 is None:
            continue
        else:
            prepare_one_df(dfs_dict.get(key), value2)

    return pd.DataFrame(results, columns=['date', 'time', 'steps', 'heart_rate'])


def prepare_one_df(d, d2):

    for idx, row in d.iterrows():
        date = row['date']
        minute = row['time']

        for idx2, row2 in d2.iterrows():
            date2 = row2['date']
            minute2 = row2['time']

            if date == date2:
                if minute == minute2:
                    results.append([date, minute, row2['steps'], row['heartRate']])
                    break
                else:
                    results.append([date, minute,  0, row['heartRate']])

            if minute2 > minute:
                print(str(date2) + str(minute2))
                print(str(date) + str(minute))
                break


change_to_dict(dfs, dfs_dict)
change_to_dict(dfs2, dfs2_dict)

var = prepare_dataframe(dfs_dict, dfs2_dict)
var = var.drop_duplicates(subset=['date', 'time', 'steps', 'heart_rate'], keep='first')
var = var.drop_duplicates(subset=['date', 'time'], keep='last')
var.to_csv('data/cleaned_data_unlebeled3.csv')