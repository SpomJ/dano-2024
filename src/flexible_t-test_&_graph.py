import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../datasets/ds_clean.csv")

df['industry_id_list'] = df['industry_id_list'].apply(eval)
df = df[df['industry_id_list'].apply(lambda x: 7 in x)]

df['schedule_type'] = df['work_schedule'].apply(
    lambda x: 'Удаленный график' if x == 'flexible' else ('Полный день' if x == 'full_day' else None)
)

df = df[df['schedule_type'].notna()]

flexible_or_remote = df[df['schedule_type'] == 'Удаленный график']['response_count']
full_day = df[df['schedule_type'] == 'Полный день']['response_count']

# Тест Уэлча
stat, p_value = ttest_ind(flexible_or_remote, full_day, equal_var=False)
print(f"Welch's t-test p-value: {p_value}")

print(f"Среднее число откликов (Полный день): {full_day.mean()}")
print(f"Среднее число откликов (Гибкий): {flexible_or_remote.mean()}")

# Визуализация
sns.boxplot(x='schedule_type', y='response_count', data=df, palette='Set2', showfliers=False)
plt.title('Сравнение числа откликов по графику работы')
plt.xlabel('Тип графика работы')
plt.ylabel('Число откликов')
plt.show()
