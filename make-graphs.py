import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt
import numpy as np

train = pd.read_csv("train.csv")

area = train['OverallQual']
price = train['SalePrice']

fig, ax = plt.subplots()

ax.scatter(area, price)

ax.set_xlabel(r'OverallQual', fontsize=15)
ax.set_ylabel(r'SalesPrice', fontsize=15)

plt.show()