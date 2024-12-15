import pandas as pd
import numpy as np
from scipy.stats import levene, mannwhitneyu, shapiro
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(r"../datasets/ds_clean.csv")

# Фильтрация вакансий в розничной торговле
df = df[df['industry_id_list'].str.contains('7', na=False)]

convenient_schedules = ['flexible']
df['is_flexible_schedule'] = df['work_schedule'].isin(convenient_schedules)

flexible = df[df['is_flexible_schedule'] == True]['response_count']
not_flexible = df[df['is_flexible_schedule'] == False]['response_count']


p_shapiro_flex = shapiro(flexible)
p_shapiro_no_flex = shapiro(not_flexible)

print("\nПроверка нормальности:")
print("p-value (гибкий график):", p_shapiro_flex)
print("p-value (без гибкого графика):", p_shapiro_no_flex)

# Тест Манна-Уитни
stat, p_value = mannwhitneyu(flexible, not_flexible)
print(f'U-test p-value: {p_value}')

# Визуализация
# Боксплоты числа откликов по типу графика работы
sns.boxplot(x='is_flexible_schedule', y='response_count', data=df, palette='Set2', showfliers=False)
plt.xticks([0, 1], ['Негибкий график', 'Гибкий график'])
plt.title('Сравнение числа откликов по графику работы')
plt.xlabel('Тип графика работы')
plt.ylabel('Число откликов')
plt.show()
