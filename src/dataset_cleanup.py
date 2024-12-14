import pandas as pd

df_raw = pd.read_csv('../datasets/ds_raw.csv')

# Очищаем от пустых значений в колонке industry_id_list 
df_clean = df_raw[df_raw['industry_id_list'] != '[None]']

#  Дубликатов нет, поэтому закомментировано 
#deduplicated_data = cleaned_data.drop_duplicates()
#print(deduplicated_data)

q_low = df_clean['response_count'].quantile(0.01)  # 1-й процентиль
q_hi  = df_clean['response_count'].quantile(0.99)  # 99-й процентиль

# Очищаем от выбросов
df_clean = df_clean[(df_clean['response_count'] >= q_low) &
                    (df_clean['response_count'] <= q_hi)]

df_clean.to_csv('../datasets/ds_clean.csv')

