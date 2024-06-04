import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from sklearn.metrics import mean_squared_error

file_name = "ts_data.csv"
plot_eda = False

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

if plot_eda:
    df.plot(
        style=".",
        figsize=(15,5),
        color=color_pal[0],
        title="Amount of searches for the term 'Fidesz'",
        grid=True
    )
    plt.show()

df["SearchAmount"].plot(kind="hist", bins=10)
plt.show()

if plot_eda:
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

if plot_eda:
    fig, ax = plt.subplots(figsize=(15, 5))
    train.plot(ax=ax, label='Training Set', title='Data Train/Test Split')
    test.plot(ax=ax, label='Test Set')
    ax.axvline('2019-01-01', color='black', ls='--')
    ax.legend(['Training Set', 'Test Set'])
    plt.show()

# k-fold cross-validation

