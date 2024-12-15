import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка датасета (замените 'file_path.csv' на путь к вашему файлу)
data = pd.read_csv('..datasets/ds_clean.csv')

data['industry_id_list'] = data['industry_id_list'].apply(eval)

# Фильтруем данные по индустрии 7
it_data = data[data['industry_id_list'].apply(lambda x: 7 in x)]


# Разделяем на вакансии с гибким графиком и без него
flexible_data = it_data[it_data['work_schedule'] == 'flexible']
non_flexible_data = it_data[it_data['work_schedule'] != 'flexible']

# Вычисляем средние отклики для каждой группы
ratios = {
    'Male': flexible_data['male_response_count'].mean() / non_flexible_data['male_response_count'].mean(),
    'Female': flexible_data['female_response_count'].mean() / non_flexible_data['female_response_count'].mean(),
    'Teenagers': flexible_data['young_response_count'].mean() / non_flexible_data['young_response_count'].mean() ,
}

graph_data = pd.DataFrame({
    'Category': list(ratios.keys()),
    'Ratio': list(ratios.values())
})

sns.barplot(data=graph_data, x='Category', y='Ratio', palette='muted')
plt.title('Отношение средних откликов на вакансии с гибким к без гибкому')
plt.ylabel('Отношение средних откликов')
plt.xlabel('Категория откликов')
plt.ylim(0, max(graph_data['Ratio']) * 1.2)
plt.show()
