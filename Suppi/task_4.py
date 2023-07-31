import pandas as pd

from main import constitute_percent_profit_product_of_warehouse

dataFrame = pd.read_json('resources/trial_task.json')


def function_4(data):
    return constitute_percent_profit_product_of_warehouse(data)


print(function_4(dataFrame))
