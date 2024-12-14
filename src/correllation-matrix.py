import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка датасета
df = pd.read_csv("..\datasets\ds_clean.csv", encoding="utf-8", delimiter=",")

# Выбор числовых столбцов для корреляции
correlation_columns = [
    "response_count",
    "male_response_count",
    "female_response_count",
    "young_response_count",
    "employees_number",
    "invitation_count",
    "compensation_from",
    "compensation_to",
]


# Создание матрицы корреляции
correlation_matrix = df[correlation_columns].corr()

mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
np.fill_diagonal(mask, False)

# Построение heatmap
new_column_names = [
    "число всех откликов",
    "число откликов от мужчин",
    "число откликов от женщин",
    "число откликов от соискателей 14–18 лет",
    "численность штата работодателя",
    "число всех приглашений",
    "минимальная зарплата",
    "максимальная зарплата"
]

# Построение heatmap с обновленными названиями
plt.figure(figsize=(10, 8))
sns.heatmap(
    correlation_matrix, 
    mask=mask,
    annot=True, 
    fmt=".2f", 
    cmap="coolwarm", 
    square=True, 
    cbar_kws={"shrink": 0.8},
    xticklabels=new_column_names,
    yticklabels=new_column_names
)
plt.title("Матрица корреляции")
plt.xticks(rotation=45, ha='right', rotation_mode="anchor")
plt.tight_layout()
plt.show()

