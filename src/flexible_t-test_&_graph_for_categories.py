import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import stats

data = pd.read_csv('../datasets/ds_clean.csv')

data['industry_id_list'] = data['industry_id_list'].apply(eval)

it_data = data[data['industry_id_list'].apply(lambda x: 7 in x)]

flexible_data = it_data[it_data['work_schedule'] == 'flexible']
non_flexible_data = it_data[it_data['work_schedule'] == 'full_day']

categories = ['male_response_count', 'female_response_count', 'young_response_count']

for category in categories:

    flexible_responses = flexible_data[category]
    non_flexible_responses = non_flexible_data[category]

    # Тест Уэлча
    u_stat, p_value = stats.ttest_ind(flexible_responses, non_flexible_responses, equal_var = False)
    print(f"Тест Уэлча для {category}: U-статистика={u_stat:.3f}, p-значение={p_value}\n")

ratios = {
    'Мужчины': flexible_data['male_response_count'].mean() / non_flexible_data['male_response_count'].mean(),
    'Женщины': flexible_data['female_response_count'].mean() / non_flexible_data['female_response_count'].mean(),
    'Подростки (14-18 лет)': flexible_data['young_response_count'].mean() / non_flexible_data['young_response_count'].mean()
}
graph_data = pd.DataFrame({
    'Category': list(ratios.keys()),
    'Ratio': list(ratios.values())
})

sns.barplot(data=graph_data, x='Category', y='Ratio', palette='muted')
plt.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='y=1.0')
plt.title('Отношение средних: откликов на вакансии с гибким графиком к откликам на вакансии с полным днем')
plt.ylabel('Отношение')
plt.xlabel('Категория соискателей')
plt.ylim(0, max(graph_data['Ratio']) * 1.2)
plt.show()
