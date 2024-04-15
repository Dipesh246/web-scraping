import pandas as pd
import json

file_path = "VAT_Sales_Register_Report_Sample.xlsx"

# Determine file format
file_format = file_path.split(".")[-1].lower()

if file_format == "xlsx":
    excel_data = pd.read_excel(file_path)
elif file_format == "csv":
    excel_data = pd.read_csv(file_path)
else:
    print("File format not supported")

# new_excel_data = excel_data.drop(range(0, 6))
# excel_data = new_excel_data.reset_index(drop=True)
excel_data.iloc[0] = excel_data.iloc[0].str.replace(" ", "_")
new_columns = excel_data.iloc[0] + "_" + excel_data.iloc[1]
excel_data.columns = new_columns
excel_data = excel_data.drop([0, 1])
excel_data = excel_data.drop(excel_data.index[-1])
excel_data.columns = [
    "INVOICE_DATE_AD",
    "INVOICE_DATE_BS",
    "INVOICE_NO",
    "INVOICE_BUYER_NAME",
    "INVOICE_BUYER_PAN",
    "INVOICE_ITEM_NAME",
    "INVOICE_QTY",
    "INVOICE_UNIT",
    "TOTAL_SALES/EXPORT_VALUE",
    "NON_TAXABLE_SALES_VALUE",
    "TAXABLE_SALES_VALUE",
    "TAXABLE_SALES_VAT",
    "EXPORT_SALES_VALUE",
    "EXPORT_SALES_COUNTRY",
    "EXPORT_SALES_EXPORT_PP_NO",
    "EXPORT_SALES_EXPORT_PP_DATE",
]
columns_to_drop = [
        "EXPORT_SALES_COUNTRY",
        "EXPORT_SALES_EXPORT_PP_NO",
        "EXPORT_SALES_EXPORT_PP_DATE",
    ]
excel_data = excel_data.drop(columns=columns_to_drop, axis=1)
excel_data["INVOICE_DATE_BS"] = pd.to_datetime(
        excel_data["INVOICE_DATE_BS"], format="%Y.%m.%d"
    ).dt.strftime("%Y/%m/%d")

grouped_data = (
    excel_data.groupby([
        "INVOICE_DATE_AD",
        "INVOICE_DATE_BS",
        "INVOICE_NO",
        "INVOICE_BUYER_NAME",
        "INVOICE_BUYER_PAN"
    ])
    # .agg(agg_function)
    .apply(lambda group: group.drop(columns=[
        "INVOICE_DATE_AD",
        "INVOICE_DATE_BS",
        "INVOICE_NO",
        "INVOICE_BUYER_NAME",
        "INVOICE_BUYER_PAN"
    ]).to_dict(orient='records'))
    .reset_index(name='detail')
    .to_dict(orient='records')
)

json_output_file = "grouped_data.json"
with open(json_output_file, 'w') as json_file:
    json.dump(grouped_data, json_file, indent=2)