import pandas as pd 
import os 

temp = os.getcwd()

df = pd.read_csv(os.path.join(temp,'TP_hadoop','ventes','sales_data_sample.csv'),sep = ',')
df  = df[['ORDERNUMBER',
       'QUANTITYORDERED', 'PRICEEACH', 'ORDERLINENUMBER', 'SALES', 'ORDERDATE',
       'STATUS', 'QTR_ID', 'MONTH_ID', 'YEAR_ID', 'PRODUCTLINE', 'MSRP',
       'PRODUCTCODE', 'CUSTOMERNAME', 'PHONE', 'ADDRESSLINE1', 'ADDRESSLINE2',
       'CITY', 'STATE', 'POSTALCODE', 'COUNTRY', 'TERRITORY',
       'CONTACTLASTNAME', 'CONTACTFIRSTNAME', 'DEALSIZE']]
df.to_csv(fr"{os.path.join(temp,'TP_hadoop','ventes','sales_data_sample.csv')}", sep = ',',index=False)