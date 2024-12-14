import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv('DATASET_CLEAN.csv')


# Создание боксплотов
plt.figure(figsize=(12, 8))
sns.set_theme(style="whitegrid")

# Горизонтальный боксплот
palette = sns.color_palette("coolwarm", as_cmap=False)
sns.boxplot(
    data=df,
    y="work_schedule",
    x="response_count",
    palette=palette,
    orient="h",
    width=0.6
)

# Настройка внешнего вида
plt.title("Распределение количества откликов по типам графика работы", fontsize=16, fontweight='bold')
plt.xlabel("Количество откликов", fontsize=14)
plt.ylabel("Тип графика работы", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()


plt.show()
