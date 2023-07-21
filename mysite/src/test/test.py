import pandas as pd
import os
brand_list_df = pd.read_excel('comparison_list.xlsx')
brand_list = brand_list_df['comparison_list'].to_list()

url_list_df = pd.read_excel('test_data/url_list.xlsx')

url_list = url_list_df['link'].to_list()

df0=pd.read_excel('test_data/0.xlsx')
df1=pd.read_excel('test_data/1.xlsx')
df2=pd.read_excel('test_data/2.xlsx')
df_list =[]
df_list.append(df0)
df_list.append(df1)
df_list.append(df2)
print(df_list)