import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, levene
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../datasets/ds_clean.csv")
print(df.columns)

# Фильтрация вакансий в розничной торговле
df = df[df['industry_id_list'].str.contains('41', na=False)]

df = df[df['response_count'] > 0]

# Удобный и неудобный график
convenient_schedules = ['flexible']
df['is_convenient_schedule'] = df['work_schedule'].isin(convenient_schedules)

# Обработака выбросов
q99 = df['response_count'].quantile(0.99)
df = df[df['response_count'] <= q99]

convenient = df[df['is_convenient_schedule'] == True]['response_count']
not_convenient = df[df['is_convenient_schedule'] == False]['response_count']


# Проверка равенства дисперсий (тест Левена)
stat, p_levene = levene(convenient, not_convenient)
print(f'Levene test p-value: {p_levene}')

# Тест Уэлча
stat, p_value = ttest_ind(convenient, not_convenient, equal_var=(p_levene >= 0.05))
print(f'T-test p-value: {p_value}')

# Визуализация
# Боксплоты числа откликов по типу графика работы
sns.boxplot(x='is_convenient_schedule', y='response_count', data=df, palette='Set2', showfliers=False)
plt.xticks([0, 1], ['Неудобный график', 'Удобный график'])
plt.title('Сравнение числа откликов по графику работы')
plt.xlabel('Тип графика работы')
plt.ylabel('Число откликов')
plt.show()


# Проверка механизма
# t-test для школьников
convenient_school = df[df['is_convenient_schedule'] == True]['young_response_count']
not_convenient_school = df[df['is_convenient_schedule'] == False]['young_response_count']
stat_school, p_school = ttest_ind(convenient_school, not_convenient_school, equal_var=False)
print(f'T-test p-value для школьников: {p_school}')

# Визуал теста
sns.boxplot(x='is_convenient_schedule', y='young_response_count', data=df, palette='Pastel1', showfliers=False)
plt.xticks([0, 1], ['Неудобный график', 'Удобный график'])
plt.title('Число откликов от школьников (14-18 лет)')
plt.xlabel('Тип графика работы')
plt.ylabel('Число откликов от школьников')
plt.show()


# t-test для женщин
convenient_female = df[df['is_convenient_schedule'] == True]['female_response_count']
not_convenient_female = df[df['is_convenient_schedule'] == False]['female_response_count']
stat_female, p_female = ttest_ind(convenient_female, not_convenient_female, equal_var=False)
print(f'T-test p-value для женщин: {p_female}')

# Визуал теста
sns.boxplot(x='is_convenient_schedule', y='female_response_count', data=df, palette='Pastel2', showfliers=False)
plt.xticks([0, 1], ['Неудобный график', 'Удобный график'])
plt.title('Число откликов от женщин')
plt.xlabel('Тип графика работы')
plt.ylabel('Число откликов от женщин')
plt.show()


# Доп. построения
# Распределение числа откликов в зависимости от требуемого опыта
sns.boxplot(x='length_of_employment', y='response_count', data=df, palette='Set3', showfliers=False)
plt.title('Влияние опыта работы на число откликов')
plt.xlabel('Требуемый опыт работы')
plt.ylabel('Число откликов')
plt.xticks(
    ticks=[0, 1, 2, 3],
    labels=['Нет опыта', '1-3 года', '3-6 лет', 'Более 6 лет']
)
plt.show()

experience_groups = df.groupby('length_of_employment')['response_count'].mean()
print('Среднее число откликов по опыту работы:')
print(experience_groups)

region_groups = df.groupby('region_name')['response_count'].mean()
print('Среднее число откликов по регионам:')
print(region_groups)

# Распределение числа откликов в зависимости от региона
sns.barplot(x='region_name', y='response_count', data=df, palette='Set2')
plt.title('Среднее число откликов по регионам')
plt.xlabel('Регион')
plt.ylabel('Число откликов')
plt.xticks(rotation=45)
plt.show()

