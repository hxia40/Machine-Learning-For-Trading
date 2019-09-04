
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("text1.csv", parse_dates=True, na_values=['nan'])
print df
fig, ax = plt.subplots()

for key, grp in df.groupby(['color']):
    ax = grp.plot(ax=ax, kind='line', x='x', y='y', c=key, label=key)

plt.legend(loc='best')
plt.show()