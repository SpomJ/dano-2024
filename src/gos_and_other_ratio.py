import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('..\datasets\ds_clean.csv')

# Проверим, что все необходимые колонки существуют
required_columns = ["work_schedule", "response_count", "industry_id_list"]
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    raise ValueError(f"В датасете отсутствуют следующие колонки: {', '.join(missing_columns)}")

# Преобразуем колонку industry_id_list в список (если она в строковом формате)
data['industry_id_list'] = data['industry_id_list'].apply(eval)

# Удаляем выбросы в response_count с использованием метода межквартильного размаха (IQR)
q1 = data['response_count'].quantile(0.25)
q3 = data['response_count'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

data = data[(data['response_count'] >= lower_bound) & (data['response_count'] <= upper_bound)]

# Создаем результирующую таблицу для расчетов
result = []

# Итерация по уникальным индустриям
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

# Преобразуем результат в DataFrame
result_df = pd.DataFrame(result)

# Рассчитываем среднее отношение для flexible графика во всех отраслях (кроме 36)
flexible_all_except_36 = result_df[(result_df['work_schedule'] == 'flexible') & (result_df['industry'] != 36)]['ratio'].mean()

# Извлекаем отношение для flexible в сфере номер 36
flexible_industry_36 = result_df[(result_df['work_schedule'] == 'flexible') & (result_df['industry'] == 36)]
flexible_ratio_36 = flexible_industry_36['ratio'].values[0] if not flexible_industry_36.empty else 0

# Подготовка данных для диаграммы
df_plot = pd.DataFrame({
    'Category': ['Все остальные', 'Государственные организации'],
    'Ratio': [flexible_all_except_36, flexible_ratio_36]
})

# Создание минималистичной диаграммы
sns.set(style="whitegrid")
plt.figure(figsize=(8, 6))

# Столбчатая диаграмма с изменением ширины и сдвига
sns.barplot(x='Category', y='Ratio', data=df_plot, palette='Blues_d', dodge=False)

# Настройка осей и заголовков
plt.title('Отношение гибкого графика к общей медиане', fontsize=14)
plt.ylabel('Отношение', fontsize=12)
plt.xlabel('Категория', fontsize=12)

# Убираем расстояние между столбиками
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
