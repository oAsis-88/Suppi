import pandas as pd

from main import constitute_table_find_average_profit_order

dataFrame = pd.read_json('resources/trial_task.json')
result, average_profit_order = constitute_table_find_average_profit_order(dataFrame)

print(result)
print(f"средняя прибыль заказов - {average_profit_order}")
