import os
import pandas as pd

metrics_dir = 'data-collection/local-metrics'

dataframes = []

for filename in os.listdir(metrics_dir):
    if filename.endswith('.xlsx'):
        filepath = os.path.join(metrics_dir, filename)
        df = pd.read_excel(filepath)
        
        city_name = os.path.splitext(filename)[0]
        
        df['city'] = city_name
        
        dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)

cols = ['city'] + [col for col in combined_df.columns if col != 'city']
combined_df = combined_df[cols]

combined_df.columns = ['City', 'φ', 'Ηo', 'Ηw', 'ĩ', 'ς', 'k̅', 'Pde', 'P4w']

combined_df['City'] = combined_df['City'].str.replace('_', ' ').str.title()

combined_df.to_excel('data-collection/combined_metrics.xlsx', index=False)