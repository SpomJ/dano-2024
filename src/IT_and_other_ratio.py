import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def convert_to_int_list(lst):
    return [int(i) for i in lst]

data['industry_id_list'] = data['industry_id_list'].apply(lambda x: convert_to_int_list(x) if isinstance(x, list) else x)

# Создаем результирующую таблицу для расчетов
result = []

# Итерация по уникальным индустриям
for industry in set(industry for sublist in data['industry_id_list'] for industry in sublist):
    # Фильтруем данные по индустрии
    industry_data = data[data['industry_id_list'].apply(lambda x: industry in x)]

    if industry_data.empty:
        continue

    # Общая медиана откликов по индустрии
    overall_median = industry_data['response_count'].mean()

    # Расчет медиан откликов для каждого графика работы
    for schedule in industry_data['work_schedule'].unique():
        schedule_data = industry_data[industry_data['work_schedule'] == schedule]
        schedule_median = schedule_data['response_count'].mean()
        
        # Отношение медианы графика к общей медиане
        if overall_median > 0:  # Проверка на деление на ноль
            ratio = schedule_median / overall_median
            result.append({
                'industry': industry,
                'work_schedule': schedule,
                'ratio': ratio
            })

result_df = pd.DataFrame(result)

# Рассчитываем медианы для двух категорий: full_day и flexible_or_remote
# Для всех индустрий, кроме 7
full_day_all_except_7 = result_df[(result_df['work_schedule'] == 'full_day') & (result_df['industry'] != 7)]['ratio'].mean()
flexible_or_remote_all_except_7 = result_df[(result_df['work_schedule'].isin(['remote', 'flexible'])) & (result_df['industry'] != 7)]['ratio'].mean()

# Для индустрии 7
full_day_industry_7 = result_df[(result_df['work_schedule'] == 'full_day') & (result_df['industry'] == 7)]
full_day_ratio_7 = full_day_industry_7['ratio'].values[0] if not full_day_industry_7.empty else 0

flexible_or_remote_industry_7 = result_df[(result_df['work_schedule'].isin(['remote', 'flexible'])) & (result_df['industry'] == 7)]
flexible_or_remote_ratio_7 = flexible_or_remote_industry_7['ratio'].mean() if not flexible_or_remote_industry_7.empty else 0

# Подготовка данных для диаграммы
df_plot = pd.DataFrame({
    'Category': ['ИТ (Удаленный+Гибкий)', 'Все остальные (Удаленный+Гибкий)'],
    'Ratio': [flexible_or_remote_ratio_7, flexible_or_remote_all_except_7]
})

# Создание графика
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

sns.barplot(x='Category', y='Ratio', data=df_plot, palette='Blues_d', dodge=False)

plt.title('Отношение средних: откликов на вакансии с гибким и удаленным графиком работы к откликам на вакансии с полным днем', fontsize=14)
plt.ylabel('Отношение', fontsize=12)
plt.xlabel('Отрасль', fontsize=12)
plt.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='y=1.0')
plt.xticks()
plt.tight_layout()
plt.show()
