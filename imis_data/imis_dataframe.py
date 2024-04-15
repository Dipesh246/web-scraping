from pandas import DataFrame as df, read_json

# icd = read_json('main_dg_data.json')
item_data = read_json('item_data.json')
# service_data = read_json('service_data.json')

# # icd_dataframe = df(icd)
item_dataframe = df(item_data)
# service_dataframe = df(service_data)

# # icd_dataframe.to_csv('icd.csv',mode='w',index=False)
item_dataframe.to_csv('item.csv',index=False)
# service_dataframe.to_csv('service.csv', index=False)

print("Data was written to the CSV file successfully.")
# print(icd_dataframe.columns)
