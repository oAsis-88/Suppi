import pandas as pd

from main import sorting_and_add_accumulated_percent_profit_product_of_warehouse
from task_4 import function_4

dataFrame = pd.read_json('resources/trial_task.json')


def function_5(data):
    tmp_data = function_4(data)
    result = sorting_and_add_accumulated_percent_profit_product_of_warehouse(tmp_data)
    return result


print(function_5(dataFrame))
