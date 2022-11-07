# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import pandas as pd
import numpy as np

df_order =pd.read_csv('orders.txt', sep='\t', engine='python',encoding='latin-1',parse_dates=['orderdate'])
#print(df_order)
#print(df_order.columns)
df_customer =pd.read_csv('customer.txt', sep='\t', engine='python',encoding='latin-1')

df_order = df_order[['orderid','customerid','orderdate','totalprice']]
df = df_order.merge(df_customer[['customerid','householdid']],left_on='customerid',right_on = 'customerid')

print(df)
print(df.isnull().values.sum())

#order month
#print(df.head)
#
import datetime as dt
df['order_month'] = df['orderdate'].apply(lambda x: dt.datetime(x.year,x.month, 1))
df_g_h = df.groupby('householdid')['order_month'].min().reset_index()
df_g_h.columns=['householdid','cohort']

df = df.merge(df_g_h, left_on='householdid', right_on='householdid')
print(df)

print()

#the period from every transcation to cohort month
df['cohort_month']=df['orderdate'].apply(lambda x:x.year*12 + x.month)-\
                   df['cohort'].apply(lambda x:x.year*12 + x.month) + 1
df['cohort']=df['cohort'].dt.strftime('%Y/%m')
print(df)
df_cohort=df.groupby(['cohort','cohort_month'])['householdid'].apply(pd.Series.nunique).reset_index()
print(df_cohort)
df_pivot= df_cohort.pivot(index = 'cohort', columns='cohort_month',values='householdid')
df_retention=df_pivot.divide(df_pivot.iloc[:,0],axis=0)
df_retention.round(3)*100

print(df_retention)

import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(18,10))
sns.heatmap(df_retention.iloc[0:5, 0:11], annot=True, vmin=0.0, vmax=20, cmap='YlGnBu',fmt='g')
plt.show()
