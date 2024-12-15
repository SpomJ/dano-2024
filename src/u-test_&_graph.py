import pandas as pd 
import numpy as np
from scipy.stats import mannwhitneyu
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../datasets/ds_clean.csv")

# Фильтрация вакансий в сфере IT
df = df[df['industry_id_list'].str.contains('7', na=False)]

# Определяем гибкие графики
convenient_schedules = ['flexible']
df['is_flexible_schedule'] = df['work_schedule'].isin(convenient_schedules)

# Разделение данных на гибкие и негибкие графики
flexible = df[df['is_flexible_schedule'] == True]['response_count']
not_flexible = df[df['is_flexible_schedule'] == False]['response_count']

# Тест Манна-Уитни
stat, p_value = mannwhitneyu(flexible, not_flexible, alternative='two-sided')
print(f'Mann-Whitney U test p-value: {p_value}')

# Визуализация
# Боксплоты числа откликов по типу графика работы
sns.boxplot(x='is_flexible_schedule', y='response_count', data=df, palette='Set2', showfliers=False)
plt.xticks([0, 1], ['Негибкий график', 'Гибкий график'])
plt.title('Сравнение числа откликов по графику работы')
plt.xlabel('Тип графика работы')
plt.ylabel('Число откликов')
plt.show()
