import pandas as pd

from main import find_cost_tariff_for_each_warehouse

dataFrame = pd.read_json('resources/trial_task.json')
result = find_cost_tariff_for_each_warehouse(dataFrame)

print(result)
