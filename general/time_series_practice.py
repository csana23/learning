import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import TimeSeriesSplit

file_name = "ts_data.csv"
PLOT_EDA = False
PLOT_TSS = False

# pre-processing
df = pd.read_csv(file_name, sep=",")
print("Initial load:\n", df.head())

df = df.rename(columns={"Fidesz: (Hungary)": "SearchAmount"})
df = df.set_index("Month")
df.index = pd.to_datetime(df.index)
df.index = df.index.rename("YearMonth")
print("Changing index:\n", df.head())

# plot data
color_pal = sns.color_palette()

if PLOT_EDA:
    df.plot(
        style=".",
        figsize=(15,5),
        color=color_pal[0],
        title="Amount of searches for the term 'Fidesz'",
        grid=True
    )
    plt.show()

if PLOT_EDA:
    df["SearchAmount"].plot(kind="hist", bins=10)
    plt.show()

if PLOT_EDA:
    df.query("SearchAmount > 60")["SearchAmount"].plot(
        style=".",
        figsize=(15,5),
        color=color_pal[5],
        title="Outliers",
        grid=True
    )
    plt.show()

df = df.query("SearchAmount < 60").copy()

# reference train-test split
train = df.loc[df.index < "2019-01-01"]
test = df.loc[df.index >= "2019-01-01"]

if PLOT_EDA:
    fig, ax = plt.subplots(figsize=(15, 5))
    train.plot(ax=ax, label='Training Set', title='Data Train/Test Split')
    test.plot(ax=ax, label='Test Set')
    ax.axvline('2019-01-01', color='black', ls='--')
    ax.legend(['Training Set', 'Test Set'])
    plt.show()

# k-fold cross-validation
tss = TimeSeriesSplit()
df = df.sort_index()

if PLOT_TSS:
    fig, axs = plt.subplots(5, 1, figsize=(10, 15), sharex=True)

    fold = 0
    for train_idx, val_idx in tss.split(df):
        train = df.iloc[train_idx]
        test = df.iloc[val_idx]
        train['SearchAmount'].plot(ax=axs[fold],
                            label='Training Set',
                            title=f'Data Train/Test Split Fold {fold}')
        test['SearchAmount'].plot(ax=axs[fold],
                            label='Test Set')
        axs[fold].axvline(test.index.min(), color='black', ls='--')
        fold += 1
    plt.show()

def create_features(df):
    df = df.copy()
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    return df

df = create_features(df)

def add_lags(df):
    target_map = df['SearchAmount'].to_dict()
    df['lag1'] = (df.index - pd.DateOffset(years=1)).map(target_map)
    df['lag2'] = (df.index - pd.DateOffset(years=2)).map(target_map)
    df['lag3'] = (df.index - pd.DateOffset(years=3)).map(target_map)
    return df

df = add_lags(df)
print("Adding lags:\n", df.tail())

fold = 0
preds = []
scores = []

for train_idx, val_idx in tss.split(df):
    train = df.iloc[train_idx]
    test = df.iloc[val_idx]

    train = create_features(train)
    test = create_features(test)

    FEATURES = ['quarter', 'month','year','lag1','lag2','lag3']
    TARGET = 'SearchAmount'

    X_train = train[FEATURES]
    y_train = train[TARGET]

    X_test = test[FEATURES]
    y_test = test[TARGET]

    reg = xgb.XGBRegressor(base_score=0.5, booster='gbtree',    
                           n_estimators=1000,
                           early_stopping_rounds=50,
                           objective='reg:linear',
                           max_depth=3,
                           learning_rate=0.01)
    reg.fit(X_train, y_train,
            eval_set=[(X_train, y_train), (X_test, y_test)],
            verbose=100)

    y_pred = reg.predict(X_test)
    preds.append(y_pred)
    score = np.sqrt(mean_squared_error(y_test, y_pred))
    scores.append(score)

print(f'Score across folds {np.mean(scores):0.4f}')
print(f'Fold scores:{scores}')