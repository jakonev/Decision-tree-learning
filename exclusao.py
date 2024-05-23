import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
#
# data = {
# 'gender': ['male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female', 'female'],
# 'height': [6, 4, 10, 5, 2, 6, 4, 1, 1, 10, 4, 9, 9, 2, 9, 6, 6, 8, 3, 4, 3, 3, 2, 3, 8, 9, 7, 10, 4, 8, 5, 7, 6, 1, 9, 6, 9, 5, 4, 6, 2, 6, 5, 6, 5, 1, 9, 1, 7, 4]
# }
#
# df = pd.DataFrame(data)
# df.head(n = 5)
#
# y = sns.histplot(data=df, x="height", hue='gender', alpha=0.5, multiple="dodge", stat="percent")
#
# female = []
# male = []
# for f,m in zip(y.containers[0], y.containers[1]):
#     female.append(f.get_height())
#     male.append(m.get_height())
#
# print(female)
# print(male)
#
# female_per = ['{:.2f}%'.format(x/sum(female)*100) for x in female]
# male_per = ['{:.2f}%'.format(x/sum(male)*100) for x in male]
# print(female_per)
# print(male_per)
#
# y.bar_label(y.containers[0], labels=female_per)
# y.bar_label(y.containers[1], labels=male_per)
#
# plt.show()
#
# # y.bar_label(y.containers[0])
# # y.bar_label(y.containers[1])


# xlist = 900+200*np.random.randn(50,1)
#
# fig, ax = plt.subplots()
# y = sns.histplot(data=xlist, element="bars", bins=20, stat='count', legend=False)
# y.set(xlabel='total time (ms)')
# y.bar_label(y.containers[0])
#
# plt.show()

fruit_names = ['Coffee', 'Salted Caramel', 'Pistachio']
fruit_counts = [4000, 2000, 7000]

fig, ax = plt.subplots()
bar_container = ax.bar(fruit_names, fruit_counts)
ax.set(ylabel='pints sold', title='Gelato sales by flavor', ylim=(0, 8000))
ax.bar_label(bar_container, fmt='{:,.0f}')
plt.show()