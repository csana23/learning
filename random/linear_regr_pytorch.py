import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("..\medical_insurance.csv")
df.info()

x = df["bmi"].to_numpy()
y = df["charges"].to_numpy()

