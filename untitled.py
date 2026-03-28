import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('titanic/train.csv')
print("Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())