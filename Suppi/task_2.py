import pandas as pd

from main import find_qty_income_expense_profit

dataFrame = pd.read_json('resources/trial_task.json')
result = find_qty_income_expense_profit(dataFrame)

print(result)
