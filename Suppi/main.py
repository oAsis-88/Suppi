import numpy as np
import pandas as pd


def find_cost_tariff_for_each_warehouse(data):
    table = pd.DataFrame(data={'name': data['warehouse_name'].unique(),
                               'highway_cost': [0] * data['warehouse_name'].nunique()})

    for i, row in data.iterrows():
        cost = sum(map(lambda x: row['highway_cost'] * x['quantity'], row['products']))
        table.loc[table['name'] == row['warehouse_name'], 'highway_cost'] += cost

    return table


def find_qty_income_expense_profit(data):
    # Решением взять мапу было для уменьшения времени вставки данных в DataFrame
    # т.к. добавление в словарь занимает O(1), тк она основана на хэш-таблице
    # в худшем случае у нас получиться O(n^2), то же время, что и при поиске ячейки по имени продукта
    # в лучшем случае у нас получиться O(n), n - кол-во данных в исходном файле

    table = pd.DataFrame(columns=['product', 'quantity', 'income', 'expenses', 'profit'])

    index_of_names = {}

    for i, row in data.iterrows():
        for j, item in enumerate(row['products']):
            income = item['price'] * item['quantity']
            expenses = row['highway_cost'] * item['quantity']
            profit = income - expenses
            if item['product'] not in index_of_names:
                index_of_names[item['product']] = len(table.index)
                table.loc[len(table.index)] = [item['product'], item['quantity'], income, expenses, profit]
            else:
                table.iloc[index_of_names[item['product']], 1:] += [item['quantity'], income, expenses, profit]

    return table


def constitute_table_find_average_profit_order(data):
    # loc и iterrows - это очень временно затратная процедура
    # поэтому воспользуемся другими методами

    income = data['products'].apply(lambda x: sum(map(lambda y: y['price'] * y['quantity'], x)))
    expenses = data['highway_cost'] * data['products'].apply(lambda x: sum(map(lambda y: y['quantity'], x)))
    profit = income + expenses

    table = pd.concat([data['order_id'], profit], keys=['order_id', 'order_profit'], axis=1)

    average_profit_order = table['order_profit'].sum() / 2
    return table, average_profit_order


def constitute_percent_profit_product_of_warehouse(data):
    tmp = data.explode('products', ignore_index=True)
    node = pd.json_normalize(tmp['products'])

    quantity = data['products'].apply(lambda x: sum(map(lambda y: y['quantity'], x)))
    quantity.name = 'quantity'
    profit_table = node['quantity'] * (node['price'] + tmp['highway_cost'])
    profit_table.name = 'profit'

    table = pd.concat([tmp['warehouse_name'], node['product'], node['quantity'], profit_table], axis=1)

    profit_warehouse_name = table.groupby(['warehouse_name']).agg({'profit': 'sum'}).to_dict()

    profit_list = []
    for i, row in table.iterrows():
        profit_list.append(row['profit'] / profit_warehouse_name['profit'][row['warehouse_name']])

    table = table.assign(percent_profit_product_of_warehouse=profit_list)
    return table


def sorting_and_add_accumulated_percent_profit_product_of_warehouse(data):
    table = data.sort_values(by=['percent_profit_product_of_warehouse'])
    new_table = table.groupby('warehouse_name').agg({'percent_profit_product_of_warehouse': 'cumsum'}).to_dict()

    for k, v in new_table['percent_profit_product_of_warehouse'].items():
        table.loc[k, 'accumulated_percent_profit_product_of_warehouse'] = v

    return table


def assigning_category(data):
    accumulated = 'accumulated_percent_profit_product_of_warehouse'
    conditions = [
        np.less_equal(data[accumulated], 0.7),
        np.greater(data[accumulated], 0.7) & np.less_equal(data[accumulated], 0.9),
        np.greater(data[accumulated], 0.9),
    ]
    choices = ['A', 'B', 'C']

    # data['category'] = np.where(conditions, 'A', 'B')[0]
    data['category'] = np.select(conditions, choices)

    # data.loc[data['accumulated_percent_profit_product_of_warehouse'] <= 0.7, 'category'] = 'A'
    # data.loc[((data['accumulated_percent_profit_product_of_warehouse'] > 0.7) &
    #           (data['accumulated_percent_profit_product_of_warehouse'] <= 0.9)), 'category'] = 'B'
    # data.loc[data['accumulated_percent_profit_product_of_warehouse'] > 0.9, 'category'] = 'C'

    return data


if __name__ == "__main__":
    dataFrame = pd.read_json('resources/trial_task.json')

    task_1 = find_cost_tariff_for_each_warehouse(dataFrame)
    task_2 = find_qty_income_expense_profit(dataFrame)
    task_3, average_profit_order = constitute_table_find_average_profit_order(dataFrame)

    task_4 = constitute_percent_profit_product_of_warehouse(dataFrame)
    task_5 = sorting_and_add_accumulated_percent_profit_product_of_warehouse(task_4)
    task_6 = assigning_category(task_5)

    print(task_1)
    print(task_2)
    print(task_3)
    print(task_4)
    print(task_5)
    print(task_6)