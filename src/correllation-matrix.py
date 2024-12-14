import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка датасета
df = pd.read_csv("../datasets/ds_clean.csv")

df.dropna()
# Преобразование опыта работы в числовой формат
experience_mapping = {
    "no_experience": 0,
    "up_to_3_years": 2,
    "up_to_6_years": 4.5,
    "above_6_years": 7
}
df["length_of_employment_numeric"] = df["length_of_employment"].map(experience_mapping)

# Выбор числовых столбцов для корреляции
correlation_columns = [
    "response_count",
    "female_response_count",
    "young_response_count",
    "invitation_count",
    "compensation_from",
    "compensation_to",
    "length_of_employment_numeric",
]

# Создание матрицы корреляции
correlation_matrix = df[correlation_columns].corr()

# Построение heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(
    correlation_matrix, 
    annot=True, 
    fmt=".2f", 
    cmap="coolwarm", 
    square=True, 
    cbar_kws={"shrink": 0.8}
)
plt.title("Матрица корреляции")
plt.xticks(rotation=45, ha='right', rotation_mode="anchor")
plt.tight_layout()
plt.show()

