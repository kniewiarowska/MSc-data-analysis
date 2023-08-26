# Analiza i modyfikacja danych
import numpy as np
import pandas as pd
# Ewaluacja
import sns as sns
from matplotlib import pyplot as plt
from sklearn.metrics import precision_score, classification_report
from sklearn.metrics import recall_score, f1_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
# machine learning
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier


# Wizualizacja
def read_raw_data():
    df = pd.read_csv('data/messy/final_data_raw2.csv')
    return df.drop(columns=df.columns[0], axis=1)


def read_grouped_data():
    df = pd.read_csv('data/messy/final_data.csv')
    return df.drop(columns=df.columns[0], axis=1)


def calculate_feeling_rate_distribution(df):
    print('DATA:')
    count = df.count()[0]
    for i in df['feeling_rate'].unique():
        occur = df['feeling_rate'].value_counts()[i]
        percent = (occur / count) * 100
        print(str(i) + ' ' + str(round(percent, 2)) + '%')


def print_df_information(df):
    print(df.head())
    print(df.info())
    print(df.describe())


def change_txt_data(df):
    print(df.describe(include=['O']))
    categoricals = list(df.select_dtypes(include=['O']).columns)
    encoder = OneHotEncoder(sparse_output=False)
    encoded = encoder.fit_transform(df[categoricals])
    train_ohe = pd.DataFrame(encoded, columns=np.hstack(encoder.categories_))
    df = pd.concat((df, train_ohe), axis=1).drop(categoricals, axis=1)
    print(df.head())
    return df


def calculate_metrics(model, X_test, y_test):
    pred = model.predict(X_test)
    # acc = accuracy_score(y_test, pred)
    print(classification_report(y_test, pred))
    # precision = precision_score(y_test, pred, pos_label='positive')
    # recall = recall_score(y_test, pred, pos_label='positive')
    # f_score = f1_score(y_test, pred, pos_label='positive', average='micro')
    # print('Accuracy: {}\nPrecision: {}\nRecall: {}\nF1_score: {}'.format(
    #    acc, precision, recall, f_score))


train_df = read_grouped_data()
train_df = change_txt_data(train_df)
Y = train_df['feeling_rate'].values
X = train_df.drop(['feeling_rate'], axis=1).values
calculate_feeling_rate_distribution(train_df)

sns.heatmap(train_df.corr(), annot=True)
plt.tight_layout()


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=71830, stratify=Y)

print('Tree')
tree = DecisionTreeClassifier(random_state=71830, class_weight='balanced')
tree.fit(X_train, Y_train)
calculate_metrics(tree, X_test, Y_test)

print('K Neighbours')
kneighbors = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto', leaf_size=30, p=2,                                  metric='minkowski', metric_params=None, n_jobs=None)
kneighbors.fit(X_train, Y_train)
calculate_metrics(kneighbors, X_test, Y_test)

print('Naive Bayes')
gnb = GaussianNB()
gnb.fit(X_train, Y_train)
calculate_metrics(gnb, X_test, Y_test)

# print('MLPClassifier')
# sc = StandardScaler()
# mlp_data = sc.fit_transform(train_df)
# mlp = MLPClassifier(hidden_layer_sizes=(150,100,50), max_iter=300,activation = 'relu',solver='adam',random_state=1)
# X_mpl_train, X_mpl_test, Y_mpl_train, Y_mpl_test = train_test_split(X, Y, test_size=0.2, random_state=71830, stratify=Y)
# mlp.fit(X_mpl_train, Y_mpl_test)
# calculate_metrics(mlp, X_mpl_test, Y_mpl_test)
