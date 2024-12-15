import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, levene
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../datasets/ds_clean.csv")

# Фильтрация вакансий в розничной торговле
df = df[df['industry_id_list'].str.contains('7', na=False)]

convenient_schedules = ['flexible']
df['is_flexible_schedule'] = df['work_schedule'].isin(convenient_schedules)

flexible = df[df['is_flexible_schedule'] == True]['response_count']
not_flexible = df[df['is_flexible_schedule'] == False]['response_count']

print(flexible.count())
print(not_flexible.count())
# Проверка равенства дисперсий (тест Левена)
stat, p_levene = levene(flexible, not_flexible)
print(f'Levene test p-value: {p_levene}')

# Тест Уэлча
stat, p_value = ttest_ind(flexible, not_flexible, equal_var=(p_levene >= 0.05))
print(f'T-test p-value: {p_value}')

# Визуализация
# Боксплоты числа откликов по типу графика работы
sns.boxplot(x='is_flexible_schedule', y='response_count', data=df, palette='Set2', showfliers=False)
plt.xticks([0, 1], ['Негибкий график', 'Гибкий график'])
plt.title('Сравнение числа откликов по графику работы')
plt.xlabel('Тип графика работы')
plt.ylabel('Число откликов')
plt.show()