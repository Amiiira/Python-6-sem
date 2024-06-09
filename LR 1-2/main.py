from typing import List, Dict
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mathstats import MathStats
import csv

FILE = 'Retail.csv'
FILE2 = 'MarketingSpend.csv'

def read_data(file: str) -> List[Dict[str, str]]:
    data = []
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data.extend(row for row in reader)
    return data

def count_unique_values(data: List[Dict[str, str]], key: str) -> int:
    return len(set(item[key] for item in data))

def count_invoices(data: List[Dict[str, str]]) -> int:
    return count_unique_values(data, 'InvoiceNo')

def get_total_quantity(data: List[Dict[str, str]], stock_code: int) -> int:
    return sum(int(item['Quantity']) for item in data if item['StockCode'] == str(stock_code))

def get_monthly_data():
    data = pd.read_csv(FILE2, skiprows=1, names=['Date', 'Offline Spend', 'Online Spend'])
    data['Offline Spend'] = data['Offline Spend'].astype(float)
    data['Online Spend'] = data['Online Spend'].astype(float)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Month'] = data['Date'].dt.to_period('M')
    data = data.drop(columns=['Date'])
    monthly_spend = data.groupby('Month').sum()

    sales_types = ['Online Spend', 'Offline Spend']
    sales_data = {sale_type: monthly_spend[sale_type].values for sale_type in sales_types}
    months = monthly_spend.index.strftime('%B')

    width = 0.6
    _, ax = plt.subplots(figsize=(8, 6))  # Adjust figure size
    left = np.zeros(len(months))

    for sales_type, data_values in sales_data.items():
        p = ax.barh(months, data_values, width, label=sales_type, left=left)
        left += data_values
        ax.bar_label(p, labels=data_values.round(2), label_type='center')

    for month, total in zip(months, monthly_spend.sum(axis=1)):
        ax.text(total, month, round(total, 2), ha='left', va='center')

    ax.set_title('Ежемесячные затраты', fontsize=14)  # Increase title font size
    ax.legend(prop={'size': 10})  # Increase legend font size
    ax.tick_params(axis='y', labelsize=10)  # Increase y-axis tick font size
    plt.tight_layout()
    plt.savefig('monthly.png')

def get_daily_data():
    data = pd.read_csv(FILE)
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    daily_sales = data.groupby(data['InvoiceDate'].dt.dayofyear)['Quantity'].sum()
    plt.figure(figsize=(10, 6))
    plt.scatter(daily_sales.index, daily_sales.values, color='orange', alpha=0.7)
    plt.xlabel('День в году', fontsize=12)  # Increase x-axis label font size
    plt.ylabel('Количество проданных товаров', fontsize=12)  # Increase y-axis label font size
    plt.title('Ежедневные продажи', fontsize=14)  # Increase title font size
    plt.xticks(range(1, 365, 15))
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('daily.png')

def main():
    data = read_data(FILE)
    print(f'Всего инвойсов (первые 5 строк): {count_invoices(data[:5])}')
    print(f'Всего инвойсов (первые 11 строк): {count_invoices(data[:11])}')
    print(f'Всего инвойсов: {count_invoices(data)}')
    print(f'Количество уникальных InvoiceNo: {count_unique_values(data, "InvoiceNo")}')
    print(f'Количество уникальных InvoiceDate: {count_unique_values(data, "InvoiceDate")}')
    print(f'Количество уникальных StockCode: {count_unique_values(data, "StockCode")}')
    print(f'Общее количество для StockCode 21421: {get_total_quantity(data, 21421)}')
    print(f'Общее количество для StockCode 22178: {get_total_quantity(data, 22178)}')
    data2 = MathStats(FILE2)
    print('Средние значения MathStats:', data2.mean)
    print('Максимальные значения MathStats:', data2.max)
    print('Минимальные значения MathStats:', data2.min)
    print('Дисперсия MathStats:', data2.disp)
    print('Квадрат стандартного отклонения MathStats:', data2.sigma_sq)
    get_daily_data()
    get_monthly_data()

if __name__ == "__main__":
    main()
