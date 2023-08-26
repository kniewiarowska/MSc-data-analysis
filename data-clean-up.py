import pandas as pd
# Read data from mi_band
df = pd.read_csv("data/db_mi_band.csv")

# remove id column
df = df.drop('id', axis=1)
number_of_original_rows = df.count()[0]
print('Original number of records:' + str(number_of_original_rows))

# remove duplicates for test1
df = df.drop_duplicates(subset=['timestamp', 'user_id'], keep='first')
number_of_row_after_removal_of_duplicates = df.count()[0]
print('Number of records after duplicate removal:' + str(number_of_row_after_removal_of_duplicates))

difference = number_of_original_rows - number_of_row_after_removal_of_duplicates
print('Difference:')
print(difference)

# FOR mi band 6
var = df.loc[df['user_id'] == 'test1']
test1_data = var[((var['steps'] > 0) | ((var['heart_rate'] < 243) & (var['raw_intensity'] > 5)))]

# FOR mi band 3
var2 = df.loc[df['user_id'] != 'test1']
other_data = var2[((var2['steps'] > 0) | ((var2['heart_rate'] > 1) & (var2['raw_intensity'] > 0)))]

data = [test1_data, other_data]
df = pd.concat(data)

df.sort_values(by='timestamp', ascending=True)

print(df)
df.to_csv('data/cleaned_data.csv')

