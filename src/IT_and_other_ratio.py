import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('../datasets/ds_clean.csv')

data['industry_id_list'] = data['industry_id_list'].apply(eval)

result = []

for industry in set(industry for sublist in data['industry_id_list'] for industry in sublist):
    # Фильтруем данные по индустрии
    industry_data = data[data['industry_id_list'].apply(lambda x: industry in x)]

    if industry_data.empty:
        continue

    # Общая медиана откликов по индустрии
    overall_median = industry_data['response_count'].median()

    # Расчет медиан откликов для каждого графика работы
    for schedule in industry_data['work_schedule'].unique():
        schedule_data = industry_data[industry_data['work_schedule'] == schedule]
        schedule_median = schedule_data['response_count'].median()
        
        # Отношение медианы графика к общей медиане
        if overall_median > 0:  # Проверка на деление на ноль
            ratio = schedule_median / overall_median
            result.append({
                'industry': industry,
                'work_schedule': schedule,
                'ratio': ratio
            })


result_df = pd.DataFrame(result)

# Рассчитываем среднее отношение для flexible графика во всех отраслях (кроме 7)
flexible_all_except_7 = result_df[(result_df['work_schedule'] == 'flexible') & (result_df['industry'] != 7)]['ratio'].median()

# Извлекаем отношение для flexible в сфере 7
flexible_industry_7 = result_df[(result_df['work_schedule'] == 'flexible') & (result_df['industry'] == 7)]
flexible_ratio_7 = flexible_industry_7['ratio'].values[0] if not flexible_industry_7.empty else 0

df_plot = pd.DataFrame({
    'Category': ['Все остальные', 'ИТ, системная интеграция, интернет'],
    'Ratio': [flexible_all_except_7, flexible_ratio_7]
})


sns.set(style="whitegrid")
plt.figure(figsize=(8, 6))

sns.barplot(x='Category', y='Ratio', data=df_plot, palette='Blues_d', dodge=False)

plt.title('Отношение медианы гибкого графика к общей', fontsize=14)
plt.ylabel('Отношение', fontsize=12)
plt.xlabel('Категория', fontsize=12)

plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

print()
